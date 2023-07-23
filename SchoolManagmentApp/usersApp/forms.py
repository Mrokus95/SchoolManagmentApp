from django import forms
from django.contrib.auth.models import User
from .models import ClassUnit, Student, Profile


class MyRegistrationForm(forms.ModelForm):
    class_id = forms.ModelChoiceField(queryset=ClassUnit.objects.all(), empty_label="Select a class")
    account_type = forms.ChoiceField(choices=Profile.TYPE_ACCOUNT_CHOICES)
    phone_number = forms.CharField(max_length=9)
    photo = forms.ImageField()
    password1 = forms.CharField(max_length=9, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=9, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'photo', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number', 'account_type', 'class_id']
