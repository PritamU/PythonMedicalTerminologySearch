from app import create_app, db
from app.models import Diagnosis
from sqlalchemy import func 

app = create_app()

def already_seeded():
    return db.session.query(Diagnosis).first() is not None
def remove_values():
    return db.drop_all()

def seed_from_txt(filepath="data.txt"):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    count = 0
    for i, line in enumerate(lines):
        if i%2 == 0 or "id" in line:  # skip header
            continue
        parts = line.strip().split("\t")
        if len(parts) != 9:
            print(f"[WARN] Skipped malformed line {i+1}: {line.strip()}")
            continue
        try:
            concept = Diagnosis(
                effectiveTime=parts[1],
                active=bool(int(parts[2])),
                moduleId=parts[3],
                conceptId=parts[4],
                languageCode=parts[5],
                typeId=parts[6],
                term=parts[7],
                caseSignificanceId=parts[8],
                search_vector=func.to_tsvector('english', parts[7])
            )
            db.session.add(concept)
            count += 1
        except Exception as e:
            print(f"[ERROR] Line {i+1}: {e}")
    db.session.commit()
    print(f"[INFO] Seeded {count} records into the database.")

with app.app_context():
    db.create_all()
    if not already_seeded():
        print("[INFO] Seeding data from data.txt...")
        seed_from_txt()
    else:
        # remove_values()
        # seed_from_txt()
        print("[INFO] Data already seeded, skipping.")
