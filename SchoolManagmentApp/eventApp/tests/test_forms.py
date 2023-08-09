from django.test import TestCase
from eventApp.forms import AddEvent, EventFilterStudentForm
from eventApp.models import LessonReport, Subject, Teacher, ClassUnit
from gradesApp.models import Semester
from django.contrib.auth.models import User
from usersApp.models import Profile
from datetime import date, timedelta

class AddEventFormTest(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name=Subject.ENGLISH)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, phone_number='123456789', account_type = Profile.TEACHER)
        self.teacher = Teacher.objects.create(user=self.profile)
        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')
        self.lesson_title = 'Simple Title'
        self.lesson_description = 'Simple Description'       
        self.event_type = 'Small Test'

        self.fake_lesson = LessonReport.objects.create(
            subject=self.subject,
            teacher=self.teacher,
            class_unit=self.class_unit,
            lesson_title = self.lesson_title,
            lesson_description = self.lesson_description
        )

    def test_add_event_valid_form(self):
        data = {
            'description': 'Test event',
            'connected_to_lesson': self.fake_lesson.id,
            'realisation_time': date.today()+ timedelta(days=1),
            'event_type': self.event_type
            }
        form = AddEvent(data)
        self.assertTrue(form.is_valid())

    def test_add_event_invalid_form(self):
        wrong_data = {
            'description': '',
            'connected_to_lesson': 999,
            'realisation_time': date.today() - timedelta(days=1),
            'event_type': 'incorrect'
            }
        form = AddEvent(wrong_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

class EventFilterSutentFormTest(TestCase):
    def setUp(self):
        self.subject = 'English'
        self.event_type = 'Small Test'
        self.semester = Semester.objects.create(
            number=1,
            start_school_year=2023,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
        )
        
    def test_valid_event_filter_student_form(self):
        data = {
            'subject': self.subject,  
            'event_type': self.event_type,
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=1),
        }
        
        form = EventFilterStudentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_event_filter_student_form(self):
        wrong_data = {
            'subject': 'Invalid Subject',
            'event_type': 'Invalid Event Type',
            'start_date': date.today(),
            'end_date': date.today() - timedelta(days=5),
        }

        form = EventFilterStudentForm(data=wrong_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)