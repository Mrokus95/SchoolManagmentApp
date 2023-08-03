from django.shortcuts import render, redirect, reverse
from usersApp.models import Profile, Student
from eventApp.models import Teacher
from eventApp.models import LessonReport, CalendarEvents, Subject, Attendance
from django.contrib import messages
from eventApp.views import event_paginator, student_events
from .forms import LessonRportFilter, ClassSubjectChoiceForm, AttendanceForm
from usersApp.models import ClassUnit
from datetime import date
from django.forms import formset_factory


# Create your views here.



def teacher_required(func):
    def _wrapped_func(request, *args, **kwargs):
        if request.user.profile.account_type != 'Teacher':
            messages.error(request, "Only for teachers!")
            return redirect('home')         
        return func(request, *args, **kwargs)  
    return _wrapped_func

def reports_student_filter(request, queryset):
    subject_condition = request.POST.get('subject')
    start_date_condition = request.POST.get('start_date')
    class_condition = request.POST.get('class_unit')

    if subject_condition != 'All':
        queryset = queryset.filter(subject__name=subject_condition)
               
    if start_date_condition:
        queryset = queryset.filter(create_date=start_date_condition)

    if class_condition != 'All':
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
        filter_form = LessonRportFilter

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

def report_detail(request, reportId, requested=False):
    current_report = LessonReport.objects.get(id=reportId)
    connected_events = CalendarEvents.objects.filter(connected_to_lesson=current_report.id)
    if requested:
        
        context={
        'current_report': current_report,
        'connected_events': connected_events,
        'requested' : requested,
        }
        return render(request, 'report_detail.html', context)

    else:
        context={
            'current_report': current_report,
            'connected_events': connected_events,
         }
        return render(request, 'report_detail.html', context)

def teacher_app_start(request):
    current_profile = Profile.objects.get(user=request.user)
    account_type = current_profile.account_type

    if account_type == "Teacher":
        return teacher_app_teacher(request)
    
    else:
        return student_events(request)

def from_event_to_raport(request, eventId):
    event = CalendarEvents.objects.get(id=eventId)
    reportId = event.connected_to_lesson.id
    curret_profile = Profile.objects.get(user=request.user)
    account_type = curret_profile.account_type

    if account_type == "Teacher":        
        return report_detail(request, reportId, True)
        
    else:
        current_report = LessonReport.objects.get(id=reportId)
        connected_events = CalendarEvents.objects.filter(connected_to_lesson=current_report.id)
        context={
            'connected_evens': connected_events,
            'current_report': current_report,
        }
        return render(request, 'pure_report.html', context)      

@teacher_required
def lesson_delivery_start(request):
    class_choices =[(str(unit.study_year) + unit.letter_mark, str(unit.study_year) + unit.letter_mark) for unit in ClassUnit.objects.all()]

    subject_choices =[(subject.name, subject.name) for subject in Subject.objects.all()]

    if request.method == 'POST':
        form_subject = request.POST.get('subject')
        selected_subject = Subject.objects.get(name=form_subject)

        form_class = request.POST.get('class_unit')
        class_year = int(form_class[0])
        class_letter_mark = form_class[1]
        selected_class = ClassUnit.objects.filter(study_year=class_year, letter_mark=class_letter_mark)
        current_teacher = Teacher.objects.get(user=request.user.profile)
       
        lesson_report = LessonReport.objects.create(
            create_date=date.today(),
            subject=selected_subject,
            teacher=current_teacher,
            class_unit=selected_class.first(),
            lesson_title='Initial Title',
            lesson_description = 'Initial Description',
        )      
        messages.success(request, "Lesson created!")
        return redirect('lesson_class_initiation', lesson_report.id)

    else:
        choice_class_subject_form = ClassSubjectChoiceForm()
        context={
            'user': request.user,
            'class_choices': class_choices,
            'subject_choces': subject_choices,
            'choice_class_subject_form': choice_class_subject_form,
                }      
        return render(request, 'lesson_delivery_start.html', context)
    
@teacher_required
def lesson_class_initiation(request, lesson_report_id):
    current_lesson_report = LessonReport.objects.get(id=lesson_report_id)
    students = Student.objects.filter(class_unit=current_lesson_report.class_unit)

    if request.method == 'POST':

        for participant in students:
            checkbox_key = str(participant.id)
            attendance_object = Attendance.objects.create(
                lesson_report = current_lesson_report,
                student = participant,
                is_present=request.POST.get(checkbox_key, False) == 'True'
                )
            messages.success(request, "Attendance checked!")
            return redirect('lesson_conducting', current_lesson_report.id)
        
    else:
        form = AttendanceForm()
        context={
            'students': students,
            'form': form,
            }
        return render(request, 'lesson_class_initiation.html', context)

@teacher_required
def lesson_conducting(request, current_lesson_report_id):
    context={

    }
    return render(request, 'lesson_conducting.html', context)