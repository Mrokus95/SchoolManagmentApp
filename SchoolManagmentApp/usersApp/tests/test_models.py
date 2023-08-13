from unittest.mock import MagicMock, patch
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import ClassUnit, Parent, Profile, Student


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.profile = Profile.objects.create(
            user=self.user, phone_number="123456789", 
            account_type=Profile.TEACHER
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone_number, "123456789")
        self.assertEqual(self.profile.account_type, Profile.TEACHER)

    def test_str_representation(self):
        expected_str = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(str(self.profile), expected_str)

    def test_default_photo(self):
        self.assertEqual(self.profile.photo.url, 
                         "/media/users/avatars/unknown.png")

    def test_change_account_type(self):
        self.profile.account_type = Profile.PARENT
        self.profile.save()
        self.assertEqual(self.profile.account_type, Profile.PARENT)

    def test_invalid_account_type(self):
        with self.assertRaises(ValidationError):
            self.profile.account_type = "Invalid"
            self.profile.save()

    @patch("PIL.Image.open")
    def test_invalid_photo_file_type(self, mock_open):
        mock_image = MagicMock()
        mock_image.format = "INVALID_FORMAT"
        mock_open.return_value = mock_image

        with self.assertRaises(ValidationError):
            self.profile.validate_image("dummy_path_to_invalid.gif")

    def test_phone_number_too_short(self):
        with self.assertRaises(ValidationError):
            self.profile.phone_number = "253656"
            self.profile.save()

    def test_phone_numbers_with_alpha(self):
        with self.assertRaises(ValidationError):
            self.profile.phone_number = "253656df8"
            self.profile.save()

    def test_null_phone_number(self):
        self.profile.phone_number = None
        self.profile.save()
        self.assertIsNone(self.profile.phone_number)

    def test_blank_phone_number(self):
        self.profile.phone_number = ""
        self.profile.save()
        self.assertEqual(self.profile.phone_number, "")

    def test_update_profile(self):
        new_phone_number = "987654321"
        self.profile.phone_number = new_phone_number
        self.profile.save()
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.phone_number, new_phone_number)

    def test_delete_profile(self):
        profile_id = self.profile.id
        self.profile.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(pk=profile_id)

    def test_delete_profiles_user(self):
        profile_id = self.profile.id
        self.user.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(pk=profile_id)


class ClassUnitTestCase(TestCase):
    def test_valid_class_unit(self):
        class_unit = ClassUnit.objects.create(
            start_year=2023, study_year=1, letter_mark="A"
        )
        self.assertEqual(str(class_unit), "Class 1A")

    def test_invalid_start_year(self):
        with self.assertRaises(ValidationError):
            class_unit = ClassUnit(start_year=2022, study_year=1, 
                                   letter_mark="A")
            class_unit.full_clean()

    def test_invalid_study_year(self):
        with self.assertRaises(ValidationError):
            class_unit = ClassUnit(start_year=2023, study_year=0, 
                                   letter_mark="A")
            class_unit.full_clean()

    def test_invalid_letter_mark(self):
        with self.assertRaises(ValidationError):
            class_unit = ClassUnit(start_year=2023, study_year=1, 
                                   letter_mark="X")
            class_unit.full_clean()

    def test_unique_together_constraint(self):
        ClassUnit.objects.create(start_year=2023, study_year=1, 
                                 letter_mark="A")

        with self.assertRaises(ValidationError):
            class_unit = ClassUnit(start_year=2023, study_year=1, 
                                   letter_mark="A")
            class_unit.full_clean()


class ClassUnitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.profile = Profile.objects.create(
            user=self.user, phone_number="123456789", 
            account_type=Profile.PARENT
        )
        self.profile2 = Profile.objects.create(
            user=self.user2, phone_number="123456789", 
            account_type=Profile.STUDENT
        )
        self.parent = Parent.objects.create(user=self.profile)

    def test_parent_creation(self):
        self.assertEqual(self.parent.user.user, self.user)
        self.assertEqual(self.parent.user.phone_number, "123456789")
        self.assertEqual(self.parent.user.photo, "users/avatars/unknown.png")
        self.assertEqual(self.parent.user.account_type, Profile.PARENT)

    def test_str_representation(self):
        self.assertEqual(
            str(self.parent),
            f"Parent: {self.parent.user.user.first_name} \
                {self.parent.user.user.last_name}'s profile",
        )

    def test_invalid_parent_profile(self):
        with self.assertRaises(ValidationError):
            parent = Parent(user=self.profile2)
            parent.full_clean()

    def test_delete_user(self):
        parent_id = self.parent.id
        self.user.delete()
        with self.assertRaises(Parent.DoesNotExist):
            Parent.objects.get(pk=parent_id)


class StudentTestCase(TestCase):
    def setUp(self):
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username="testuser", password="testpassword"
            )

        self.profile = Profile.objects.create(
            user=self.user, phone_number="123456789", 
            account_type=Profile.STUDENT
        )
        self.class_unit = ClassUnit.objects.create(
            start_year=2023, study_year=1, letter_mark="A"
        )
        self.parent = Parent.objects.create(user=self.profile)
        self.student = Student.objects.create(
            user=self.profile, class_unit=self.class_unit, parent=self.parent
        )

    def tearDown(self):
        Student.objects.filter(user=self.profile).delete()
        Parent.objects.filter(user=self.profile).delete()
        self.profile.delete()

    def test_student_creation(self):
        self.assertEqual(self.student.user, self.profile)
        self.assertEqual(self.student.class_unit, self.class_unit)
        self.assertEqual(self.student.parent, self.parent)

    def test_str_representation(self):
        expected_str = f"{self.user.first_name} \
            {self.user.last_name} - student"
        self.assertEqual(str(self.student), expected_str)

    def test_related_names(self):
        self.assertIn(self.student, self.parent.children.all())
        self.assertIn(self.student, self.class_unit.students_in_class.all())

    def test_limit_choices(self):
        invalid_user = User.objects.create_user(
            username="invaliduser", password="testpassword"
        )
        invalid_profile = Profile.objects.create(
            user=invalid_user, phone_number="987654321", 
            account_type=Profile.PARENT
        )

        with self.assertRaises(ValidationError):
            student = Student.objects.create(
                user=invalid_profile, class_unit=self.class_unit, 
                parent=self.parent
            )
            student.full_clean()

    def test_delete_user(self):
        student_id = self.student.id
        self.user.delete()
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=student_id)

    def test_delete_parent(self):
        parent_id = self.parent.id
        self.parent.delete()
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=parent_id)

    def test_delete_class_unit(self):
        self.class_unit.delete()
        Student.objects.get(pk=self.student.id)
