from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def get_inbox(request):
    if request.method == 'GET':
        inbox_messages = Message.objects.filter(receiver=request.user.profile)
        count = len(inbox_messages)
        test = count
        inbox_messages_number = Message.objects.filter(receiver=request.user.profile).count()
        context={'inbox_messages': inbox_messages,
                 'inbox_messages_number': inbox_messages_number,
                 'test' : 'test'}
        return render(request, 'inbox.html', context)
