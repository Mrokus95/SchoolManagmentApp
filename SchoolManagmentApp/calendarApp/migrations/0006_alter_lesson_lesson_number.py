# Generated by Django 4.2.3 on 2023-08-01 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarApp', '0005_lesson_is_base_delete_weeklyschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_number',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')], default=1),
        ),
    ]
