from django.test import TestCase
from datetime import date
from eventApp.models import CalendarEvents
from eventApp.views import events_student_filter

class EventStudentFilterTestCase(TestCase):
 
 def setUp(self):
    self.event_1=CalendarEvents.objects.create(subject="Mathematic", event_type="Test", realisation_time=date(2023, 8, 10))
    self.event_2=CalendarEvents.objects.create(subject="English", event_type="Project", realisation_time=date(2023, 8, 15))
    self.event_3=CalendarEvents.objects.create(subject="History", event_type="Other", realisation_time=date(2023, 8, 20))

def test_filter_by_subject(self):
    request = self.client.post('/', {'subject': 'Math'})
    queryset = events_student_filter(request, CalendarEvents.objects.all())
    self.assertEqual(queryset.count(), 1)
    self.assertEqual(queryset[0], self.event1)



