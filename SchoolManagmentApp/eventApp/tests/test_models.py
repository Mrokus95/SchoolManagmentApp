from django.test import TestCase
from eventApp.models import Subject, Teacher, LessonReport, CalendarEvents
from usersApp.models import Profile, ClassUnit
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import date

class SubjectTestCase(TestCase):

    def setUp(self):
        self.subject_math = Subject.objects.create(name=Subject.MATHEMATIC)

    def test_subject_create(self):
        self.assertEqual(self.subject_math.name, Subject.MATHEMATIC)

    def test_subject_name_unique(self):
        with self.assertRaises(IntegrityError):
            Subject.objects.create(name=Subject.MATHEMATIC)

    def test_subject_name_default(self):
        default_subject = Subject.objects.create()
        self.assertEqual(default_subject.name, '')

    def test_subject_str(self):
        self.assertEqual(str(self.subject_math), Subject.MATHEMATIC)

class TeacherTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, phone_number='123456789', account_type = Profile.TEACHER)
        self.lesson_type_english = Subject.objects.create(name=Subject.ENGLISH)
        self.lesson_type_mathematic = Subject.objects.create(name=Subject.MATHEMATIC)
        self.teacher = Teacher.objects.create(user=self.profile)
        self.teacher.lesson_type.add(self.lesson_type_mathematic)
        self.teacher.lesson_type.add(self.lesson_type_english)

    def test_teacher_creation(self):
        self.assertEqual(self.teacher.user, self.profile)
        expected_lesson_types = [self.lesson_type_english, self.lesson_type_mathematic]
        actual_lesson_types = list(self.teacher.lesson_type.all())
        self.assertEqual(expected_lesson_types, actual_lesson_types)

    def test_teacher_str(self):
        expected_str = f'{self.user.first_name} {self.user.last_name}'
        self.assertEqual(str(self.teacher), expected_str)

    def test_teacher_related_names(self):
       self.assertEqual(self.teacher, self.profile.teacher_student)
       self.assertIn(self.teacher, self.lesson_type_english.subject_teachers.all())

    
    def test_limit_choices(self):
        invalid_user = User.objects.create_user(username='invalid_user', password='test_password')
        invalid_profile = Profile.objects.create(user=invalid_user, phone_number='987654321', account_type=Profile.PARENT)

        try:
            invalid_teacher = Teacher.objects.create(user=invalid_user)
            invalid_teacher.full_clean()

        except ValueError:
            pass

    def test_delete_subject(self):
        self.teacher.lesson_type.clear()
        self.assertTrue(Teacher.objects.filter(id=self.teacher.id).exists())


     
    def test_delete_teacher(self):
        teacher_id = self.teacher.id
        self.teacher.delete()
        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(id=teacher_id)
        
        self.teacher = Teacher.objects.create(user=self.profile)
        self.teacher.lesson_type.add(self.lesson_type_mathematic)

    def test_delete_user(self):
        teacher_id = self.teacher.id
        self.user.delete()
        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(id=teacher_id)

class LessonReportCase(TestCase):
    def setUp(self):
        self.create_date = date.today()
        self.subject = Subject.objects.create(name=Subject.ENGLISH)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, phone_number='123456789', account_type = Profile.TEACHER)
        self.teacher = Teacher.objects.create(user=self.profile)
        self.teacher.lesson_type.add(self.subject)
        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')
        self.lesson_title = 'Simple Title'
        self.lesson_discription = 'Simple Description'

        self.report = LessonReport.objects.create(
            subject=self.subject,
            teacher=self.teacher,
            class_unit=self.class_unit,
            lesson_title = self.lesson_title,
            lesson_description = self.lesson_discription
        )

        self.report_id = self.report.id

    def test_lesson_creation_correct_date(self):
        self.assertEqual(self.report.create_date, date.today())
        self.assertEqual(self.report.subject, self.subject)
        self.assertEqual(self.report.teacher, self.teacher)
        self.assertEqual(self.report.class_unit, self.class_unit)
        self.assertEqual(self.report.lesson_title, 'Simple Title')
        self.assertEqual(self.report.lesson_description, 'Simple Description')

    def test_lesson_str(self):
        expected_str = f'Lesson report: {self.subject} from {self.create_date} of {self.class_unit}'
        self.assertEqual(str(self.report), expected_str)

    def test_lesson_report_related_names(self):
        self.assertEqual(list(self.report.subject.reports_subject.all()), [self.report])
        self.assertEqual(list(self.report.teacher.reports_teacher.all()), [self.report])
        self.assertEqual(list(self.report.class_unit.reports_class_unit.all()), [self.report])


    def test_lesson_report_title_length(self):
        orginal_title = self.report.lesson_title
        invalid_title = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eget justo nulla. Fusce accumsan sapien sit amet hendrerit interdum. Nulla facilisi. Nam feugiat tristique risus, ac pellentesque dolor dictum nec. Fusce auctor feugiat libero, vel ullamcorper odio suscipit ut.'
        self.report.lesson_title = invalid_title

        with self.assertRaises(ValidationError):
            self.report.full_clean()

        self.report.lesson_title = orginal_title
        
    def test_lesson_report_deleting_teacher(self):
        report_id = self.report.id
        self.teacher.delete()
        self.assertFalse(LessonReport.objects.filter(id=report_id).exists())

        self.teacher = Teacher.objects.create(user=self.profile)
        self.report = LessonReport.objects.create(
            subject=self.subject,
            teacher=self.teacher,
            class_unit=self.class_unit,
            lesson_title = self.lesson_title,
            lesson_description = self.lesson_discription
        )

    def test_lesson_report_deleting_class_unit(self):
        report_id = self.report.id
        self.class_unit .delete()
        self.assertFalse(LessonReport.objects.filter(id=report_id).exists())

        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')
        self.report = LessonReport.objects.create(
            subject=self.subject,
            teacher=self.teacher,
            class_unit=self.class_unit,
            lesson_title = self.lesson_title,
            lesson_description = self.lesson_discription
        )

    def test_lesson_report_deleting_subject(self):
        report_id = self.report.id
        self.subject.delete()
        self.assertFalse(LessonReport.objects.filter(id=report_id).exists())

        self.subject = Subject.objects.create(name=Subject.ENGLISH)
        self.report = LessonReport.objects.create(
            subject=self.subject,
            teacher=self.teacher,
            class_unit=self.class_unit,
            lesson_title = self.lesson_title,
            lesson_description = self.lesson_discription
        )

    def test_delete_lesson_raport(self):
        report_id = self.report.id
        self.report.delete()
        self.assertFalse(LessonReport.objects.filter(id=report_id).exists())

class CalendarEventsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, phone_number='123456789', account_type=Profile.TEACHER)
        self.subject = Subject.objects.create(name=Subject.ENGLISH)
        self.teacher = Teacher.objects.create(user=self.profile)
        self.teacher.lesson_type.add(self.subject)
        self.event_type = CalendarEvents.TEST
        self.description = 'Simple Event Description'

        #report data:

        self.teacher.lesson_type.add(self.subject)
        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')
        self.lesson_title = 'Simple Title'
        self.lesson_discription = 'Simple Description'

        #create report

        self.report = LessonReport.objects.create(
            subject=self.subject,
            teacher=self.teacher,
            class_unit=self.class_unit,
            lesson_title = self.lesson_title,
            lesson_description = self.lesson_discription
        )
        #create event

        self.event = CalendarEvents.objects.create(
            description=self.description,
            event_type=self.event_type,
            realisation_time=date.today(),
            subject=self.subject,
            author=self.teacher,
            connected_to_lesson=self.report,
            visited = True,
        )

        self.event_id = self.event.id

    def test_event_creation(self):
        self.assertEqual(self.event.description, 'Simple Event Description')
        self.assertEqual(self.event.event_type, self.event_type)
        self.assertEqual(self.event.realisation_time, date.today())
        self.assertEqual(self.event.subject, self.subject)
        self.assertEqual(self.event.author, self.teacher)
        self.assertEqual(self.event.connected_to_lesson, self.report)
        self.assertEqual(self.event.author, self.teacher)
        self.assertEqual(self.event.visited, True)


    def test_event_str(self):
        expected_str = f'{self.event.event_type} added by: {self.teacher} on: {self.subject}'
        self.assertEqual(str(self.event), expected_str)

    def test_event_related_names(self):
        self.assertEqual(list(self.event.subject.subject.all()), [self.event])
        self.assertEqual(list(self.event.author.author.all()), [self.event])
        self.assertEqual(list(self.event.connected_to_lesson.related_lesson.all()), [self.event])



    # def test_delete_event(self):
    #     event_id = self.event.id
    #     self.event.delete()
    #     self.assertFalse(CalendarEvents.objects.filter(id=event_id).exists())
        
    #     self.event = CalendarEvents.objects.create(
    #         description=self.description,
    #         event_type=self.event_type,
    #         realisation_time=date.today(),
    #         subject=self.subject,
    #         author=self.teacher
    #     )

    # def test_related_lesson_delete(self):
    #     self.report = LessonReport.objects.create(
    #         subject=self.subject,
    #         teacher=self.teacher,
    #         class_unit=self.class_unit,
    #         lesson_title='Simple Title',
    #         lesson_description='Simple Description'
    #     )

    #     self.event.connected_to_lesson = self.report
    #     self.event.save()

    #     report_id = self.report.id
    #     self.report.delete()
    #     self.assertFalse(CalendarEvents.objects.filter(id=self.event_id).exists())

    #     self.report = LessonReport.objects.create(
    #         subject=self.subject,
    #         teacher=self.teacher,
    #         class_unit=self.class_unit,
    #         lesson_title='Simple Title',
    #         lesson_description='Simple Description'
    #     )
        
    #     self.event.connected_to_lesson = self.report
    #     self.event.save()

     
 

