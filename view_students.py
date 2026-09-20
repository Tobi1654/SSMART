from app import create_app
from app.models import User, Student

app = create_app()

with app.app_context():
    users = User.query.filter_by(role='student').all()
    print(f"\n {len(users)} Students  \n")
    for u in users:
        student = Student.query.filter_by(user_id=u.user_id).first()
        if student:
            print(f"Username: {u.username}")
            print(f"Email: {u.email}")
            print(f"Full Name: {student.full_name}")
            print(f"DOB: {student.dob}")
            print(f"Class ID: {student.class_id}")
            print(f"Enrolled: {student.date_enrolled}")
            print("-" * 40)
        else:
            print(f"Username: {u.username} — NO STUDENT RECORD")