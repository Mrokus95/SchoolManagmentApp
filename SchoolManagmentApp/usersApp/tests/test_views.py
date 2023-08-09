from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Profile, ClassUnit, Student, Parent
from eventApp.models import Teacher, Subject
from ..forms import UserEditForm, ProfileEditForm
from django.contrib.auth.tokens import default_token_generator

class HomeViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='testpassword1')
        self.parent_profile = Profile.objects.create(user=self.user, account_type=Profile.PARENT)
        self.parent = Parent.objects.create(user=self.parent_profile)

        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')

        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.student_profile = Profile.objects.create(user=self.user2, account_type=Profile.STUDENT)
        self.student = Student.objects.create(user=self.student_profile, class_unit=self.class_unit, parent=self.parent)
        self.client = Client()
        self.home_url = reverse('home')
        
    def test_get_home_as_unauthenticated_user(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, '<button id="login-nav-btn" class="login-nav-btn">Login</button>')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_failed(self):
        self.client.login(username= 'invalid', password= 'testpassword1')
        response = self.client.post(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, '<button id="login-nav-btn" class="login-nav-btn">Login</button>')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_get_home_as_authenticated_user(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('view_schedule'))
        self.assertEqual(response.status_code, 302)



class CustomPasswordResetViewTest(TestCase):
    def setUp(self):
        self.password_reset_url = reverse('password_reset')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_password_reset_view(self):
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_form.html')
    
    def test_password_reset_success(self):
        response = self.client.post(self.password_reset_url, {'email': self.user.email})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_form.html')
    
