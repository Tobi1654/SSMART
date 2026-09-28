from app import create_app
from app.models import Student, Attendance, Class

app = create_app()

with app.app_context():
    print("\n=== STUDENTS ===")
    for s in Student.query.all():
        print(f"{s.full_name}: {s.attendance_percentage}% (class_id={s.class_id})")

    print("\n=== ATTENDANCE RECORDS ===")
    for a in Attendance.query.all():
        student = Student.query.get(a.student_id)
        print(f"{student.full_name}: {a.status} on {a.date}")

    print("\n=== CLASSES ===")
    for c in Class.query.all():
        print(f"{c.class_name}: avg = {c.average_attendance}")