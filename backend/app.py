from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
import joblib
override_model = joblib.load('ml/override_predictor.pkl')

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:newpassword@localhost/prescription_audit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with open('interactions.json') as f:
    interaction_data = json.load(f)

interaction_lookup = {}
for pair in interaction_data['interactions']:
    key = frozenset([pair['drug_a'].lower(), pair['drug_b'].lower()])
    interaction_lookup[key] = pair
print(f"Loaded {len(interaction_lookup)} interaction pairs")
print("Warfarin+Aspirin in lookup?", frozenset(['warfarin', 'aspirin']) in interaction_lookup)

def check_interactions(drug_names):
    flagged = []
    for i in range(len(drug_names)):
        for j in range(i + 1, len(drug_names)):
            key = frozenset([drug_names[i].lower(), drug_names[j].lower()])
            if key in interaction_lookup:
                pair = interaction_lookup[key]
                flagged.append({
                    "drug_a": drug_names[i],
                    "drug_b": drug_names[j],
                    "severity": pair['severity'],
                    "note": pair['note']
                })
    return flagged

# ---------- MODELS ----------

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    allergies = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Drug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50))

prescription_drugs = db.Table('prescription_drugs',
    db.Column('prescription_id', db.Integer, db.ForeignKey('prescription.id'), primary_key=True),
    db.Column('drug_id', db.Integer, db.ForeignKey('drug.id'), primary_key=True)
)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_name = db.Column(db.String(100))
    condition = db.Column(db.String(255))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    drugs = db.relationship('Drug', secondary=prescription_drugs, backref='prescriptions')
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'))
    action = db.Column(db.String(50))
    doctor_name = db.Column(db.String(100))
    details = db.Column(db.Text)
    override_reason = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # plain for student project; note limitation in report
    role = db.Column(db.String(20), nullable=False)  # 'doctor' or 'admin'
    full_name = db.Column(db.String(100))


def serialize_prescription(p):
    """Return the format used by the admin prescription tables."""
    log = AuditLog.query.filter_by(prescription_id=p.id).order_by(AuditLog.timestamp.desc()).first()
    return {
        "id": p.id,
        "patient_id": p.patient_id,
        "doctor_name": p.doctor_name,
        "drugs": [d.name for d in p.drugs],
        "created_at": p.created_at.strftime('%Y-%m-%d %H:%M:%S') if p.created_at else None,
        "was_overridden": log.action == 'override' if log else False,
        "override_reason": log.override_reason if log else None
    }

# ---------- ROUTES ----------

@app.route('/')
def home():
    return {"message": "Backend is running"}

@app.route('/db-check')
def db_check():
    try:
        db.session.execute(db.text('SELECT 1'))
        return {"message": "Database connected successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(
        name=data['name'],
        age=data.get('age'),
        gender=data.get('gender'),
        allergies=data.get('allergies')
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient added", "id": new_patient.id})

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    result = []
    for p in patients:
        result.append({
            "id": p.id, "name": p.name, "age": p.age,
            "gender": p.gender, "allergies": p.allergies
        })
    return jsonify(result)

@app.route('/drugs', methods=['GET'])
def get_drugs():
    drugs = Drug.query.all()
    return jsonify([{"id": d.id, "name": d.name} for d in drugs])

@app.route('/prescriptions', methods=['POST'])
def add_prescription():
    data = request.json
    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    drug_ids = data['drug_ids']
    drugs = Drug.query.filter(Drug.id.in_(drug_ids)).all()
    drug_names = [d.name for d in drugs]

    warnings = check_interactions(drug_names)

    if warnings and not data.get('override_reason'):
        return jsonify({
            "message": "Interaction warnings found, override reason required to proceed",
            "interaction_warnings": warnings,
            "requires_override": True
        }), 200

    new_prescription = Prescription(
    patient_id=data['patient_id'],
    doctor_name=data.get('doctor_name'),
    condition=data.get('condition'),
    remarks=data.get('remarks')
)
    new_prescription.drugs = drugs
    db.session.add(new_prescription)
    db.session.commit()

    log = AuditLog(
        prescription_id=new_prescription.id,
        action='override' if warnings else 'create',
        doctor_name=data.get('doctor_name'),
        details=f"Drugs: {', '.join(drug_names)}",
        override_reason=data.get('override_reason')
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": "Prescription created",
        "id": new_prescription.id,
        "interaction_warnings": warnings
    })

