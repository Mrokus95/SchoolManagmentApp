from django.db import models
from eventApp.models import Subject, Teacher
from usersApp.models import ClassUnit



class Classroom(models.Model):
    FLOOR_CHOICES = (
        (0, 'Ground floor'),
        (1, '1st floor'),
        (2, '2nd floor'),
    )

    floor = models.IntegerField(choices=FLOOR_CHOICES)
    room_number = models.CharField(max_length=4)

    def __str__(self):
        return f"Classroom: {self.room_number} (Floor: {self.floor})"


class ClassroomReservation(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
    )

    LESSON_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
    )

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    lesson_number = models.IntegerField(choices=LESSON_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    class_unit = models.ForeignKey(ClassUnit, on_delete=models.CASCADE)


    def __str__(self):
        return f"Reservation of {self.classroom} - Day: {self.get_day_of_week_display()} - Lesson {self.lesson_number}"


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=((1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday')), default=1)
    lesson_number = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')), default=1)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    class_name = models.ForeignKey(ClassUnit, on_delete=models.CASCADE, null=False, blank=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    is_base = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    classroom_reservation = models.OneToOneField(ClassroomReservation, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.get_day_of_week_display()} - Lesson {self.lesson_number}: {self.subject} ({self.teacher})"
    