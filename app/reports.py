from io import BytesIO
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib import colours
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from reportlab.graphics.shapes import Drawing, Circle, String
from reportlab.graphics.charts.piecharts import Pie

from app.models import Student, Subject, Grade, Class

def generate_report(student_id): #This gets the student id and looks them up in the database
    student = Student.query.get(student_id)
    if not student: 
        return None

    student_class = Class.query.get(student.class_id) # this gets rge students class name nad year group

    raw_grades = Grade.query.filter_by(student_id=student_id).order_by(Grade.date.desc()).all() #This gets the students grades
    
    grades = []
    for g in raw_grades:
        subject  = Subject.query.get(g.subject_id)
    
        grades.append({
            'subject_name': subject.subject_name if subject else '-',
            'assessment_name': g.assessment_name,
            'score': f'{g.student_score}/{g.max_score}',
            'percentage': g.percentage,
            'letter_grade': g.letter_grade,
            'date': g.date,
            'feedback': g.feedback or ''
        })

    #this gets the average percentage for each subject
    subject_totals = {}
    subject_counts = {}

    for g in raw_grades:
        subject  = Subject.query.get(g.subject_id)
        name = subject.subject_name if subject else '-'

        if name not in subject_totals:
            subject_totals[name] = 0
            subject_counts[name] = 0

        subject_totals[name] = subject_totals[name] + g.percentage
        subject_counts[name] = subject_counts[name] + 1

        subject_averages = {}
        for name in subject_totals:
            average = subject_totals[name] / subject_counts[name]
            subject_averages[name] =round(average,2)


    att_percentage = student.attendance_percentage or 0 # This gets the calculated attendance

    buffer = BytesIO() #This creates the file PDF
    doc = SimpleDocTemplate( #this sets up the document
        buffer,
        pagesize = A4,
        leftMargin = 2*cm,
        rightMargin = 2*cm,
        topMargin = 2*cm,
        bottomMargin = 2*cm,
    )

    styles = getSampleStyleSheet()
    heading = ParagraphStyle(
        'Heading',
        parent = styles['Heading1'],
        alignment=1,
        textColor=colours.blue,
    )

    subheading = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading2'],
        textColor=colours.lightblue,
        spaceAfter=4
    )

    normal = styles['Normal']

    elements = []

#heading
    elements.append(Paragraph('SSMART Progress Report', heading))
    elements.append(Spacer(1, 0.4*cm))

#list of roles for student info
    info_data = [
        ['Name: ', student.full_name],
        ['Class: ', f'{student_class.class_name} (Year{student_class.year_group})' if student_class else '-'],
        ['Date of Birth: ', student.dob.strftime('%d/%m/%Y') if student.dob else '-'],
        ['Attendance: ', f'{att_percentage}%'],
        ['Report date: ' date.today().strftime('%d/%m/%Y')],
    ]

#table styling
    info_table = Table(info_data, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Courier')
        ('FONTSIZE', (0,0), (-1,-1), 10)
        ('BOTTOMPADDING', (0,0), (-1,-1), 4)
        ('TOPPADDING', (0,0), (-1,-1), 4)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 0.6*cm))