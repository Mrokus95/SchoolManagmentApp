from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from usersApp.models import Profile, Student, ClassUnit, Parent
from django.test.client import RequestFactory

class EventTest(TestCase):

    def setUp(self):
        self.user_student = User.objects.create_user(username='testuser', password='testpassword')
        self.user_parent = User.objects.create_user(username='testuser1', password='testpassword')
        self.profile_student = Profile.objects.create(user=self.user_student, phone_number='123456789', account_type = Profile.STUDENT)
        self.profile_parent = Profile.objects.create(user=self.user_parent, phone_number='123456789', account_type = Profile.PARENT)
        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')
        self.parent = Parent.objects.create(user=self.profile_parent)
        self.student = Student.objects.create(user=self.profile_student, class_unit=self.class_unit, parent=self.parent)

    def test_event_redirect_user_url(self):
        url = reverse('events')
        response = self.client.get(url)                    
        self.assertEqual(response.status_code, 302)

    def test_event_student_url(self):
        self.client.force_login(self.user_student)
        url = reverse('filter_events_student')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_event_student_template(self):
        self.client.force_login(self.user_student)
        url = reverse('filter_events_student')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'events.html')