class CustomPasswordResetDoneViewTest(TestCase):
    def test_password_reset_done_view(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_done.html')

class CustomPasswordResetConfirmViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.uid = str(self.user.id)
        self.token = default_token_generator.make_token(self.user)
        self.password_reset_confirm_url = reverse('password_reset_confirm', args=[self.uid, self.token])
    
    def test_password_reset_confirm_view(self):
        response = self.client.get(self.password_reset_confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_confirm.html')
    
    def test_password_reset_confirm_success(self):
        new_password = 'newtestpassword'
        response = self.client.post(self.password_reset_confirm_url, {
            'new_password1': new_password,
            'new_password2': new_password,
        })
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'password_reset_confirm.html')
        self.assertTemplateUsed(response, 'base.html')

class CustomPasswordResetCompleteViewTest(TestCase):
    def test_password_reset_complete_view(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_complete.html')


class RegistrationCompleteTest(TestCase):
 
    def setUp(self):
        #Creating admin account
        self.admin = User.objects.create_user(username='testuser1', password='testpassword1', is_staff=True)
        self.admin_profile = Profile.objects.create(user=self.admin, account_type=Profile.ADMIN)


        self.user = User.objects.create_user(username='testuser2', password='testpassword2')
        self.parent_profile = Profile.objects.create(user=self.user, account_type=Profile.PARENT)
        self.parent = Parent.objects.create(user=self.parent_profile)

        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')

        self.user2 = User.objects.create_user(username='testuser3', password='testpassword3')
        self.student_profile = Profile.objects.create(user=self.user2, account_type=Profile.STUDENT)
        self.student = Student.objects.create(user=self.student_profile, class_unit=self.class_unit, parent=self.parent)
        self.client = Client()
        self.registration_url = reverse('registration_complete')

    def test_get_no_permissions(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_with_permissions(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_complete.html')
        self.assertTemplateUsed(response, 'base.html')


class ParentRegisterViewTest(TestCase):
 
    def setUp(self):

        self.admin = User.objects.create_user(username='testuser1', password='testpassword1', is_staff=True)
        self.admin_profile = Profile.objects.create(user=self.admin, account_type=Profile.ADMIN)


        self.user = User.objects.create_user(username='testuser2', password='testpassword2')
        self.parent_profile = Profile.objects.create(user=self.user, account_type=Profile.PARENT)
        self.parent = Parent.objects.create(user=self.parent_profile)

        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')

        self.user2 = User.objects.create_user(username='testuser3', password='testpassword3')
        self.student_profile = Profile.objects.create(user=self.user2, account_type=Profile.STUDENT)
        self.student = Student.objects.create(user=self.student_profile, class_unit=self.class_unit, parent=self.parent)
        self.client = Client()
        self.parent_registration_url = reverse('register_parent')

    def test_get_no_permissions(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.parent_registration_url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_with_permissions(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(self.parent_registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_successful_registration_redirecting(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newparent',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newparent@gmail.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'phone_number': '123456789',
        }
        response = self.client.post(self.parent_registration_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('registration_complete'))

    def test_invalid_registration(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newparent',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newparentgmail.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'phone_number': '1234569',
        }
        response = self.client.post(self.parent_registration_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
    
        for field_name, field_errors in response.context    ['registration_form'].errors.items():
            for error in field_errors:
                self.assertContains(response, str(error))

    def test_successful_registration_objects_created(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newparent2',
            'first_name': 'Mike',
            'last_name': 'Smith',
            'email': 'newparent2@gmail.com',
            'password1': 'securepassword2',
            'password2': 'securepassword2',
            'phone_number': '123456459',
        }
        response = self.client.post(self.parent_registration_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('registration_complete'))
        
        user = User.objects.get(username=data['username'])
        profile = Profile.objects.get(user=user)
        parent = Parent.objects.get(user=profile)
        
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])

        self.assertEqual(profile.phone_number, data['phone_number'])
        self.assertEqual(profile.account_type, 'Parent')

        self.assertEqual(parent.user, profile)


class TeacherRegisterViewTest(TestCase):
 
    def setUp(self):

        self.admin = User.objects.create_user(username='testuser1', password='testpassword1', is_staff=True)
        self.admin_profile = Profile.objects.create(user=self.admin, account_type=Profile.ADMIN)


        self.user = User.objects.create_user(username='testuser2', password='testpassword2')
        self.parent_profile = Profile.objects.create(user=self.user, account_type=Profile.PARENT)
        self.parent = Parent.objects.create(user=self.parent_profile)

        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')

        self.user2 = User.objects.create_user(username='testuser3', password='testpassword3')
        self.student_profile = Profile.objects.create(user=self.user2, account_type=Profile.STUDENT)
        self.student = Student.objects.create(user=self.student_profile, class_unit=self.class_unit, parent=self.parent)
        self.client = Client()
        self.teacher_registration_url = reverse('register_teacher')

        self.subject = Subject.objects.create(name='ENGLISH')

    def test_get_no_permissions(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.teacher_registration_url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_with_permissions(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(self.teacher_registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_successful_registration_redirecting(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newteacher',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newteacher@gmail.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'phone_number': '123456789',
            'name': self.subject.id,
        }
        response = self.client.post(self.teacher_registration_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('registration_complete'))

    def test_invalid_registration(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newteacher',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newparentgmail.com',
            'password1': 'securepasswor',
            'password2': 'securepassword',
            'phone_number': '1234569',
            'name': self.subject.id,
        }
        response = self.client.post(self.teacher_registration_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
    
        for field_name, field_errors in response.context    ['registration_form'].errors.items():
            for error in field_errors:
                self.assertContains(response, str(error))

    def test_successful_registration_objects_created(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newteacher',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newteacher@gmail.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'phone_number': '123456789',
            'name': self.subject.id,
        }
        response = self.client.post(self.teacher_registration_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('registration_complete'))
        
        user = User.objects.get(username=data['username'])
        profile = Profile.objects.get(user=user)
        teacher = Teacher.objects.get(user=profile)
        
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])

        self.assertEqual(profile.phone_number, data['phone_number'])
        self.assertEqual(profile.account_type, 'Teacher')

        self.assertEqual(teacher.user, profile)


class StudentRegisterViewTest(TestCase):
 
    def setUp(self):
        self.admin = User.objects.create_user(username='testuser1', password='testpassword1', is_staff=True)
        self.admin_profile = Profile.objects.create(user=self.admin, account_type=Profile.ADMIN)


        self.user = User.objects.create_user(username='testuser2', password='testpassword2')
        self.parent_profile = Profile.objects.create(user=self.user, account_type=Profile.PARENT)
        self.parent = Parent.objects.create(user=self.parent_profile)

        self.user = User.objects.create_user(username='testuser4', password='testpassword4')
        self.parent_profile2 = Profile.objects.create(user=self.user, account_type=Profile.PARENT)
        self.parent2 = Parent.objects.create(user=self.parent_profile2)

        self.class_unit = ClassUnit.objects.create(start_year=2023, study_year=1, letter_mark='A')

        self.user2 = User.objects.create_user(username='testuser3', password='testpassword3')
        self.student_profile = Profile.objects.create(user=self.user2, account_type=Profile.STUDENT)
        self.student = Student.objects.create(user=self.student_profile, class_unit=self.class_unit, parent=self.parent)
        self.client = Client()
        self.student_registration_url = reverse('register_student')

        self.subject = Subject.objects.create(name='ENGLISH')

    def test_get_no_permissions(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.student_registration_url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_with_permissions(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(self.student_registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_successful_registration_redirecting(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newstudent',
            'first_name': 'David',
            'last_name': 'Doe',
            'email': 'newstudent@gmail.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'phone_number': '123456789',
            'parent': self.parent2.id,
            'class_unit': self.class_unit.id
        }
        response = self.client.post(self.student_registration_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('registration_complete'))

    def test_invalid_registration(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newstudent',
            'first_name': 'David43',
            'last_name': 'Doe',
            'email': 'newstudent@gmailcom',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'phone_number': '123456',
            'parent': self.parent2.id,
            'class_unit': self.class_unit.id
        }
        response = self.client.post(self.student_registration_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
    
        for field_name, field_errors in response.context    ['registration_form'].errors.items():
            for error in field_errors:
                self.assertContains(response, str(error))

    def test_successful_registration_objects_created(self):
        self.client.login(username='testuser1', password='testpassword1')
        data = {
            'username': 'newstudent',
            'first_name': 'David',
            'last_name': 'Doe',
            'email': 'newstudent@gmail.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
            'phone_number': '123456789',
            'parent': self.parent2.id,
            'class_unit': self.class_unit.id
        }
        response = self.client.post(self.student_registration_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('registration_complete'))
        
        user = User.objects.get(username=data['username'])
        profile = Profile.objects.get(user=user)
        student = Student.objects.get(user=profile)
        
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])

        self.assertEqual(profile.phone_number, data['phone_number'])
        self.assertEqual(profile.account_type, 'Student')

        self.assertEqual(student.user, profile)
        self.assertEqual(student.class_unit.id, data['class_unit'])
        self.assertEqual(student.parent.id, data['parent'])


class EditUserDataViewTest(TestCase):
 
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpassword', email = 'test@gmail.com')
        self.parent_profile = Profile.objects.create(user=self.user, phone_number='549200023', account_type=Profile.PARENT)
        self.parent = Parent.objects.create(user=self.parent_profile)
        self.url = reverse('update_user_profile')
        self.client = Client()

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home') + f'?next={self.url}')

    def test_authenticated_user_can_access(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertIsInstance(response.context['user_form'], UserEditForm)
        self.assertIsInstance(response.context['profile_form'], ProfileEditForm)

    def test_form_initial_values(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        user_form = response.context['user_form']
        profile_form = response.context['profile_form']

        self.assertEqual(user_form['email'].value(), 'test@gmail.com')
        self.assertEqual(profile_form['phone_number'].value(), '549200023')

    def test_successful_updating(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'email': 'newstudent43@gmail.com',
            'phone_number': '123456789',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertContains(response, 'Profile updated successfully.')

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data['email'])
        self.assertEqual(self.user.profile.phone_number, data['phone_number'])


    def test_invalid_updating(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'email': 'newstudentgmailcom',
            'phone_number': '12345f789',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertNotContains(response, 'Profile updated successfully.')

class CustomPasswordChangeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('passwordChange')
        self.client = Client()
        
    def get_password_changing_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home') + f'?next={self.url}')
        self.assertContains(response, 'Login')

    def get_password_changing_authorized(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change_form.html')
        self.assertContains(response, 'Change Password')

    def test_password_changing_success(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'old_password': 'testpassword',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword',
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse('passwordChangeDone'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your password has been changed.')

    def test_password_changing_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'old_password': 'wrongpassword',
            'new_password1': 'newtestpassword',
            'new_password2': 'differentnewtestpassword',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change_form.html')
        self.assertContains(response, 'The two password fields didn’t match.')

class CustomPasswordChangeDoneViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('passwordChangeDone')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_password_change_confirmation_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_change_done.html')
        self.assertContains(response, 'Your password has been changed.')

    def get_password_change_confirmation_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home') + f'?next={self.url}')
        self.assertContains(response, 'Login')