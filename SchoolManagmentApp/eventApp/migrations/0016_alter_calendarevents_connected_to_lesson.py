# Generated by Django 4.2.3 on 2023-07-25 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventApp', '0015_alter_subject_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevents',
            name='connected_to_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='related_lesson', to='eventApp.lessonreport'),
        ),
    ]