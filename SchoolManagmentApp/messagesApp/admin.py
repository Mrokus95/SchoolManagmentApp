from django.contrib import admin
from .models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ['sender', 'receiver', 'title', 'date']
    list_filter = ['sender', 'receiver', 'is_trash']
    ordering = ['sender', 'date']