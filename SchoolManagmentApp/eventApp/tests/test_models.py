from django.test import TestCase
from eventApp.models import Subject, Teacher
from usersApp.models import Profile
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class SybjectTestCase(TestCase):

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
        self.profile = Profile.objects.create(user=self.user, phone_number='123456789', account_type = Profile.STUDENT)
        self.lesson_type = Subject.objects.create(name=Subject.MATHEMATIC)
        self.teacher = Teacher.objects.create(user=self.profile)
        self.teacher.lesson_type.set([self.lesson_type])

    def test_teacher_creation(self):
        self.assertEqual(self.teacher.user, self.profile)
        self.assertEqual(self.teacher.lesson_type, self.lesson_type.all())

    # def test_teacher_str(self):
    #     expected_str = f'{self.user.user.first_name} {self.user.user.last_name}'
    #     self.assertEqual(str(self.teacher), expected_str)

    # def test_teacher_related_names(self):
    #     self.assertEqual(self.teacher, self.profile.teacher_student.filter(id=self.teacher.id))
    #     self.assertEqual(self.teacher, self.lesson_type.subject_teachers.filter(id=self.teacher.id))

    
    # def test_limit_choices(self):
    #     invalid_user = User.objects.create_user(username='invalid_user', password='test_password')
    #     invalid_profile = Profile.objects.create(user=invalid_user, phone_number='987654321', account_type=Profile.PARENT)

    #     with self.assertRaises(ValidationError):
    #         teacher = Teacher.objects.create(user=invalid_user) 
    #         teacher.lesson_type.set([self.lesson_type])
    #         teacher.full_clean()

    # def test_delete_user(self):
    #     teacher_id = self.teacher.id
    #     self.teacher.lesson_type.clear()
    #     self.user.delete()
    #     with self.assertRaises(Teacher.DoesNotExist):
    #         Teacher.objects.get(id=teacher_id)
      