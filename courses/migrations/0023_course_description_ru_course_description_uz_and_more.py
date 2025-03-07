# Generated by Django 5.1.5 on 2025-02-01 05:03

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_alter_course_slug_alter_course_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='description_uz',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='title_uz',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='content_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='content_uz',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='title_ru',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='title_uz',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='description_ru',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='description_uz',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='title_ru',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='title_uz',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
