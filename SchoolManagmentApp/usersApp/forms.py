from django import forms
from django.contrib.auth.models import User
from eventApp.models import Subject
from django.core.validators import validate_email
from .models import Student, Parent
import re



class RegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=9)
    photo = forms.ImageField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'photo', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

            # Check if passwords match
        if password1 != password2:
            self.add_error('password1', "Passwords do not match.")

        # Check if phone number has 9 digits and all signs are digits
        if phone_number and len(phone_number) != 9:
            self.add_error('phone_number', "Phone number has to be 9 digits.")
        
        if phone_number and not phone_number.isdigit():
            self.add_error('phone_number', "Phone number can only contains digits.")

        # Check if email is in a valid format
        if email:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if not re.fullmatch(regex, email):
                self.add_error('email', "Invalid email address.")


        # Check if email is unique
        if User.objects.filter(email=email).exists():
            self.add_error('email', "This email is already registered.")

        #Check if name and surname are in a valid format
        if not first_name.isalpha():
            self.add_error('first_name', "First name can only contains alphabetical characters.")
        
        if not last_name.isalpha():
            self.add_error('last_name', "Last name can only contains alphabetical characters.")
        
        return cleaned_data



class TeacherRegistrationForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ['name']


    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data['name']

        subject_exists = Subject.objects.get(name=subject).exists()

        if not subject_exists:
            self.add_error('name', "Subject does not exist.")
        
        return cleaned_data


class ParentRegistrationForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all())

    class Meta:
        model = Parent
        fields = ['student']

    def clean(self):
        cleaned_data = super().clean()

        student_id = self.cleaned_data['student'].id
        student_exists = Student.objects.filter(id=student_id).exists()

        if not student_exists:
            self.add_error('student', "Student does not exist.")
        
        return cleaned_data