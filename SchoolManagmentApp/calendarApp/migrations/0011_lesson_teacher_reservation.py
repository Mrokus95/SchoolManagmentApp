# Generated by Django 4.2.3 on 2023-08-03 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendarApp', '0010_teacherreservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='teacher_reservation',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='calendarApp.teacherreservation'),
            preserve_default=False,
        ),
    ]