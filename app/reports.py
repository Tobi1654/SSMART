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
    