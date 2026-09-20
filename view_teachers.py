from app import create_app
from app.models import User, Teacher

app = create_app()

with app.app_context():
    teachers = User.query.filter_by(role='teacher').all()
    print(f"\n{len(teachers)} Teachers in database")
    for user in teachers:
        teacher = Teacher.query.filter_by(user_id=user.user_id).first()
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Full Name: {teacher.full_name if teacher else 'MISSING'}")
        print(f"Department: {teacher.department if teacher else 'MISSING'}")
        print(f"Subjects: {teacher.subjects if teacher else 'MISSING'}")
        