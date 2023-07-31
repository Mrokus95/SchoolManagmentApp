from django.shortcuts import render

# Create your views here.

def teacher_app_start(request):
    
    return render(request, 'teacher_app_start.html')

