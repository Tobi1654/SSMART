from app import create_app
from app.models import Class

app = create_app()

with app.app_context():
    classes = Class.query.all()
    print(f"\n {len(classes)} Classes in the database \n")
    for c in classes:
        print(f"Class ID: {c.class_id}")
        print(f"Class Name: {c.class_name}")
        print(f"Year Group: {c.year_group}")
        print(f"Teacher ID: {c.teacher_id} ")
        print("-" * 40)