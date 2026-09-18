from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    if User.query.first(): #this function checks for already existing users
        print("User already exists")
    else:
        admin = User( # creating a testing admin account
            username='admin1',
            email='admin1@school.org.uk',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        teacher = User( #creating a test teacher account
            username='teacher1',
            email='teacher1@school.org.uk',
            role='teacher'
        )
        teacher.set_password('teacher123')
        db.session.add(teacher)

        student = User( # creating test student account
            username='student1',
            email='student1@school.org.uk',
            role='student'
        )
        student.set_password('student123')
        db.session.add(student)


        db.session.commit()
        print("""
                Test users created:
                1. admin1 / admin123 (admin)
                2. teacher1 / teacher123 (teacher)
                3. Micheal.Drew / student123 (student)
            """)