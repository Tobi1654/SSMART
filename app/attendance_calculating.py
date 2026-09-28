from app.models import Attendance, Student

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