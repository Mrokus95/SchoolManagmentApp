from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from .models import Lesson
from .forms import LessonForm
from datetime import datetime, timedelta

def get_weekdays(date):
    today = date
    current_weekday = today.weekday()

    dates = {i: today + timedelta(days=i-current_weekday) for i in range(7)}


    return dates

class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'create_lesson.html'
    success_url = 'inbox'

def view_schedule(request, class_id=None, week_offset=0):
    if class_id is None:
        class_id = 11

   
    date = datetime.now().date() + timedelta(weeks=week_offset)
    
    week_dates = get_weekdays(date)

    lessons = Lesson.objects.filter(class_name=class_id)

    monday_lessons = lessons.filter(day_of_week=1).order_by('lesson_number')
    thusday_lessons = lessons.filter(day_of_week=2).order_by('lesson_number')
    wednesday_lessons = lessons.filter(day_of_week=3).order_by('lesson_number')
    thursday_lessons = lessons.filter(day_of_week=4).order_by     ('lesson_number')
    friday_lessons = lessons.filter(day_of_week=5).order_by('lesson_number')





    context={
        'range': range(1,6),
        'class_id': class_id,
        'monday_lessons':monday_lessons,
        'thusday_lessons':thusday_lessons,
        'wednesday_lessons':wednesday_lessons,
        'thursday_lessons':thursday_lessons,
        'friday_lessons':friday_lessons
    }

    return render(request, 'view_schedule.html', context)