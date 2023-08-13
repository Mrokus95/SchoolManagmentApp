import calendar
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from eventApp.models import Subject, Teacher
from messagesApp.models import Message
from usersApp.models import ClassUnit, Profile, Student
from .forms import ClassUnitForm, EditLessonForm, LessonForm
from .models import ClassroomReservation, Lesson, TeacherReservation


def teachers(request, subject_id):
    try:
        subject = Subject.objects.get(pk=subject_id)
        teachers = Teacher.objects.filter(lesson_type=subject)
        teacher_data = [
            {"id": teacher.id, "name": str(teacher)} for teacher in teachers
        ]
        return JsonResponse(teacher_data, safe=False)
    except Subject.DoesNotExist:
        return JsonResponse({"error": "Subject not found"}, status=404)


def get_weekdays(date):
    today = date
    current_weekday = today.weekday()

    dates = {i: today + timedelta(days=i - current_weekday) for i in range(7)}

    return dates


def check_exceptions(lessons, exceptions):
    for lesson_exception in exceptions:
        for no, lesson in enumerate(lessons):
            if (
                lesson is not None
                and lesson.lesson_number == lesson_exception.lesson_number
            ):
                index = lessons.index(lesson)
                lessons[index] = lesson_exception
                break
            elif lesson is None and lesson_exception.lesson_number == no + 1:
                index = lessons.index(None, no)
                lessons[index] = lesson_exception
    return lessons


def get_lessons_for_day(lessons, day_of_week_no, lesson_date):
    monday_lessons = list(
        lessons.filter(day_of_week=day_of_week_no, is_base=True).order_by(
            "-date", "lesson_number"
        )
    )

    unique_lessons_dict = {}
    for lesson in monday_lessons:
        if lesson.lesson_number not in unique_lessons_dict:
            unique_lessons_dict[lesson.lesson_number] = lesson

    unique_lessons_list = list(unique_lessons_dict.values())

    unique_lessons_list.sort(key=lambda x: x.lesson_number)

    monday_lessons = unique_lessons_list

    lesson_list = [None] * 8

    for lesson in monday_lessons:
        lesson_number = lesson.lesson_number
        lesson_list[lesson_number - 1] = lesson

    monday_lessons_exceptions = list(
        lessons.filter(
            day_of_week=day_of_week_no, is_base=False, date=lesson_date
        ).order_by("lesson_number")
    )
    return check_exceptions(lesson_list, monday_lessons_exceptions)


@login_required
def view_schedule(request, class_id=None, week_offset=None):
    if not week_offset:
        week_offset = 0
        date = datetime.now().date()

    else:
        week_offset = int(week_offset)
        if week_offset < -8:
            messages.error(request, 
                           "Too far away. 8 weeks in past is maximum offset.")
            week_offset = -8
        elif week_offset > 8:
            messages.error(
                request, "Too far away. 8 weeks in future is maximum offset."
            )
            week_offset = 8
        else:
            pass

        if week_offset > 0:
            date = datetime.now().date() + timedelta(weeks=week_offset)
        elif week_offset < 0:
            date = datetime.now().date() - timedelta(weeks=abs(week_offset))
        else:
            week_offset = 0
            date = datetime.now().date() + timedelta(weeks=week_offset)

    if class_id is None:
        try:
            if request.user.profile.account_type == "Teacher":
                class_id = ClassUnit.objects.last()
            elif request.user.profile.account_type == "Student":
                class_id = request.user.profile.student.class_unit
            elif request.user.profile.account_type == "Parent":
                parent_profile = request.user.profile.parent
                student = Student.objects.filter(parent=parent_profile).first()
                if student:
                    class_id = student.class_unit
            else:
                class_id = ClassUnit.objects.last()
        except AttributeError:
            class_id = ClassUnit.objects.last()
    else:
        class_id = get_object_or_404(ClassUnit.objects.filter(id=class_id))

    if request.method == "GET":
        week_dates = get_weekdays(date)

        lessons = Lesson.objects.filter(class_name=class_id, 
                                        date__lte=week_dates[4])

        monday_lessons = get_lessons_for_day(lessons, 1, week_dates[0])
        thusday_lessons = get_lessons_for_day(lessons, 2, week_dates[1])
        wednesday_lessons = get_lessons_for_day(lessons, 3, week_dates[2])
        thursday_lessons = get_lessons_for_day(lessons, 4, week_dates[3])
        friday_lessons = get_lessons_for_day(lessons, 5, week_dates[4])

        form = ClassUnitForm()

        context = {
            "week_offset": week_offset,
            "start_date": week_dates[0],
            "end_date": week_dates[4],
            "class_id": class_id,
            "form": form,
            "days": [
                ("Monday", monday_lessons),
                ("Thusday", thusday_lessons),
                ("Wednesday", wednesday_lessons),
                ("Thursday", thursday_lessons),
                ("Friday", friday_lessons),
            ],
        }

        return render(request, "view_schedule.html", context)
    else:
        form = ClassUnitForm(request.POST)

        if form.is_valid():
            class_id = form.cleaned_data["class_unit"].id
            return redirect("view_schedule", class_id=class_id, 
                            week_offset=week_offset)


