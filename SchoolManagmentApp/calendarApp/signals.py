from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Lesson


@receiver(post_delete, sender=Lesson)
def delete_related_reservations(sender, instance, **kwargs):
    if instance.classroom_reservation:
        instance.classroom_reservation.delete()
    if instance.teacher_reservation:
        instance.teacher_reservation.delete()
