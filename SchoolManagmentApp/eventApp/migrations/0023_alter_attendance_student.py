# Generated by Django 4.2.3 on 2023-08-02 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0007_alter_student_parent'),
        ('eventApp', '0022_alter_attendance_lesson_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersApp.student'),
        ),
    ]
