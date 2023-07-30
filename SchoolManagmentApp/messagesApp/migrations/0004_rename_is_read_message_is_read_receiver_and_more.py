# Generated by Django 4.2.3 on 2023-07-30 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagesApp', '0003_message_is_delete_receiver_message_is_delete_sender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='is_read',
            new_name='is_read_receiver',
        ),
        migrations.RemoveField(
            model_name='message',
            name='is_trash',
        ),
        migrations.AddField(
            model_name='message',
            name='is_read_sender',
            field=models.BooleanField(default=False),
        ),
    ]
