from django.db import models
from usersApp.models import Profile, ClassUnit
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class PlanOfLesson(models.Model):
    class_unit = models.OneToOneField(Profile, on_delete=models.CASCADE,
                                       related_name='plan_of_lesson')

class Subject(models.Model):
    MATH = "Math"
    ENGLISH = "English"
    SUBJECT_CHOICES = [
    (MATH, "Mathematic"),
    (ENGLISH, "English"),
    ('','')
        ]
    name = models.CharField(max_length=100, choices=SUBJECT_CHOICES, default='')

    def __str__(self):
        return f'{self.name} prowadzący: {self.subject_teachers.user}'

class Teacher(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.DO_NOTHING, related_name='teacher', to_field= 'last_name')
    lesson_type = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, blank=False, null=False, related_name='subject_teachers')

class Day(models.Model):
    DAYS_OF_WEEK = [
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ]
    
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, unique=True)
    
    def __str__(self):
        return self.get_day_of_week_display()

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    day = models.ForeignKey(Day, on_delete=models.DO_NOTHING)
    order = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(7)
    ])
    
# Conduction of lesson

class LessonReport(models.Model):
    create_date = models.DateField(auto_now_add=True)
    subject = models.ForeignKey(Subject, related_name='reports_subject', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher, related_name='reports_teacher', on_delete=models.DO_NOTHING)
    class_unit = models.ForeignKey(ClassUnit, related_name='reports_class_unit', on_delete=models.DO_NOTHING)
    lesson_title = models.CharField(max_length=250)
    lesson_description = models.TextField()

class CalendarEvents(models.Model):
    pass
       

 

class Attendance(models.Model):
    lesson_report = models.OneToOneField(LessonReport, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_name} - {self.lesson.day} - {self.lesson_report.create_date} - {'Obecny' if self.is_present else 'Nieobecny'}"