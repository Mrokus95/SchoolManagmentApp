import re
from django import forms
from django.contrib.auth.models import User
from eventApp.models import Subject, Teacher
from .models import ClassUnit, Parent, Profile, Student


class RegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=9)
    photo = forms.ImageField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), 
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), 
                                label="Confirm password")

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "photo",
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if password1 != password2:
            self.add_error("password1", "Passwords do not match.")

        if phone_number and len(phone_number) != 9:
            self.add_error("phone_number", 
                           "Phone number has to be 9 digits.")

        if phone_number and not phone_number.isdigit():
            self.add_error("phone_number", 
                           "Phone number can only contains digits.")

        if email:
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
            if not re.fullmatch(regex, email):
                self.add_error("email", "Invalid email address.")

        if User.objects.filter(email=email).exists():
            self.add_error("email", "This email is already registered.")

        if not first_name.isalpha():
            self.add_error(
                "first_name", 
                "First name can only contains alphabetical characters."
            )

        if not last_name.isalpha():
            self.add_error(
                "last_name", 
                "Last name can only contains alphabetical characters."
            )

        return cleaned_data


class TeacherRegistrationForm(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all().order_by("name"),
        label="Subjects",
        widget=forms.CheckboxSelectMultiple,
        error_messages={"invalid_choice": 
                        "Some selected subjects are not valid."},
    )

    class Meta:
        model = Teacher
        fields = ["name"]

    def clean(self):
        cleaned_data = super().clean()
        selected_subjects = cleaned_data.get("name")

        if selected_subjects:
            available_subjects = Subject.objects.filter(
                pk__in=[subject.pk for subject in selected_subjects]
            )
            if len(selected_subjects) != len(available_subjects):
                self.add_error("name", "invalid_choice")
        return cleaned_data


class StudentRegistrationForm(forms.ModelForm):
    class_unit = forms.ModelChoiceField(
        queryset=ClassUnit.objects.all(),
        label="Class:",
        error_messages={"invalid_choice": "Class does not exist."},
    )
    parent = forms.ModelChoiceField(
        queryset=Parent.objects.all(),
        label="Parent:",
        error_messages={"invalid_choice": "Parent does not exist."},
    )

    class Meta:
        model = Student
        fields = ["class_unit", "parent"]

    def clean(self):
        cleaned_data = super().clean()

        parent = cleaned_data.get("parent")
        if parent:
            parent_exists = Parent.objects.filter(id=parent.id).exists()
            if not parent_exists:
                self.add_error("parent", "Parent does not exist.")

        class_unit = cleaned_data.get("class_unit")
        if class_unit:
            class_exists = ClassUnit.objects.filter(id=class_unit.id).exists()
            if not class_exists:
                self.add_error("class_unit", "Class does not exist.")

        return cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        # Check if email is in a valid format
        if email:
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
            if not re.fullmatch(regex, email):
                self.add_error("email", "Enter a valid email address.")

        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number"]

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")

        if phone_number and len(phone_number) != 9:
            self.add_error("phone_number", 
                           "Phone number has to be 9 digits.")

        if phone_number and not phone_number.isdigit():
            self.add_error("phone_number", 
                           "Phone number can only contain digits.")

        return cleaned_data
