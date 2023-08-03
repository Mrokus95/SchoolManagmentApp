from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from eventApp.models import CalendarEvents, Teacher
from eventApp.forms import EventFilterStudentForm, AddEvent
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

    if CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).exists():
        events = CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).order_by('realisation_time')
        event_status_changer(events)  
        filter_form = EventFilterStudentForm()

        if request.method == 'GET':
            pages = event_paginator(request, events, 6)
    
            context = {
            'pages': pages,
            'kid_id': kid_id,
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
    if CalendarEvents.objects.filter(id=eventId).exists():
        event = CalendarEvents.objects.get(id=eventId)
        event.visited = True
        event.save()
        return render(request, 'event_detail.html', {'event': event})
    else:
        messages.error(
        request, 'Event cannot be viewd, please contact the author!')
        return redirect('events')
    
def teacher_event_detail(request, eventId):
    curret_profile = Profile.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(user=request.user.profile)

    if curret_profile.account_type == Profile.TEACHER:

        if CalendarEvents.objects.filter(author=current_teacher).exists():
            event = CalendarEvents.objects.get(id=eventId)
            return render(request, 'teacher_event_details.html', {'event': event})
        
        else:    
            messages.error(request, 'Event cannot be viewd!')
            return render(request, 'teacher_event_details.html')
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
        
def delete_event(request, eventId):

    if CalendarEvents.objects.get(id=eventId):
        event = CalendarEvents.objects.get(id=eventId)
        event.delete()
        messages.success(request, 'Event deleted!')
        return redirect('teacher_events')

    else:
        messages.error(request, 'Problem with deleting!')
        return redirect('teacher_events')
    
def edit_event(request, eventId):
    edited_event = CalendarEvents.objects.get(id=eventId)
    connected_to_lesson = edited_event.connected_to_lesson

    if request.method == 'GET':
        edit_form = AddEvent(instance=edited_event)    
        context={'edit_form': edit_form,
                 'connected_to_lesson' : connected_to_lesson}
        return render(request, 'edit_event.html', context)
    
    else:
        edited_form = AddEvent(request.POST, instance=edited_event)

        if edited_form.is_valid():
            edited_form.save()
            edited_event.visited = False
            edited_event.save()
            messages.success(request, "Event changed!")
            return redirect ('teacher_events')
        
        else:
            errors = edited_form.errors
            return render(request, 'add_event.html', {'errors': errors})
