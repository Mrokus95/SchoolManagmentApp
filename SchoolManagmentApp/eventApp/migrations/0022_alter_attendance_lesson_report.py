# Generated by Django 4.2.3 on 2023-08-02 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0021_remove_attendance_student_name_attendance_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='lesson_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventApp.lessonreport'),
        ),
    ]
