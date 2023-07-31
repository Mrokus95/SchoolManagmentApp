from django.shortcuts import render
from django.views.generic import CreateView
from .models import Lesson
from .forms import LessonForm

class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'create_lesson.html'
    success_url = 'inbox'