@staff_member_required
def create_lesson(
    request, class_id=None, date=None, lesson_number=None, week_offset=None
):
    if request.method == "GET":
        class_unit = get_object_or_404(ClassUnit, id=class_id) \
            if class_id else None

        lesson_form = LessonForm()

        context = {
            "form": lesson_form,
            "class_unit": class_unit,
            "date": date,
            "lesson_number": lesson_number,
        }
        return render(request, "create_lesson.html", context)

    if request.method == "POST":
        class_unit = get_object_or_404(ClassUnit, id=class_id) \
            if class_id else None
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_of_week_int = date_obj.weekday() + 1

        form = LessonForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            day_of_week = day_of_week_int
            lesson_number = lesson_number
            teacher = form.cleaned_data["teacher"]
            class_name = class_unit
            classroom = form.cleaned_data["classroom"]
            date = date_obj
            is_base = form.cleaned_data["is_base"]

            if is_base:
                classroom_reservation_exists = \
                    ClassroomReservation.objects.filter(
                    start_date__gte=date,
                    classroom=classroom,
                    day_of_week=day_of_week,
                    lesson_number=lesson_number,
                ).exists()

                pre_base_classroom_reservation_exists = (
                    ClassroomReservation.objects.filter(
                        start_date__lt=date,
                        classroom=classroom,
                        day_of_week=day_of_week,
                        lesson_number=lesson_number,
                        end_date=None,
                    ).exists()
                )

                not_base_classroom_reservation_exists = (
                    ClassroomReservation.objects.filter(
                        start_date=date,
                        classroom=classroom,
                        day_of_week=day_of_week,
                        lesson_number=lesson_number,
                        end_date=date,
                    ).exists()
                )

                teacher_reservation_exists = \
                    TeacherReservation.objects.filter(
                    start_date__gte=date,
                    teacher=teacher,
                    day_of_week=day_of_week,
                    lesson_number=lesson_number,
                ).exists()

                pre_base_teacher_reservation_exists = \
                    TeacherReservation.objects.filter(
                    start_date__lt=date,
                    teacher=teacher,
                    day_of_week=day_of_week,
                    lesson_number=lesson_number,
                    end_date=None,
                ).exists()

                not_base_teacher_reservation_exists = \
                    TeacherReservation.objects.filter(
                    start_date=date,
                    teacher=teacher,
                    day_of_week=day_of_week,
                    lesson_number=lesson_number,
                    end_date=date,
                ).exists()

            else:
                classroom_reservation_exists = \
                    ClassroomReservation.objects.filter(
                    Q(start_date__lte=date)
                    & (Q(end_date__gte=date) | Q(end_date=None)),
                    classroom=classroom,
                    day_of_week=day_of_week,
                    lesson_number=lesson_number,
                ).exists()

                not_base_classroom_reservation_exists = (
                    ClassroomReservation.objects.filter(
                        start_date=date,
                        classroom=classroom,
                        day_of_week=day_of_week,
                        lesson_number=lesson_number,
                        end_date=date,
                    ).exists()
                )

                pre_base_classroom_reservation_exists = False
                pre_base_teacher_reservation_exists = False

                teacher_reservation_exists = TeacherReservation.objects.filter(
                    Q(start_date__lte=date)
                    & (Q(end_date__gte=date) | Q(end_date=None)),
                    teacher=teacher,
                    day_of_week=day_of_week,
                    lesson_number=lesson_number,
                ).exists()

                not_base_teacher_reservation_exists = \
                    TeacherReservation.objects.filter(
                    start_date=date,
                    teacher=teacher,
                    day_of_week=day_of_week,
                    lesson_number=lesson_number,
                    end_date=date,
                ).exists()

            if (
                not teacher_reservation_exists
                and not pre_base_teacher_reservation_exists
                and not not_base_teacher_reservation_exists
            ):
                if (
                    not classroom_reservation_exists
                    and not pre_base_classroom_reservation_exists
                    and not not_base_classroom_reservation_exists
                ):
                    try:
                        with transaction.atomic():
                            if is_base:
                                new_reservation = \
                                    ClassroomReservation.objects.create(
                                    classroom=classroom,
                                    day_of_week=day_of_week,
                                    lesson_number=lesson_number,
                                    start_date=date,
                                    class_unit=class_name,
                                )

                                new_teacher_reservation = (
                                    TeacherReservation.objects.create(
                                        teacher=teacher,
                                        day_of_week=day_of_week,
                                        lesson_number=lesson_number,
                                        start_date=date,
                                        class_unit=class_name,
                                    )
                                )

                            else:
                                new_reservation = \
                                    ClassroomReservation.objects.create(
                                    classroom=classroom,
                                    day_of_week=day_of_week,
                                    lesson_number=lesson_number,
                                    start_date=date,
                                    end_date=date,
                                    class_unit=class_name,
                                )

                                new_teacher_reservation = (
                                    TeacherReservation.objects.create(
                                        teacher=teacher,
                                        day_of_week=day_of_week,
                                        lesson_number=lesson_number,
                                        start_date=date,
                                        end_date=date,
                                        class_unit=class_name,
                                    )
                                )

                            Lesson.objects.create(
                                subject=subject,
                                day_of_week=day_of_week,
                                lesson_number=lesson_number,
                                teacher=teacher,
                                class_name=class_name,
                                classroom=classroom,
                                date=date,
                                is_base=is_base,
                                is_cancelled=False,
                                classroom_reservation=new_reservation,
                                teacher_reservation=new_teacher_reservation,
                            )

                            sender_profile = \
                                Profile.objects.get(user=request.user)

                            students = class_name.students_in_class.all()
                            date_str = date.strftime("%Y-%m-%d")
                            day_of_week_str = calendar.day_name[day_of_week]

                            for student in students:
                                receiver = student.user
                                title = "New lesson for your class"
                                body = f"""There is a new lesson for your class in schedule:

                                    Subject: {subject}
                                    Teacher: {teacher}
                                    Classroom: {classroom}
                                    When: {day_of_week_str} lesson no. {lesson_number}
                                    Date: {date_str}

                                    Please check your schedule for more information.
                                """
                                Message.objects.create(
                                    sender=sender_profile,
                                    receiver=receiver,
                                    title=title,
                                    body=body,
                                )

                            messages.success(request, 
                                             "Lesson created successfully")

                            return redirect(
                                "view_schedule",
                                class_id=class_id,
                                week_offset=week_offset,
                            )
                    except:
                        messages.error(
                            request,
                            "Occured an error while creating - \
                                please check data and try again.",
                        )
                        return redirect(
                            "view_schedule", class_id=class_id, 
                            week_offset=week_offset
                        )
                else:
                    messages.error(
                        request, "Classroom is curently \
                            reserved for this date."
                    )
                    return redirect(
                        "view_schedule", class_id=class_id, 
                        week_offset=week_offset
                    )
            else:
                messages.error(request, "Teacher is curently \
                               reserved for this date.")
                return redirect(
                    "view_schedule", class_id=class_id, 
                    week_offset=week_offset
                )
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)

            return redirect(".")


