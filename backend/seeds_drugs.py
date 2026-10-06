import json
from app import app, db, Drug

with open('interactions.json') as f:
    data = json.load(f)

with app.app_context():
    for drug_name in data['drugs']:
        existing = Drug.query.filter_by(name=drug_name).first()
        if not existing:
            db.session.add(Drug(name=drug_name, category='general'))
    db.session.commit()
    print(f"Seeded {len(data['drugs'])} drugs")