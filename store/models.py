from django.db import models
from projectaccount.models import Semester,Subject

# Create your models here.

class Student(models.Model):
    semester = semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="student_semester", null=True, blank=True
    )
    name = models.CharField(max_length=50,null=True,blank=True)
    register_number = models.IntegerField(null=True,blank=True)
    roll_number = models.IntegerField(null=True,blank=True)


class TheoryInternalMark(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_name", null=True, blank=True
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="Theory_subject", null=True, blank=True
    )
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="semester_theory_mark", null=True, blank=True
    )

    se1 = models.IntegerField(null=True,blank=True)
    se2 = models.IntegerField(null=True,blank=True)
    se3 = models.IntegerField(null=True,blank=True)

    assignment1 = models.IntegerField(null=True,blank=True)
    assignment2 = models.IntegerField(null=True,blank=True)
    assignment3 = models.IntegerField(null=True,blank=True)

    attendance_percentage = models.IntegerField(null=True,blank=True)


class LabInternalMark(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="Lab_student_name", null=True, blank=True
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="Lab_subject", null=True, blank=True
    )
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="semester_Lab_mark", null=True, blank=True
    )
   
    test1 = models.IntegerField(null=True,blank=True)
    test2 = models.IntegerField(null=True,blank=True)

    rough_record_mark = models.IntegerField(null=True,blank=True)
    fair_record_mark = models.IntegerField(null=True,blank=True)
    lab_work_mark = models.IntegerField(null=True,blank=True)
    open_ended_mark = models.IntegerField(null=True,blank=True)
    attendance_mark = models.IntegerField(null=True,blank=True)
