# Generated by Django 5.1.4 on 2025-01-29 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_contactmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='contactmessage',
            name='last_name',
        ),
    ]
