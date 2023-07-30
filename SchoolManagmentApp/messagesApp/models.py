from django.db import models
from usersApp.models import Profile
from django.urls import reverse

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE , related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    is_read_receiver = models.BooleanField(default=False)
    is_read_sender = models.BooleanField(default=False)
    is_delete_receiver = models.BooleanField(default=False)
    is_delete_sender = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}, dated: {self.date}'
    
    def get_absolute_url(self, is_sender=False):
        if self.is_sender:
            return reverse('sent_email_detail',
                    args=[str(self.id)])
        else:
            return reverse('email_detail',
                        args=[str(self.id)])