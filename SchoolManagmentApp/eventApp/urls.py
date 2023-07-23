from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns =[
    path('events', views.show_events, name='events'),
    path('wydarzenie/<int:eventId>/', views.event_detail, name='event_detail')
]