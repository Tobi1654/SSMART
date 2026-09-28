from app.models import Attendance, Student, Notification, User
from app.extensions import db

def calculate_attendance_percentage(student_id):
    records = Attendance.query.filter_by(student_id=student_id).all() # fetches all the attendance records for the student

    if not records:
        return 0.0 #if teh student has no records they automatically have 0%

    total = len(records) #this is the total number of attendance entries
    present_count = 0
    late_count = 0
    absent_count = 0

    for r in records: #loops through the attendance records counting all the presents, late's and absents
        if r.status == 'present':
            present_count += 1
        elif r.status == 'late':
            late_count += 1
        else:
            absent_count += 1

    percentage = ((present_count/total)*100) + ((late_count/total)*75) # calculating the attendance formula
    return round(percentage, 1)# rounds the attendance percentage to 1 decimal place

def create_attendance_flag(student_id, class_id):
    student = Student.query.get(student_id)
    if not student:
        return False

    if student.attendance_percentage is None or student.attendance_percentage >= 80:
        return False

    student_user = User.query.get(student.user_id) #fetches the students user_id for notifications
    if not student_user:
        return False

    #checks if the unread threshold flag notification already exists
    flag_exists = Notification.query.filter_by(user_id=student_user.user_id, type='alert').filter(Notification.title.like('%Attendance%')).filter(Notification.message.like(f'% {student.full_name} %')).first()

    if flag_exists: #if the student is already flagged, it would not create another one
        return False

    notification = Notification(
        user_id = student_user.user_id,
        title = 'Attendance Update',
        message = f'{student.full_name} attendance has dropped below 80%, you now have an attendance of {student.attendance_percentage}%',
        type = 'alert',
        read_status = False
    ) #creates the notification to send to the student

    db.session.add(notification)
    db.session.commit()

    return True
