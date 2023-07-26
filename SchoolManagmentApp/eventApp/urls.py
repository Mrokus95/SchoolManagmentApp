from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns =[

    # main events
    path('events/', views.show_events, name='events'),
    path('event_detail/<int:eventId>/', views.event_detail, name='event_detail'),

    # filter events
    path('filter_events_student/', views.student_events, name='filter_events_student'),
    path('filter_events_student_parent', views.parent_events,name='filter_events_student_parent'),

    path('parent/filter_events/', views.parent_events, name='parent_filter_events'),

    #profile for student by parent
    path('events/student/<int:kid_id>', views.chosen_profile, name='student_events'),
]