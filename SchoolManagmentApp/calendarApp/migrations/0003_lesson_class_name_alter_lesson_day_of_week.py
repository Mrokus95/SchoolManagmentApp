# Generated by Django 4.2.3 on 2023-08-01 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0007_alter_student_parent'),
        ('calendarApp', '0002_weeklyschedule_remove_planoflesson_class_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='class_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='usersApp.classunit'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='day_of_week',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday')], default=1),
        ),
    ]
