from django.urls import path
from .views import view_schedule

urlpatterns = [
    path('', view_schedule, name='view_schedule_default'),
    path('<int:class_id>/', view_schedule, name='view_schedule_default'),
    path('<int:class_id>/<int:week_offset>', view_schedule, name='view_schedule'),
 
]