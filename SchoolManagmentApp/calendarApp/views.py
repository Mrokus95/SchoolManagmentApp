from django.shortcuts import render
from .models import Lesson
from datetime import datetime, timedelta

def get_weekdays(date):
    today = date
    current_weekday = today.weekday()

    dates = {i: today + timedelta(days=i-current_weekday) for i in range(7)}

    return dates

def check_exceptions(lessons, exceptions):
    for lesson_exception in exceptions:
        for lesson in lessons:
            if lesson is not None and lesson.lesson_number == lesson_exception.lesson_number:
                lessons = list(lessons)
                lessons[lessons.index(lesson)] = lesson_exception
                break
    return lessons


def get_lessons_for_day(lessons, day_of_week_no, lesson_date): 

    monday_lessons = list(lessons.filter(day_of_week=day_of_week_no, is_base=True).order_by('-date', 'lesson_number'))

    # Create a dict with unique/newest lessons 
    unique_lessons_dict = {}
    for lesson in monday_lessons:
        if lesson.lesson_number not in unique_lessons_dict:
            unique_lessons_dict[lesson.lesson_number] = lesson

    # We convert the dictionary back into a list to get the final result correct data type
    unique_lessons_list = list(unique_lessons_dict.values())

    # Sorted by lesson number due to keep logic in html template 
    unique_lessons_list.sort(key=lambda x: x.lesson_number)

    monday_lessons = unique_lessons_list

    lesson_list = [None] * 8

    for lesson in monday_lessons:
        lesson_number = lesson.lesson_number
        lesson_list[lesson_number - 1] = lesson

    monday_lessons_exceptions = list(lessons.filter(day_of_week=day_of_week_no, is_base=False, date=lesson_date).order_by('lesson_number'))

    return check_exceptions(lesson_list,monday_lessons_exceptions)

def view_schedule(request, class_id=None, week_offset=None):
    if week_offset is None:
        week_offset = 0
    
    
    if class_id is None:
        class_id = 11

   
    date = datetime.now().date() + timedelta(weeks=week_offset)
    
    week_dates = get_weekdays(date)

# Get all lessons for class
    lessons = Lesson.objects.filter(class_name=class_id, date__lte=week_dates[4])

    monday_lessons= get_lessons_for_day(lessons, 1, week_dates[0])
    thusday_lessons= get_lessons_for_day(lessons, 2, week_dates[1])
    wednesday_lessons= get_lessons_for_day(lessons, 3, week_dates[2])
    thursday_lessons= get_lessons_for_day(lessons, 4, week_dates[3])
    friday_lessons= get_lessons_for_day(lessons, 5, week_dates[4])

    context={
        'class_id': class_id,
        'days': [("Monday",monday_lessons),
                 ("Thusday",thusday_lessons),
                 ("Wednesday",wednesday_lessons),
                 ("Thursday",thursday_lessons),
                 ("Friday",friday_lessons)]
    }

    return render(request, 'view_schedule.html', context)