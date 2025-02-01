from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, null=True, blank=True)




class CourseActivity(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='user_activities')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_course_activities')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def duration(self):
        """
        Faollik davomiyligini hisoblash.
        """
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60  # Daqiqalarda
        return 0


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)  # Ism
    email = models.EmailField()  # Email
    message = models.TextField()  # Muammo yoki so‘rov
    created_at = models.DateTimeField(auto_now_add=True)  # Yuborilgan sana

    def __str__(self):
        return f"{self.name} - {self.email}"
