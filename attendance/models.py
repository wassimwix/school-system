from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    student_code = models.CharField(max_length=20, unique=True)
    birth_year = models.IntegerField()
    class_name = models.CharField(max_length=50)




class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)