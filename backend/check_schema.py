from app import create_app
from app.extensions import db
app = create_app()
with app.app_context():
    r = db.session.execute(db.text("PRAGMA table_info(subjects)")).fetchall()
    print("Columns:", r)
    r2 = db.session.execute(db.text("PRAGMA index_list(subjects)")).fetchall()
    print("Indexes:", r2)
    for idx in r2:
        r3 = db.session.execute(db.text(f"PRAGMA index_info({idx[1]})")).fetchall()
        print(f"  Index {idx[1]}:", r3)
