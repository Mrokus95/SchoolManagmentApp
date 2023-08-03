from django.shortcuts import render, redirect, reverse
from usersApp.models import Profile, Student
from eventApp.forms import AddEvent
from eventApp.models import LessonReport, CalendarEvents, Subject, Attendance, Teacher
from django.contrib import messages
from eventApp.views import event_paginator, student_events
from .forms import LessonRportFilter, ClassSubjectChoiceForm, AttendanceForm, LessonReportText
from usersApp.models import ClassUnit
from datetime import date



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
       
        lesson_report = LessonReport.objects.get_or_create(
            create_date=date.today(),
            subject=selected_subject,
            teacher=current_teacher,
            class_unit=selected_class.first(),
            lesson_title='Initial Title',
            lesson_description = 'Initial Description',
        )
        lesson_report = lesson_report[0]
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
    current_class = current_lesson_report.class_unit

    if request.method == 'POST':

        for participant in students:

            if not Attendance.objects.filter(
                lesson_report=current_lesson_report,
                student=participant.id,
                is_present__in=[True, False]
                ).exists():
                attendance_object = Attendance.objects.create(
                    lesson_report = current_lesson_report,
                    student = participant,
                    is_present=request.POST.get(str(participant.id), False) == 'True'
                    )
        messages.success(request, "Attendance checked!")
        return redirect('lesson_conducting', current_lesson_report.id)
        
    else:
        form = AttendanceForm()
        context={
            'students': students,
            'form': form,
            'current_class': current_class
            }
        return render(request, 'lesson_class_initiation.html', context)

@teacher_required
def lesson_conducting(request, current_lesson_report_id):
    current_lesson_report = LessonReport.objects.get(id=current_lesson_report_id)
    initial_data = {
        'lesson_title' : current_lesson_report.lesson_title,
        'lesson_description' : current_lesson_report.lesson_description,
            }
    lesson_report_text = LessonReportText(initial=initial_data)

    if request.method=='POST':
        updated_form = LessonReportText(request.POST, instance=current_lesson_report)

        if updated_form.is_valid():
            updated_form.save()
            messages.success(request, "Raport finalized!")
            return redirect ('teacher_events')

        else:
            errors = updated_form.errors
            context={
                'lesson_report_text': lesson_report_text,
                'current_lesson_report': current_lesson_report,
                'errors': errors
                    }
            return render(request, 'lesson_conducting.html', context)
        
    else:    
        context={
            'lesson_report_text': lesson_report_text,
            'current_lesson_report': current_lesson_report,
                }
    
        return render(request, 'lesson_conducting.html', context)

@teacher_required    
def add_event(request, current_lesson_report_id):
    current_lesson_report = LessonReport.objects.get(id=current_lesson_report_id)
    add_event_form = AddEvent()
    curret_teacher = Teacher.objects.get(user=request.user.profile)

    if request.method == 'GET':
        context = {
            'add_event_form': add_event_form,
            'current_lesson_report': current_lesson_report,
        }
        return render(request, 'add_event.html', context)

    else:
        adding_form = AddEvent(request.POST)

        if adding_form.is_valid():
            form = adding_form.save(commit=False)
            if form.realisation_time <= date.today():
                messages.error(request, 'Ralisation date must be past today')
                return redirect('add_event', current_lesson_report.id )
            
            else:
                form.author = curret_teacher
                form.subject = current_lesson_report.subject
                form.connected_to_lesson = current_lesson_report
                form.save()
                messages.success(request, "Event added successfully!")
                return redirect ('lesson_conducting', current_lesson_report.id)
        
        else:
            errors = adding_form.errors
            return render(request, 'add_event.html', {'errors': errors})