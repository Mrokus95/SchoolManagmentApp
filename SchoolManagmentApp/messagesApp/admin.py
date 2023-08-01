from django.contrib import admin
from .models import Message
# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ['id', 'sender', 'receiver', 'title', 'date']
    list_filter = ['sender', 'receiver']
    ordering = [ '-id','sender']
