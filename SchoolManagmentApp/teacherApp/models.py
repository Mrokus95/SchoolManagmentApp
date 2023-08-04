from django.db import models
from usersApp.models import Student
from eventApp.models import LessonReport, Teacher, Subject

# Create your models here.

class Grades(models.Model):

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    GRADE_CHOICES=[
        (ONE, 1),
        (TWO, 2),
        (THREE, 3),
        (FOUR, 4),
        (FIVE, 5),
        (SIX, 6)
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_grades')
    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES)
    grade_description = models.CharField(max_length=250)
    connected_to_lesson = models.ForeignKey(LessonReport, on_delete=models.CASCADE, related_name='connected_to_lesson')
    date = models.DateField(auto_now_add=True)
    submited_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_grades')

    def __str__(self):
        return f'Student: {self.student}, class: {self.student.class_unit} Grade: {self.grade}, lesson: {self.subject}, date: {self.date}'