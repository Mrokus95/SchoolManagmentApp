from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns =[

    # main events
    path('events/', views.show_events, name='events'),

    # filter events
    path('filter_events_student/', views.student_events, name='filter_events_student'),
    path('filter_events_student_parent/<int:kid_id>', views.parent_events_viewing,name='filter_events_student_parent'),
    path('teacher_events/', views.teacher_events, name='teacher_events'),

    #details events
    path('event_detail/<int:eventId>/', views.event_detail, name='event_detail'),
    path('teacher_event_details/<int:eventId>/', views.teacher_event_detail, name='teacher_event_detail'),

    #parent_redirect_if_kids
    path('parent/filter_events/', views.parent_events, name='parent_filter_events'),

    #delete event
    path('delete_event/<int:eventId>', views.delete_event, name='delete_event'),

    #edit event
    path('edit_event/<int:eventId>', views.edit_event, name='edit_event'),


    

]