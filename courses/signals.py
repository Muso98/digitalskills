from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CourseSection, CourseProgress

@receiver(post_save, sender=CourseSection)
def update_progress(sender, instance, **kwargs):
    course = instance.course
    user = instance.course.instructor  # O'zgartiring: foydalanuvchini aniqlash usuli
    total_sections = course.sections.count()
    completed_sections = total_sections  # Bu yerda bo'limning tugallanganligini kuzating

    if completed_sections == total_sections:
        progress, created = CourseProgress.objects.get_or_create(user=user, course=course)
        progress.is_completed = True
        progress.save()
