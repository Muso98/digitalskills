# Generated by Django 5.1.3 on 2024-12-26 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_coursesection_video_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursesection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course_section_images/'),
        ),
    ]
