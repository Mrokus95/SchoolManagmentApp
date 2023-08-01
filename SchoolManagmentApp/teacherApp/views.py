from django.shortcuts import render
from usersApp.models import Profile
from eventApp.models import Teacher
from eventApp.models import LessonReport, CalendarEvents, Subject
from django.contrib import messages
from eventApp.views import event_paginator
from .forms import LessonRportFilter
from usersApp.models import ClassUnit 
# Create your views here.


def reports_student_filter(request, queryset):

    subject_condition = request.POST.get('subject')
    start_date_condition = request.POST.get('start_date')
    class_condition = request.POST.get('class_unit')

    if subject_condition != 'All':
        queryset = queryset.filter(subject__name=subject_condition)
               
    if start_date_condition:
        queryset = queryset.filter(create_date__gte=start_date_condition)

    if class_condition:
        condition_year = int(class_condition[0])
        condition_letter_mark = class_condition[1]
        queryset = queryset.filter(class_unit__study_year=condition_year)
        queryset = queryset.filter(class_unit__letter_mark=condition_letter_mark)

    return queryset

def teacher_app_teacher(request):
    current_teacher = Teacher.objects.get(user=request.user.profile)

    if LessonReport.objects.filter(teacher=current_teacher.id).exists():
        current_reports = LessonReport.objects.filter(teacher=current_teacher.id).order_by('create_date')
        subject_choices =[('All', 'All')] + [(subject.name, subject.name) for subject in Subject.objects.all()]

        class_choices = [('All', 'All')] + [(str(unit.study_year) + unit.letter_mark, str(unit.study_year) + unit.letter_mark) for unit in ClassUnit.objects.all()]

        filter_form = LessonRportFilter(request.POST)

        if request.method == 'POST':
            current_reports = reports_student_filter(request, current_reports)
            pages = event_paginator(request, current_reports, 7)

        else:
            pages = event_paginator(request, current_reports, 7)
        context = {
            'pages': pages,
            'current_teacher': current_teacher,
            'filter_form': filter_form,
            'subject_choices': subject_choices,
            'class_choices': class_choices,
            }
        return render(request, 'teacher_app.html', context)
    
    else:
        messages.error(request, "You have no reports")
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

    

