# Generated by Django 4.2.3 on 2023-07-23 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0002_alter_profile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='klasa',
        ),
        migrations.AddField(
            model_name='classunit',
            name='student',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.DO_NOTHING, related_name='students_in_class', to='usersApp.student'),
            preserve_default=False,
        ),
    ]
