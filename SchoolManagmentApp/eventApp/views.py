from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from eventApp.models import CalendarEvents, Teacher
from eventApp.forms import EventFilterForm
from usersApp.models import Profile, Student, Parent


from datetime import date

# Create your views here.

def events_filter(request, queryset):
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

def chosen_profile(request, kid_id):
    print(kid_id)
    student = Student.objects.get(pk=kid_id)
    kid_profile = student.user

    return student_events(request, kid_profile)

def student_events(request, current_profile):
    current_student = Student.objects.get(user=current_profile)
    current_class = current_student.class_unit

    if CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).exists():
        events = CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).order_by('realisation_time')
        event_status_changer(events)
        filter_form = EventFilterForm()

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
                filtred=events_filter(request, events)
                pages = event_paginator(request, filtred, 6)               
                context = {
                    'pages': pages,
                    'filter': filter_form
                        }
            return render(request, 'events.html', context)
            
    else:
        messages.error(request, 'No events!')
        return render(request, 'events.html')

def teacher_events(request, current_profile):
    current_teacher = Teacher.objects.get(user=current_profile)

    if CalendarEvents.objects.filter(author=current_teacher).exists():
        events = CalendarEvents.objects.filter(author=current_teacher)
        event_status_changer(events)

                #tutaj musi być nowy filtr dla nauczyciela i rozwinięcie filtra

        if request.method == 'GET':
            pages = event_paginator(request, events, 6)

            context = {
            'pages': pages,
                
            }
        return render(request, 'events.html', context)
        # if metoda post
    else:
        messages.error(request, 'No events!')
        return render(request, 'events.html')

def parent_events(request, current_profile):
    current_parent = Parent.objects.get(user=current_profile)
    parent_kids = Student.objects.filter(parent=current_parent)
   

    if len(parent_kids) > 1:
        return render(request, 'events.html',{'parent_kids': parent_kids})
    
    else:
        kid_profile = Profile.objects.get(user=parent_kids.first().user.user)
        return student_events(request, kid_profile)

def show_events(request):
    current_profile = Profile.objects.get(user=request.user)
    account_type = current_profile.account_type

    if account_type == Profile.STUDENT:
        return student_events(request, current_profile)
       
    elif account_type == Profile.PARENT:
        return parent_events(request, current_profile)

    else:
        return teacher_events(request, current_profile)


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