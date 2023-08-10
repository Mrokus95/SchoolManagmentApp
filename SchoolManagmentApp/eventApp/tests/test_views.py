from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from usersApp.models import Profile, Student, ClassUnit, Parent
from eventApp.models import CalendarEvents, LessonReport, Subject, Teacher
from eventApp.views import events_student_filter, event_status_changer, date_filter_validation, event_paginator
from django.utils import timezone
from django.http import HttpRequest
from datetime import timedelta, date
from django.core.paginator import Paginator

class EventsViewTest(TestCase):

    def setUp(self):

        #users
        self.user_student = User.objects.create_user(username='testuser', password='testpassword')
        self.user_parent = User.objects.create_user(username='testuser1', password='testpassword')
        self.user_teacher = User.objects.create_user(username='testuser3', password='testpassword')

        #profiles
        self.profile_student = Profile.objects.create(user=self.user_student, account_type = Profile.STUDENT)
        self.profile_parent = Profile.objects.create(user=self.user_parent, account_type = Profile.PARENT)
        self.profile_teacher = Profile.objects.create(user=self.user_teacher, account_type = Profile.TEACHER)

        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')
        #accounts
        self.parent = Parent.objects.create(user=self.profile_parent)
        self.student = Student.objects.create(user=self.profile_student, class_unit=self.class_unit, parent=self.parent)
        self.teacher = Teacher.objects.create(user=self.profile_teacher)

        #lesson_report
        self.subject = Subject.objects.create(name=Subject.ENGLISH)
        self.lesson_title = 'Test title'
        self.lesson_description = 'Test description'

        self.lesson_report = LessonReport.objects.create(
            subject = self.subject,
            teacher = self.teacher,
            class_unit = self.class_unit,
            lesson_title = self.lesson_title,
            lesson_description = self.lesson_description
        )

        #calendar_event
        self.event = CalendarEvents.objects.create(
            description = self.lesson_description,
            realisation_time = date.today(),
            subject = self.subject,
            author = self.teacher,
            connected_to_lesson = self.lesson_report
        )

    #views redirect
    def test_event_redirect_user_url(self):
        url = reverse('events')
        response = self.client.get(url)                    
        self.assertEqual(response.status_code, 302)

    #redirect if kids
    # def test_event_url_parent_filter_event_teacher(self):
    #     self.client.force_login(self.user_teacher)
    #     url = reverse('parent_filter_events')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)

    # def test_event_url_parent_filter_event_parent(self):
    #     self.client.force_login(self.user_parent)
    #     url = reverse('parent_filter_events')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)

    # def test_event_url_parent_filter_event_student(self):
    #     self.client.force_login(self.user_student)
    #     url = reverse('parent_filter_events')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)


    #views events
    def test_event_url_filter_events_student(self):
        self.client.force_login(self.user_student)
        url = reverse('filter_events_student')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events.html')

    def test_event_url_filter_event_parent(self):
        self.client.force_login(self.user_parent)
        url = reverse('filter_events_student')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_event_url_filter_event_teacher(self):
        self.client.force_login(self.user_teacher)
        url = reverse('filter_events_student')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
   
    def test_event_url_filter_event_stuednt_parent_parent(self):
        test_id = self.student.id
        self.client.force_login(self.user_parent)
        url = reverse('filter_events_student_parent', args=[test_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events.html')

    def test_event_url_filter_event_student_parent_student(self):
        test_id = self.student.id
        self.client.force_login(self.user_student)
        url = reverse('filter_events_student_parent', args=[test_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_event_url_filter_event_student_parent_teacher(self):
        test_id = self.student.id
        self.client.force_login(self.user_teacher)
        url = reverse('filter_events_student_parent', args=[test_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_event_url_teacher_events_teacher(self):
        self.client.force_login(self.user_teacher)
        url = reverse('teacher_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_events.html')

    def test_event_url_teacher_events_student(self):
        self.client.force_login(self.user_student)
        url = reverse('teacher_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'teacher_events.html')

    def test_event_url_teacher_events_parent(self):
        self.client.force_login(self.user_parent)
        url = reverse('teacher_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'teacher_events.html')

    #events_detail
    def test_event_detail_url_event_detail_student(self):
        event_id = self.event.id
        self.client.force_login(self.user_student)
        url = reverse('event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_detail.html')

    def test_event_detail_url_event_detail_parent(self):
        event_id = self.event.id
        self.client.force_login(self.user_parent)
        url = reverse('event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_detail.html')

    def test_event_detail_url_event_detail_teacher(self):
        event_id = self.event.id
        self.client.force_login(self.user_teacher)
        url = reverse('event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_detail.html')

    def test_event_url_teacher_event_detail_teacher(self):
        event_id = self.event.id
        self.client.force_login(self.user_teacher)
        url = reverse('teacher_event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_event_details.html')

    def test_event_url_teacher_event_detail_student(self):
        event_id = self.event.id
        self.client.force_login(self.user_student)
        url = reverse('teacher_event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'teacher_events_detail.html')

    def test_event_url_teacher_event_detail_parent(self):
        event_id = self.event.id
        self.client.force_login(self.user_parent)
        url = reverse('teacher_event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'teacher_events_detail.html')

    #event_delete
    def test_event_url_delete_event_teacher(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_teacher)
        url = reverse('delete_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_event_url_delete_event_parent(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_parent)
        url = reverse('delete_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'delete_event.html')

    def test_event_url_delete_event_student(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_student)
        url = reverse('delete_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'delete_event.html')

    #event edit
    def test_event_url_edit_event_student(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_student)
        url = reverse('edit_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'edit_event.html')

    def test_event_url_edit_event_teacher(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_teacher)
        url = reverse('edit_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_event.html')

    def test_event_url_edit_event_parent(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_parent)
        url = reverse('edit_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'edit_event.html')

class EventsFunctionTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile_teacher = Profile.objects.create(user=self.user, account_type = Profile.TEACHER)
        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')
        self.teacher = Teacher.objects.create(user=self.profile_teacher)

        #lesson_report
        self.subject = Subject.objects.create(name=Subject.ENGLISH)
        self.subject_1 = Subject.objects.create(name=Subject.HISTORY)
        self.subject_2 = Subject.objects.create(name=Subject.MATHEMATIC)
        self.title = 'Test title'
        self.description = 'Test description'

        self.lesson_report = LessonReport.objects.create(
            subject = self.subject,
            teacher = self.teacher,
            class_unit = self.class_unit,
            lesson_title = self.title,
            lesson_description = self.description
        )

        #calendar_event
        self.event = CalendarEvents.objects.create(
            description = self.description,
            realisation_time = date.today(),
            subject = self.subject,
            author = self.teacher,
            event_type = 'Test',
            connected_to_lesson = self.lesson_report
        )

        self.event_1 = CalendarEvents.objects.create(
            description = self.description,
            realisation_time = date.today() + timedelta(days=2),
            subject = self.subject_1,
            author = self.teacher,
            event_type = 'Small Test',
            connected_to_lesson = self.lesson_report
        )

        self.event_2 = CalendarEvents.objects.create(
            description = self.description,
            realisation_time = date.today() + timedelta(days=4),
            subject = self.subject_2,
            author = self.teacher,
            event_type = 'Project',
            connected_to_lesson = self.lesson_report
        )

    def test_event_status_changer(self):
        realisation_time = date.today() - timedelta(days=1)
        self.event.realisation_time = realisation_time
        event_status_changer([self.event])
        self.assertEqual(self.event.finished, True)
    
    def test_invalid_date_validation(self):
        request = HttpRequest()
        request.POST['start_date'] = str(date.today())
        request.POST['end_date'] = str(date.today() - timedelta(days=1))
        self.assertEqual(date_filter_validation(request), True)

    def test_valid_date_validation(self):
        request = HttpRequest()
        request.POST['start_date'] = str(date.today())
        request.POST['end_date'] = str(date.today() + timedelta(days=1))
        self.assertEqual(date_filter_validation(request), False)
   
    def test_event_paginator(self):
        events_to_paginate=list(range(12)) 
        events_per_site=3
        request = HttpRequest()
        request.GET['page'] = 4
        result = event_paginator(request, events_to_paginate, events_per_site)
        self.assertEqual(result.number, 4)
        self.assertTrue(result.paginator.page(2).has_previous())
        self.assertTrue(result.paginator.page(2).has_next())
        

    def test_event_filter_events_subject(self):
        request = HttpRequest()
        request.POST['subject'] = self.subject
        request.POST['event_type'] = 'All'
        request.POST['start_date'] = None
        request.POST['end_date'] = None
        queryset = CalendarEvents.objects.all()
        queryset_after = events_student_filter(request, queryset)
        self.assertEqual(len(queryset), 3)
        self.assertEqual(len(queryset_after), 1)
        self.assertEqual(queryset_after.first().subject, self.subject)

    def test_event_filter_events_event_type(self):
        request = HttpRequest()
        request.POST['subject'] = 'All'
        request.POST['event_type'] = 'Test'
        request.POST['start_date'] = None
        request.POST['end_date'] = None
        queryset = CalendarEvents.objects.all()
        queryset_after = events_student_filter(request, queryset)
        self.assertEqual(len(queryset), 3)
        self.assertEqual(len(queryset_after), 1)
        self.assertEqual(queryset_after.first().event_type, 'Test')

    def test_event_filter_events_start_date(self):
        request = HttpRequest()
        request.POST['subject'] = 'All'
        request.POST['event_type'] = 'All'
        request.POST['start_date'] = date.today() + timedelta(days=4)
        request.POST['end_date'] = None
        queryset = CalendarEvents.objects.all()
        queryset_after = events_student_filter(request, queryset)
        self.assertEqual(len(queryset), 3)
        self.assertEqual(len(queryset_after), 1)
        self.assertEqual(queryset_after.first().realisation_time, date.today() + timedelta(days=4))

    def test_event_filter_events_end_date(self):
        request = HttpRequest()
        request.POST['subject'] = 'All'
        request.POST['event_type'] = 'All'
        request.POST['start_date'] = None
        request.POST['end_date'] = date.today() + timedelta(days=1)
        queryset = CalendarEvents.objects.all()
        queryset_after = events_student_filter(request, queryset)
        self.assertEqual(len(queryset), 3)
        self.assertEqual(len(queryset_after), 1)
        self.assertEqual(queryset_after.first().realisation_time, date.today())

    def test_event_filter_events_Both_date(self):
        request = HttpRequest()
        request.POST['subject'] = self.subject
        request.POST['event_type'] = 'All'
        request.POST['start_date'] = date.today() - timedelta(days=1)
        request.POST['end_date'] = date.today() + timedelta(days=1)
        queryset = CalendarEvents.objects.all()
        queryset_after = events_student_filter(request, queryset)
        self.assertEqual(len(queryset), 3)
        self.assertEqual(len(queryset_after), 1)
        self.assertEqual(queryset_after.first().realisation_time, date.today())

    def test_event_filter_events_all(self):
        request = HttpRequest()
        request.POST['subject'] = self.subject
        request.POST['event_type'] = 'Test'
        request.POST['start_date'] = date.today() - timedelta(days=1)
        request.POST['end_date'] = date.today() + timedelta(days=10)
        queryset = CalendarEvents.objects.all()
        queryset_after = events_student_filter(request, queryset)
        self.assertEqual(len(queryset), 3)
        self.assertEqual(len(queryset_after), 1)

    def test_event_filter_events_no_conditions(self):
        request = HttpRequest()
        request.POST['subject'] = 'All'
        request.POST['event_type'] = 'All'
        request.POST['start_date'] = None
        request.POST['end_date'] = None
        queryset = CalendarEvents.objects.all()
        queryset_after = events_student_filter(request, queryset)
        self.assertEqual(len(queryset), 3)
        self.assertEqual(len(queryset_after), 3)