@app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    prescriptions = Prescription.query.all()
    result = []
    for p in prescriptions:
        result.append({
            "id": p.id, "patient_id": p.patient_id,
            "doctor_name": p.doctor_name,
            "drugs": [d.name for d in p.drugs]
        })
    return jsonify(result)
@app.route('/predict-override-risk', methods=['POST'])
def predict_override_risk():
    data = request.json
    features = [[
        data['severity'],
        data['patient_age'],
        data['allergy_count'],
        data['active_med_count'],
        data['doctor_override_rate'],
        data['time_of_day_busy']
    ]]
    probability = override_model.predict_proba(features)[0][1]
    return jsonify({'override_likelihood': round(float(probability), 2)})

@app.route('/audit-log', methods=['GET'])
def get_audit_log():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "prescription_id": log.prescription_id,
            "action": log.action,
            "doctor_name": log.doctor_name,
            "details": log.details,
            "override_reason": log.override_reason,
            "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result)

@app.route('/audit-log/stats', methods=['GET'])
def audit_stats():
    total = AuditLog.query.count()
    overrides = AuditLog.query.filter_by(action='override').count()
    override_rate = round((overrides / total) * 100, 1) if total > 0 else 0
    return jsonify({
        "total_actions": total,
        "total_overrides": overrides,
        "override_rate_percent": override_rate
    })
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({
        "username": user.username,
        "role": user.role,
        "full_name": user.full_name
    })
@app.route('/prescriptions/detailed', methods=['GET'])
def get_prescriptions_detailed():
    doctor_filter = request.args.get('doctor_name')
    query = Prescription.query
    if doctor_filter:
        query = query.filter(Prescription.doctor_name == doctor_filter)
    prescriptions = query.order_by(Prescription.created_at.desc()).all()

    return jsonify([serialize_prescription(p) for p in prescriptions])

@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Load the admin dashboard from one consistent database snapshot."""
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    total = len(logs)
    overrides = sum(log.action == 'override' for log in logs)

    doctors = db.session.query(AuditLog.doctor_name).distinct().all()
    doctor_summary = []
    for (doctor_name,) in doctors:
        doctor_logs = [log for log in logs if log.doctor_name == doctor_name]
        doctor_overrides = sum(log.action == 'override' for log in doctor_logs)
        doctor_summary.append({
            "doctor_name": doctor_name,
            "total_prescriptions": len(doctor_logs),
            "overrides": doctor_overrides,
            "override_rate_percent": round((doctor_overrides / len(doctor_logs)) * 100, 1) if doctor_logs else 0
        })
    doctor_summary.sort(key=lambda item: -item['override_rate_percent'])

    return jsonify({
        "audit_logs": [{
            "id": log.id,
            "prescription_id": log.prescription_id,
            "action": log.action,
            "doctor_name": log.doctor_name,
            "details": log.details,
            "override_reason": log.override_reason,
            "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S') if log.timestamp else None
        } for log in logs],
        "stats": {
            "total_actions": total,
            "total_overrides": overrides,
            "override_rate_percent": round((overrides / total) * 100, 1) if total else 0
        },
        "doctor_summary": doctor_summary,
        "prescriptions": [serialize_prescription(p) for p in Prescription.query.order_by(Prescription.created_at.desc()).all()]
    })
@app.route('/doctors/override-summary', methods=['GET'])
def doctor_override_summary():
    doctors = db.session.query(AuditLog.doctor_name).distinct().all()
    summary = []
    for (doctor_name,) in doctors:
        total = AuditLog.query.filter_by(doctor_name=doctor_name).count()
        overrides = AuditLog.query.filter_by(doctor_name=doctor_name, action='override').count()
        rate = round((overrides / total) * 100, 1) if total > 0 else 0
        summary.append({
            "doctor_name": doctor_name,
            "total_prescriptions": total,
            "overrides": overrides,
            "override_rate_percent": rate
        })
    summary.sort(key=lambda x: -x['override_rate_percent'])
    return jsonify(summary)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)
