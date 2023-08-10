from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from usersApp.models import Profile, Student, ClassUnit, Parent
from eventApp.models import CalendarEvents, LessonReport, Subject, Teacher
from eventApp.views import events_student_filter
from django.utils import timezone
from django.http import HttpRequest
from datetime import timedelta, date


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
        self.assertTemplateUsed('events.html')

    def test_event_url_filter_event_parent(self):
        self.client.force_login(self.user_parent)
        url = reverse('filter_events_student')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('home.html')
        self.assertTemplateUsed('events.html')

    def test_event_url_filter_event_teacher(self):
        self.client.force_login(self.user_teacher)
        url = reverse('filter_events_student')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('home')
        self.assertTemplateUsed('teacher_events')
   
    def test_event_url_filter_event_stuednt_parent_parent(self):
        test_id = self.student.id
        self.client.force_login(self.user_parent)
        url = reverse('filter_events_student_parent', args=[test_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('events')

    def test_event_url_filter_event_student_parent_student(self):
        test_id = self.student.id
        self.client.force_login(self.user_student)
        url = reverse('filter_events_student_parent', args=[test_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('events')

    def test_event_url_filter_event_student_parent_teacher(self):
        test_id = self.student.id
        self.client.force_login(self.user_teacher)
        url = reverse('filter_events_student_parent', args=[test_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('home')
        self.assertTemplateUsed('teacher_event')

    def test_event_url_teacher_events_teacher(self):
        self.client.force_login(self.user_teacher)
        url = reverse('teacher_events')
        respoense = self.client.get(url)
        self.assertEqual(respoense.status_code, 200)
        self.assertTemplateUsed('teacher_event')

    def test_event_url_teacher_events_student(self):
        self.client.force_login(self.user_student)
        url = reverse('teacher_events')
        respoense = self.client.get(url)
        self.assertEqual(respoense.status_code, 302)
  

    def test_event_url_teacher_events_parent(self):
        self.client.force_login(self.user_parent)
        url = reverse('teacher_events')
        respoense = self.client.get(url)
        self.assertEqual(respoense.status_code, 302)

    #events_detail
    def test_event_detail_url_event_detail_student(self):
        event_id = self.event.id
        self.client.force_login(self.user_student)
        url = reverse('event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_detail_url_event_detail_parent(self):
        event_id = self.event.id
        self.client.force_login(self.user_parent)
        url = reverse('event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_detail_url_event_detail_teacher(self):
        event_id = self.event.id
        self.client.force_login(self.user_teacher)
        url = reverse('event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_url_teacher_event_detail_teacher(self):
        event_id = self.event.id
        self.client.force_login(self.user_teacher)
        url = reverse('teacher_event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_url_teacher_event_detail_student(self):
        event_id = self.event.id
        self.client.force_login(self.user_student)
        url = reverse('teacher_event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_event_url_teacher_event_detail_parent(self):
        event_id = self.event.id
        self.client.force_login(self.user_parent)
        url = reverse('teacher_event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

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

    def test_event_url_delete_event_student(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_student)
        url = reverse('delete_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    #event edit

    def test_event_url_edit_event_student(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_student)
        url = reverse('edit_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_event_url_edit_event_teacher(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_teacher)
        url = reverse('edit_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_url_edit_event_parent(self):
        event_id = self.event.id
        self.client.force_login(user=self.user_parent)
        url = reverse('edit_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

