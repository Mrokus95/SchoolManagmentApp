from django.urls import path
from .views import LessonCreateView

urlpatterns = [
    path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
]