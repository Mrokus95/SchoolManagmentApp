from django.test import TestCase
from eventApp.models import Subject
from ..forms import (ProfileEditForm, RegistrationForm,
                     StudentRegistrationForm, TeacherRegistrationForm,
                     UserEditForm)
from ..models import ClassUnit, Parent, Profile, User


class RegistrationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "phone_number": "123456789",
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_passwords(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "differentpassword",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)
        self.assertIn("Passwords do not match.", form.errors["password1"])

    def test_invalid_phone_number(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "phone_number": "123",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)
        self.assertIn("Phone number has to be 9 digits.", 
                      form.errors["phone_number"])

    def test_invalid_phone_number_letters(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "phone_number": "123fds123",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)
        self.assertIn(
            "Phone number can only contains digits.", 
            form.errors["phone_number"]
        )

    def test_invalid_email(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "email": "invalidemail",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_invalid_email(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "email": "invalidemail@gmailcom",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_duplicate_email(self):
        existing_user = User.objects.create(
            username="existinguser",
            email="existing@example.com",
            password="existingpassword",
        )

        form_data = {
            "username": "testuser2",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123456789",
            "email": "existing@example.com",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("This email is already registered.", 
                      form.errors["email"])

    def test_invalid_name(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "123",
            "last_name": "Doe",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)
        self.assertIn(
            "First name can only contains alphabetical characters.",
            form.errors["first_name"],
        )

    def test_invalid_name_mixed(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Mike123",
            "last_name": "Doe",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)
        self.assertIn(
            "First name can only contains alphabetical characters.",
            form.errors["first_name"],
        )

    def test_invalid_name_surname(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Mike",
            "last_name": "123",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)
        self.assertIn(
            "Last name can only contains alphabetical characters.",
            form.errors["last_name"],
        )

    def test_invalid_name_surname_mixed(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Mike",
            "last_name": "Doe123",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)
        self.assertIn(
            "Last name can only contains alphabetical characters.",
            form.errors["last_name"],
        )


class TeacherRegistrationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.profile = Profile.objects.create(
            user=self.user, phone_number="123456789", 
            account_type=Profile.TEACHER
        )

    def test_valid_form_single_subject(self):
        Subject.objects.create(name="MATHEMATIC")
        available_subjects = Subject.objects.all()
        form_data = {
            "name": [available_subjects[0].id],
        }
        form = TeacherRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_mulitple_subject(self):
        Subject.objects.create(name="MATHEMATIC")
        Subject.objects.create(name="ENGLISH")
        available_subjects = Subject.objects.all()
        form_data = {
            "name": [available_subjects[0].id, available_subjects[1].id],
        }
        form = TeacherRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_mulitple_subject_mixed(self):
        Subject.objects.create(name="MATHEMATIC")
        Subject.objects.create(name="ENGLISH")
        invalid_subject = 999
        available_subjects = Subject.objects.all()
        form_data = {
            "name": [
                available_subjects[0].id,
                available_subjects[1].id,
                invalid_subject,
            ],
        }
        form = TeacherRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("Some selected subjects are not valid.", 
                      form.errors["name"])

    def test_invalid_subject(self):
        invalid_subject = 999
        form_data = {
            "name": [invalid_subject],
        }
        form = TeacherRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("Some selected subjects are not valid.", 
                      form.errors["name"])

    def test_invalid_object(self):
        form_data = {
            "name": ["invalid_subject_object"],
        }
        form = TeacherRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn(
            "“invalid_subject_object” is not a valid value.", 
            form.errors["name"]
        )


class StudentRegistrationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.profile = Profile.objects.create(
            user=self.user, phone_number="123456789", 
            account_type=Profile.PARENT
        )
        self.parent = Parent.objects.create(user=self.profile)
        self.class_unit = ClassUnit.objects.create(start_year=2023, 
                                                   letter_mark="A")

    def test_valid_form(self):
        form_data = {
            "class_unit": self.class_unit.id,
            "parent": self.parent.id,
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_parent(self):
        invalid_parent_id = self.parent.id + 112256
        form_data = {
            "class_unit": self.class_unit.id,
            "parent": invalid_parent_id,
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("parent", form.errors)
        self.assertIn("Parent does not exist.", form.errors["parent"])

    def test_invalid_class_unit(self):
        invalid_class_unit_id = self.class_unit.id + 112256
        form_data = {
            "class_unit": invalid_class_unit_id,
            "parent": self.parent.id,
        }
        form = StudentRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("class_unit", form.errors)
        self.assertIn("Class does not exist.", form.errors["class_unit"])


class UserEditFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", 
            email="testuser@gmail.com"
        )

    def test_valid_form(self):
        form_data = {
            "email": "testuser2@gmail.com",
        }
        form = UserEditForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_without_a(self):
        form_data = {
            "email": "testuser2gmail.com",
        }
        form = UserEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_invalid_form_without_dot(self):
        form_data = {
            "email": "testuser2@gmailcom",
        }
        form = UserEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_invalid_form_muiltiple_a(self):
        form_data = {
            "email": "testus@er2@gmailcom",
        }
        form = UserEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_invalid_form_no_prefix(self):
        form_data = {
            "email": "@gmailcom",
        }
        form = UserEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_if_email_changed(self):
        new_email = self.user.email
        self.assertTrue(new_email, "testuser2@gmail.com")


class ProfileEditFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", 
            email="testuser@gmail.com"
        )
        self.profile = Profile.objects.create(
            user=self.user, phone_number="123456789", 
            account_type=Profile.STUDENT
        )

    def test_valid_form(self):
        form_data = {
            "phone_number": "582365896",
        }
        form = ProfileEditForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_too_short(self):
        form_data = {
            "phone_number": "5823658",
        }
        form = ProfileEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Phone number has to be 9 digits.", 
                      form.errors["phone_number"])

    def test_invalid_form_with_letters(self):
        form_data = {
            "phone_number": "5823653f8",
        }
        form = ProfileEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Phone number can only contain digits.", 
            form.errors["phone_number"]
        )

    def test_if_email_changed(self):
        new_phone_number = self.profile.phone_number
        self.assertTrue(new_phone_number, "582365896")
