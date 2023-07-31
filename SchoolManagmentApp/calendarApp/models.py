from django.db import models
from eventApp.models import Subject, Teacher
from usersApp.models import Profile, ClassUnit
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=((1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday')), default=1)
    lesson_number = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')), default=1)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    classroom = models.CharField(max_length=50, default="Not assigned")
    is_cancelled = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.get_day_of_week_display()} - Lesson {self.lesson_number}: {self.subject} ({self.teacher})"
    
class WeeklySchedule(models.Model):
    week_number = models.IntegerField()
    class_name = models.ForeignKey(ClassUnit, on_delete=models.CASCADE)
    is_base_schedule = models.BooleanField(default=False)
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return f"Schedule - Week {self.week_number} - Class {self.class_name}"