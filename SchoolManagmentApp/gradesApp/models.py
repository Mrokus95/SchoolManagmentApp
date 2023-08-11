from django.db import models
from eventApp.models import LessonReport, Subject, Teacher
from usersApp.models import Student


class Semester(models.Model):
    number = models.IntegerField(choices=[(1, 1), (2, 2)])
    start_school_year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Semester {self.number} Year {self.start_school_year}/{self.start_school_year + 1}"

    class Meta:
        unique_together = ("number", "start_school_year")


class Grades(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    GRADE_CHOICES = [(ONE, 1), (TWO, 2), (THREE, 3), (FOUR, 4), (FIVE, 5), 
                    (SIX, 6)]

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_grades"
    )
    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES)
    grade_description = models.CharField(max_length=250)
    connected_to_lesson = models.ForeignKey(
        LessonReport, on_delete=models.CASCADE, 
        related_name="connected_to_lesson"
    )
    date = models.DateField(auto_now_add=True)
    submitted_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="subject_grades"
    )
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="grades"
    )

    def __str__(self):
        return f"Student: {self.student}, class: {self.student.class_unit} Grade: {self.grade}, lesson: {self.subject}, date: {self.date}"

    class Meta:
        ordering = ("date",)
