from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from eventApp.models import CalendarEvents, Teacher
from eventApp.forms import EventFilterStudentForm
from usersApp.models import Profile, Student, Parent


from datetime import date

# Create your views here.

def events_student_filter(request, queryset):


    subject_condition = request.POST.get('subject')
    type_condition = request.POST.get('event_type')
    start_date_condition=request.POST.get('start_date')
    end_date_condition=request.POST.get('end_date')

    if subject_condition != 'empty':
        queryset = queryset.filter(subject__name=subject_condition)
         
    if type_condition != 'empty':
        queryset = queryset.filter(event_type=type_condition)
       
    if start_date_condition:
        queryset = queryset.filter(realisation_time__gte=start_date_condition)

    if end_date_condition:
        queryset = queryset.filter(realisation_time__lt=end_date_condition)

    return queryset

def event_status_changer(events_to_change):
    for record in events_to_change:
        if record.realisation_time < date.today():
            record.finished= True
            record.save()

def event_paginator(request, events_to_paginate, events_per_site):
    paginator = Paginator(events_to_paginate, events_per_site)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    return pages

def date_filter_validation(request):
    return request.POST.get('start_date') > request.POST.get('end_date')

def student_events(request):

    current_student = Student.objects.get(user=request.user.profile)
    current_class = current_student.class_unit
    
    if CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).exists():
        events = CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).order_by('realisation_time')
        event_status_changer(events)
        filter_form = EventFilterStudentForm()

        if request.method == 'GET':
            pages = event_paginator(request, events, 6)
            context = {
            'pages': pages,
            'filter': filter_form,
            'current_class': current_class
            }
            return render(request, 'events.html', context) 
                      
        else:
            if date_filter_validation(request):
                messages.error(request,"End date must be set after start date!")
                pages = event_paginator(request, events, 6)
                context = {
                'pages': pages,
                'filter': filter_form
                    }
                return render(request, 'events.html', context)
                           
            else:
                filtred=events_student_filter(request, events)
                pages = event_paginator(request, filtred, 6)               
                context = {
                    'pages': pages,
                    'filter': filter_form,
                    'current_class': current_class
                        }
            return render(request, 'events.html', context)
            
    else:
        messages.error(request, 'No events!')
        return render(request, 'events.html')

def teacher_events(request):
    current_teacher = Teacher.objects.get(user=request.user.profile)

    if CalendarEvents.objects.filter(author=current_teacher).exists():
        events = CalendarEvents.objects.filter(author=current_teacher)
        filter_form = EventFilterStudentForm()

        if request.method == 'GET':
            pages = event_paginator(request, events, 6)
            context = {
            'pages': pages,
            'filter': filter_form,                
            }
            return render(request, 'teacher_events.html', context)
    
        else:
            if date_filter_validation(request):
                messages.error(request,"End date must be set after start date!")
                pages = event_paginator(request, events, 6)
                context = {
                'pages': pages,
                'filter': filter_form,
                    }
                return render(request, 'teacher_events.html', context)
            
            else:
                filtred=events_student_filter(request, events)
                pages = event_paginator(request, filtred, 6)               
                context = {
                    'pages': pages,
                    'filter': filter_form,
                        }
            return render(request, 'teacher_events.html', context)
    else:
        messages.error(request, 'No events!')
        return render(request, 'events.html')

def parent_events_viewing(request, kid_id):

    kid_profile = Student.objects.get(id=kid_id)
    current_class = kid_profile.class_unit

    print(kid_id, kid_profile, current_class)
    if CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).exists():
        events = CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).order_by('realisation_time')
        event_status_changer(events)
    
        filter_form = EventFilterStudentForm()
        print(request.method)

        if request.method == 'GET':
            pages = event_paginator(request, events, 6)
            print('jestem w get')
            context = {
            'pages': pages,
            'kid_id': kid_id,
            'filter': filter_form,
            'current_class': current_class
            }
    
            return render(request, 'events.html', context) 
                      
        else:
            print('jestem w post')
            if date_filter_validation(request):
                messages.error(request,"End date must be set after start date!")
                pages = event_paginator(request, events, 6)
                context = {
                'pages': pages,
                'filter': filter_form,
                'filter': filter_form,
                'current_class': current_class
                    }
                return render(request, 'events.html', context)
                           
            else:
                filtred=events_student_filter(request, events)
                pages = event_paginator(request, filtred, 6)               
                context = {
                'pages': pages,
                'filter': filter_form,
                'current_class': current_class
                    }
                return render(request, 'events.html', context)
    else:
        messages.error(request, 'No events!')
        return render(request, 'events.html')   

def parent_events(request, kid_profile=None):
    print('jesem w parent event')
    current_parent = Parent.objects.get(user=request.user.profile)

    if not kid_profile:
          
        parent_kids = Student.objects.filter(parent=current_parent)
        if len(parent_kids) > 1:
            return render(request, 'events.html',{'parent_kids': parent_kids})
    
        else:
            kid_profile = parent_kids.first()
            
    return parent_events_viewing(request, kid_profile) 

def show_events(request):
    current_profile = Profile.objects.get(user=request.user)
    account_type = current_profile.account_type

    if account_type == Profile.STUDENT:
        return student_events(request)
       
    elif account_type == Profile.PARENT:
        return parent_events(request)

    else:
        return teacher_events(request)

def event_detail(request, eventId):
    curret_profile = Profile.objects.get(user=request.user)
    print(curret_profile)
    current_teacher = Teacher.objects.get(user=request.user.profile)
    print(current_teacher)

    if curret_profile.account_type == Profile.TEACHER:

        if CalendarEvents.objects.filter(author=current_teacher).exists():
            event = CalendarEvents.objects.get(id=eventId)
            return render(request, 'teacher_event_details.html', {'event': event})
    else:

        if CalendarEvents.objects.filter(id=eventId).exists():
            event = CalendarEvents.objects.get(id=eventId)
            event.visited = True
            event.save()
            return render(request, 'event_detail.html', {'event': event})
        else:
            messages.error(
            request, 'Event cannot be viewd, please contact the author!')
            return redirect('events')