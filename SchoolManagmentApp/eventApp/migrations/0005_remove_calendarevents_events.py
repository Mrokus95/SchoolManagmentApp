# Generated by Django 4.2.3 on 2023-07-23 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0004_alter_calendarevents_event_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendarevents',
            name='events',
        ),
    ]
