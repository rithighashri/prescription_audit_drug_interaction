from app import app, db, User
import random

first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
               "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
               "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
               "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
               "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
               "Timothy", "Deborah"]

last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
              "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
              "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
              "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
              "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
              "Carter", "Roberts"]

with app.app_context():
    db.create_all()

    users_to_add = []

    # 2 fixed admin accounts (easy to remember for demo/viva)
    users_to_add.append({"username": "admin", "password": "admin123", "role": "admin", "full_name": "Admin User"})
    users_to_add.append({"username": "admin2", "password": "admin123", "role": "admin", "full_name": "Admin Two"})

    # 48 doctor accounts, generated from name lists
    used_usernames = {"admin", "admin2"}
    doctor_count = 0
    idx = 0
    while doctor_count < 48:
        first = first_names[idx % len(first_names)]
        last = last_names[idx % len(last_names)]
        username = f"dr.{last.lower()}{idx}"  # index avoids duplicate usernames
        if username not in used_usernames:
            users_to_add.append({
                "username": username,
                "password": "doctor123",
                "role": "doctor",
                "full_name": f"Dr. {first} {last}"
            })
            used_usernames.add(username)
            doctor_count += 1
        idx += 1

    added = 0
    for u in users_to_add:
        if not User.query.filter_by(username=u['username']).first():
            db.session.add(User(**u))
            added += 1

    db.session.commit()
    print(f"Seeded {added} new users. Total users in table: {User.query.count()}")