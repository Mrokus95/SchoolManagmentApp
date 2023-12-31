# Generated by Django 4.2.3 on 2023-07-31 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0020_remove_lesson_day_remove_lesson_subject_and_more'),
        ('usersApp', '0007_alter_student_parent'),
        ('calendarApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklySchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.IntegerField()),
                ('is_base_schedule', models.BooleanField(default=False)),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersApp.classunit')),
            ],
        ),
        migrations.RemoveField(
            model_name='planoflesson',
            name='class_unit',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='day',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='order',
        ),
        migrations.AddField(
            model_name='lesson',
            name='classroom',
            field=models.CharField(default='Not assigned', max_length=50),
        ),
        migrations.AddField(
            model_name='lesson',
            name='day_of_week',
            field=models.IntegerField(choices=[(1, 'Poniedziałek'), (2, 'Wtorek'), (3, 'Środa'), (4, 'Czwartek'), (5, 'Piątek')], default=1),
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_number',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')], default=1),
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eventApp.teacher'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventApp.subject'),
        ),
        migrations.DeleteModel(
            name='Day',
        ),
        migrations.DeleteModel(
            name='PlanOfLesson',
        ),
        migrations.AddField(
            model_name='weeklyschedule',
            name='lessons',
            field=models.ManyToManyField(to='calendarApp.lesson'),
        ),
    ]
