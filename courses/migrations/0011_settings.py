# Generated by Django 5.1.4 on 2025-01-07 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_question_virtuallabresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_tests_per_course', models.PositiveIntegerField(default=10, verbose_name='Max Tests Per Course')),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
