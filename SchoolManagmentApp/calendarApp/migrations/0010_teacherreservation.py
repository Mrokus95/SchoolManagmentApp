# Generated by Django 4.2.3 on 2023-08-03 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0020_remove_lesson_day_remove_lesson_subject_and_more'),
        ('usersApp', '0008_alter_profile_photo'),
        ('calendarApp', '0009_lesson_classroom_reservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday')])),
                ('lesson_number', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('class_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersApp.classunit')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventApp.teacher')),
            ],
        ),
    ]
