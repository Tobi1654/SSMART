from app import create_app
from app.extensions import db
from app.models import Student

app = create_app()

with app.app_context():
    s = Student.query.first()
    if s:
        s.is_sen = True
        db.session.commit()
        print(f'{s.full_name} marked as SEN')