# Generated by Django 4.2.3 on 2023-08-03 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0023_alter_attendance_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevents',
            name='event_type',
            field=models.CharField(choices=[('Other', 'Other'), ('Small Test', 'Small Test'), ('Test', 'Test'), ('Essay', 'Essay'), ('Project', 'Project')], default='Other'),
        ),
    ]
