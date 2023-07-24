from django import forms
from django.forms.widgets import SelectDateWidget


class EventFilterForm(forms.Form):

    subject = forms.ChoiceField(choices=[
        ('empty', 'Empty'),
        ('math', 'Mathematic'),
        ('english', 'English')
    ], label='subject')

    event_type = forms.ChoiceField(choices=[
        ('empty', 'Empty'),
        ('other', 'Other'),
        ('small_test', 'Small Test'),
        ('test', 'Test'),
        ('essay', 'Essay'),
        ('project', 'Project')

    ], label='Event Type')

    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')