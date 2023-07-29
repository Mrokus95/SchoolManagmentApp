from django.db import models
from usersApp.models import Profile

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE , related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}, dated: {self.date}'