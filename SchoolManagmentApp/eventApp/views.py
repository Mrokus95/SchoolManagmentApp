from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from eventApp.models import CalendarEvents, Teacher
from eventApp.forms import EventFilterForm
from usersApp.models import Profile


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
            record.finished = True
            record.save()


def show_events(request):

    current_profile = Profile.objects.get(user=request.user)
    account_type = current_profile.account_type

    if account_type == Profile.STUDENT or account_type == Profile.PARENT:
        current_student = current_profile.student
        current_class = current_student.class_unit

        if CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).exists():
            events = CalendarEvents.objects.filter(connected_to_lesson__class_unit=current_class).order_by('realisation_time')

            event_status_changer(events)

            filter_form = EventFilterForm()
            if request.method == 'GET':
                paginator = Paginator(events, 6)
                page_number = request.GET.get('page')
                pages = paginator.get_page(page_number)
                context = {
                'pages': pages,
                'filter': filter_form
                }
                return render(request, 'events.html', context) 
                      
            else:
                start_date_condition=request.POST.get('start_date')
                end_date_condition=request.POST.get('end_date')

                if start_date_condition > end_date_condition:
                    messages.error(request,"End date must be after start date!")                
                    paginator = Paginator(events, 6)
                    page_number = request.GET.get('page')
                    pages = paginator.get_page(page_number)
                    context = {
                    'pages': pages,
                    'filter': filter_form
                        }
                    return render(request, 'events.html', context)
                           
                else:
                    filtred=events_filter(request, events)
                    paginator = Paginator(filtred, 6)
                    page_number = request.GET.get('page')
                    pages = paginator.get_page(page_number)               
                    context = {
                        'pages': pages,
                        'filter': filter
                        }
                return render(request, 'events.html', context)
            
        else:
            messages.error(request, 'No events!')
            return render(request, 'events.html')
        
    else:
        current_teacher = Teacher.objects.get(user=current_profile)

        if CalendarEvents.objects.filter(author=current_teacher).exists():

            events = CalendarEvents.objects.filter(author=current_teacher)

            event_status_changer(events)

                #tutaj musi być nowy filtr dla nauczyciela i rozwinięcie filtra

            if request.method == 'GET':
                paginator = Paginator(events, 6)
                page_number = request.GET.get('page')
                pages = paginator.get_page(page_number)
            context = {
            'pages': pages,
                
            }
            return render(request, 'events.html', context)

        else:
            messages.error(request, 'No events!')
            return render(request, 'events.html')


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