@staff_member_required
def edit_lesson(request, lesson_id, date=None, week_offset=None):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    current_classroom_reservation = lesson.classroom_reservation
    current_teacher_reservation = lesson.teacher_reservation
    if request.method == "GET":
        initial_data = {
            "subject": lesson.subject,
            "teacher": lesson.teacher,
            "class_name": lesson.class_name,
            "classroom": lesson.classroom,
            "is_base": lesson.is_base,
            "is_canceled": lesson.is_cancelled,
        }
        lesson_form = EditLessonForm(initial=initial_data)

        context = {
            "form": lesson_form,
            "class_unit": lesson.class_name,
            "date": date,
            "lesson_number": lesson.lesson_number,
        }
        return render(request, "edit_lesson.html", context)

    if request.method == "POST":
        form = EditLessonForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            day_of_week = lesson.day_of_week
            lesson_number = lesson.lesson_number
            teacher = form.cleaned_data["teacher"]
            class_name = lesson.class_name
            classroom = form.cleaned_data["classroom"]
            date = date
            is_base = form.cleaned_data["is_base"]
            is_cancelled = form.cleaned_data["is_cancelled"]

            if (
                lesson.is_base
                or lesson.classroom != classroom
                or lesson.teacher != teacher
            ):
                if is_base:
                    try:
                        with transaction.atomic():
                            current_classroom_reservation.end_date = date
                            current_classroom_reservation.save()

                            current_teacher_reservation.end_date = date
                            current_teacher_reservation.save()

                            classroom_reservation_exists = (
                                ClassroomReservation.objects.filter(
                                    (Q(start_date__gt=date) | Q(start_date__lte=date)),
                                    classroom=classroom,
                                    day_of_week=day_of_week,
                                    lesson_number=lesson_number,
                                    end_date=None,
                                )
                            )

                            if classroom_reservation_exists:
                                if (
                                    classroom_reservation_exists.count() == 1
                                    and classroom_reservation_exists[0]
                                    == current_classroom_reservation
                                ):
                                    classroom_reservation_exists = False

                            teacher_reservation_exists = (
                                TeacherReservation.objects.filter(
                                    (Q(start_date__gt=date) | Q(start_date__lte=date)),
                                    teacher=teacher,
                                    day_of_week=day_of_week,
                                    lesson_number=lesson_number,
                                    end_date=None,
                                )
                            )

                            if teacher_reservation_exists:
                                if (
                                    teacher_reservation_exists.count() == 1
                                    and teacher_reservation_exists[0]
                                    == current_teacher_reservation
                                ):
                                    teacher_reservation_exists = False

                            if not teacher_reservation_exists:
                                if not classroom_reservation_exists:
                                    classrooom_new_reservation = (
                                        ClassroomReservation.objects.create(
                                            classroom=classroom,
                                            day_of_week=day_of_week,
                                            lesson_number=lesson_number,
                                            start_date=date,
                                            class_unit=class_name,
                                        )
                                    )

                                    teacher_new_reservation = (
                                        TeacherReservation.objects.create(
                                            teacher=teacher,
                                            day_of_week=day_of_week,
                                            lesson_number=lesson_number,
                                            start_date=date,
                                            class_unit=class_name,
                                        )
                                    )

                                    lesson = Lesson.objects.create(
                                        subject=subject,
                                        day_of_week=day_of_week,
                                        lesson_number=lesson_number,
                                        teacher=teacher,
                                        class_name=class_name,
                                        classroom=classroom,
                                        date=date,
                                        is_base=is_base,
                                        is_cancelled=is_cancelled,
                                        classroom_reservation=classrooom_new_reservation,
                                        teacher_reservation=teacher_new_reservation,
                                    )

                                    sender_profile = Profile.objects.get(
                                        user=request.user
                                    )

                                    students = \
                                        class_name.students_in_class.all()
                                    date_str = date.strftime("%Y-%m-%d")
                                    day_of_week_str = \
                                        calendar.day_name[day_of_week]

                                    for student in students:
                                        receiver = student.user
                                        title = "New lesson for your class"
                                        body = f"""There is a change in your schedule. Currently your {lesson_number} lesson on {day_of_week_str} ({date_str}) will be:

                                        Subject: {subject}
                                        Teacher: {teacher}
                                        Classroom: {classroom}

                                        Please check your schedule for more information.
                                        """
                                        Message.objects.create(
                                            sender=sender_profile,
                                            receiver=receiver,
                                            title=title,
                                            body=body,
                                        )

                                    messages.success(
                                        request, "Lesson edited successfully"
                                    )
                                    return redirect(
                                        "view_schedule",
                                        class_id=class_name.id,
                                        week_offset=week_offset,
                                    )
                                else:
                                    messages.error(
                                        request, "Classroom is curently \
                                            reserved."
                                    )
                                    return redirect(
                                        "view_schedule",
                                        class_id=class_name.id,
                                        week_offset=week_offset,
                                    )
                            else:
                                messages.error(request, \
                                               "Teacher is curently reserved.")
                                return redirect(
                                    "view_schedule",
                                    class_id=class_name.id,
                                    week_offset=week_offset,
                                )

                    except:
                        messages.error(
                            request,
                            "Occured an error while editing - \
                                please check data and try again.",
                        )
                        return redirect(
                            "view_schedule",
                            class_id=class_name.id,
                            week_offset=week_offset,
                        )
                else:
                    try:
                        with transaction.atomic():
                            current_classroom_reservation.end_date = date
                            current_classroom_reservation.save()

                            current_teacher_reservation.end_date = date
                            current_teacher_reservation.save()

                            pre_classroom_reservation_exists = (
                                ClassroomReservation.objects.filter(
                                    classroom=classroom,
                                    day_of_week=day_of_week,
                                    lesson_number=lesson_number,
                                    start_date__lte=date,
                                    end_date=None,
                                ).exists()
                            )

                            pre_teacher_reservation_exists = (
                                TeacherReservation.objects.filter(
                                    teacher=teacher,
                                    day_of_week=day_of_week,
                                    lesson_number=lesson_number,
                                    start_date__lte=date,
                                    end_date=None,
                                ).exists()
                            )

                            if not pre_teacher_reservation_exists:
                                if not pre_classroom_reservation_exists:
                                    classrooom_new_reservation = (
                                        ClassroomReservation.objects.create(
                                            classroom=classroom,
                                            day_of_week=day_of_week,
                                            lesson_number=lesson_number,
                                            start_date=date,
                                            end_date=date,
                                            class_unit=class_name,
                                        )
                                    )

                                    teacher_new_reservation = (
                                        TeacherReservation.objects.create(
                                            teacher=teacher,
                                            day_of_week=day_of_week,
                                            lesson_number=lesson_number,
                                            start_date=date,
                                            end_date=date,
                                            class_unit=class_name,
                                        )
                                    )

                                    Lesson.objects.create(
                                        subject=subject,
                                        day_of_week=day_of_week,
                                        lesson_number=lesson_number,
                                        teacher=teacher,
                                        class_name=class_name,
                                        classroom=classroom,
                                        date=date,
                                        is_base=is_base,
                                        is_cancelled=is_cancelled,
                                        classroom_reservation=classrooom_new_reservation,
                                        teacher_reservation=teacher_new_reservation,
                                    )

                                    sender_profile = Profile.objects.get(
                                        user=request.user
                                    )

                                    students = class_name.students_in_class.all()
                                    date_str = date.strftime("%Y-%m-%d")
                                    day_of_week_str = calendar.day_name[day_of_week]

                                    for student in students:
                                        receiver = student.user
                                        title = "New lesson for your class"
                                        body = f"""There is a change in your schedule. Currently your {lesson_number} lesson on {day_of_week_str} ({date_str}) will be:

                                        Subject: {subject}
                                        Teacher: {teacher}
                                        Classroom: {classroom}

                                        Please check your schedule for more information.
                                        """
                                        Message.objects.create(
                                            sender=sender_profile,
                                            receiver=receiver,
                                            title=title,
                                            body=body,
                                        )

                                    messages.success(
                                        request, "Lesson edited successfully"
                                    )
                                    return redirect(
                                        "view_schedule",
                                        class_id=class_name.id,
                                        week_offset=week_offset,
                                    )
                                else:
                                    messages.error(
                                        request,
                                        "Classroom is curently \
                                            reserved for this date.",
                                    )
                                    return redirect(
                                        "view_schedule",
                                        class_id=class_name.id,
                                        week_offset=week_offset,
                                    )
                            else:
                                messages.error(
                                    request,
                                    "Teacher is curently reserved for \
                                        this date.",
                                )
                                return redirect(
                                    "view_schedule",
                                    class_id=class_name.id,
                                    week_offset=week_offset,
                                )
                    except:
                        messages.error(
                            request,
                            "Occured an error while editing - please check \
                                data and try again.",
                        )
                        return redirect(
                            "view_schedule",
                            class_id=class_name.id,
                            week_offset=week_offset,
                        )

            else:
                try:
                    lesson.subject = form.cleaned_data["subject"]
                    lesson.is_base = form.cleaned_data["is_base"]
                    lesson.is_cancelled = form.cleaned_data["is_cancelled"]
                    lesson.save()

                    messages.success(request, "Lesson edited successfully")
                    return redirect(
                        "view_schedule", class_id=class_name.id, 
                        week_offset=week_offset
                    )
                except:
                    messages.error(
                        request,
                        "Occured an error while editing - \
                            please check data and try again.",
                    )
                    return render(
                        request,
                        "view_schedule.html",
                        class_id=lesson.class_id,
                        week_offset=week_offset,
                    )

        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)

            return redirect(".")
