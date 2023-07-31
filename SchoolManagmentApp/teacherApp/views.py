from django.shortcuts import render
from usersApp.models import Profile
from eventApp.models import Teacher
from eventApp.models import LessonReport, CalendarEvents
from django.contrib import messages
from eventApp.views import event_paginator
# Create your views here.


def teacher_app_teacher(request):
    current_teacher = Teacher.objects.get(user=request.user.profile)

    if LessonReport.objects.filter(teacher=current_teacher.id).exists():
        current_reports = LessonReport.objects.filter(teacher=current_teacher.id)
        pages = event_paginator(request, current_reports, 7)

        context = {
            'pages': pages,
            'current_teacher': current_teacher,
                   }

        return render(request, 'teacher_app.html', context)
    
    else:
        messages.error(request, "U have no reports")
        return render(request, 'teacher_app')


def report_detail(request, reportId):

    current_report = LessonReport.objects.get(id=reportId)
    connected_events = CalendarEvents.objects.filter(connected_to_lesson=current_report.id)
    context={
        'current_report': current_report,
        'connected_events': connected_events,
        }

    return render(request, 'report_detail.html', context)

def teacher_app_stuent(request):
    pass




def teacher_app_start(request):
    current_profile = Profile.objects.get(user=request.user)
    account_type = current_profile.account_type

    if account_type == "Teacher":
        return teacher_app_teacher(request)
    else:
        return teacher_app_stuent(request)

    

