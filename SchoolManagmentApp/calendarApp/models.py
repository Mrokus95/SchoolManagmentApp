from django.db import models
from eventApp.models import Subject, Teacher
from usersApp.models import Profile, ClassUnit
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=((1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday')), default=1)
    lesson_number = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')), default=1)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    class_name = models.ForeignKey(ClassUnit, on_delete=models.CASCADE, null=False, blank=False)
    classroom = models.CharField(max_length=50, default="Not assigned")
    date = models.DateField(null=False, blank=False)
    is_base = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.get_day_of_week_display()} - Lesson {self.lesson_number}: {self.subject} ({self.teacher})"
    