# Generated by Django 4.2.3 on 2023-08-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersApp', '0007_alter_student_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='users/avatars/musk.webp', upload_to='users/avatars/'),
        ),
    ]
