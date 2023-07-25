from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from eventApp.models import CalendarEvents
from eventApp.forms import EventFilterForm


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



def show_events(request):

    if CalendarEvents.objects.all().exists():
        events = CalendarEvents.objects.all().order_by('realisation_time')
        
        for event in events:
            if event.realisation_time < date.today():
                    event.finished = True
                    event.save()


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
            filtred=events_filter(request, events)

            # print('to jest po funkcji filtred:', events_filter(request, events))

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