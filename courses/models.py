from django.db import models
import os
import cv2
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


def get_video_duration_opencv(file_path):
    try:
        video = cv2.VideoCapture(file_path)
        if not video.isOpened():
            raise Exception("Could not open video file.")

        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)
        video.release()
        duration_seconds = frames / fps if fps > 0 else 0

        hours, remainder = divmod(int(duration_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"
    except Exception:
        return "00:00"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Path(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DifficultyLevel(models.Model):
    LEVELS = [
        ('easy', 'Oson'),
        ('medium', 'O‘rtacha'),
        ('hard', 'Qiyin'),
    ]
    name = models.CharField(max_length=20, choices=LEVELS, unique=True)

    def __str__(self):
        return self.get_name_display()


class Course(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)  # Slug maydoni
    image = models.ImageField(upload_to='course_section_images/', blank=True, null=True)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, related_name='courses', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    path = models.ForeignKey(Path, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    difficulty_level = models.ForeignKey(DifficultyLevel, related_name='courses', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.difficulty_level.get_name_display()}"

    def total_duration(self):
        total_seconds = 0
        for section in self.sections.all():
            if section.duration:  # `None` qiymatlarni tekshirish
                parts = section.duration.split(":")
                if len(parts) == 2:  # MM:SS formati
                    minutes, seconds = map(int, parts)
                    total_seconds += minutes * 60 + seconds
                elif len(parts) == 3:  # HH:MM:SS formati
                    hours, minutes, seconds = map(int, parts)
                    total_seconds += hours * 3600 + minutes * 60 + seconds

        # Sekundlarni soat, minut va sekundlarga ajratish
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Formatni qaytarish
        if hours > 0:
            return f"{hours} hours {minutes} minutes {seconds} seconds"
        else:
            return f"{minutes} minutes {seconds} seconds"



class CourseSection(models.Model):
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    additional_info = RichTextField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)  # Foydalanuvchi ushbu bo‘limni tugatganmi?

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.video_file and not self.duration:
            if os.path.exists(self.video_file.path):
                self.duration = get_video_duration_opencv(self.video_file.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class CourseTest(models.Model):
    course = models.ForeignKey(Course, related_name='tests', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_virtual_lab = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    test = models.ForeignKey(CourseTest, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, blank=True, null=True)
    option_d = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.text


class CourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)

    @staticmethod
    def can_access(user, section):
        previous_sections = CourseSection.objects.filter(course=section.course, order__lt=section.order)
        return all(
            CourseSectionProgress.objects.filter(user=user, section=prev_section, is_completed=True).exists()
            for prev_section in previous_sections
        )

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({'Completed' if self.is_completed else 'In Progress'})"


class CourseSectionProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='section_progress')
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'section'], name='unique_section_progress_per_user')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.section.title} ({'Completed' if self.is_completed else 'Not Completed'})"


class Settings(models.Model):
    max_tests_per_user = models.PositiveIntegerField(default=10)
    max_tests_per_course = models.PositiveIntegerField(default=10)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Settings (Max Tests per User: {self.max_tests_per_user}, Max Tests per Course: {self.max_tests_per_course})"


@receiver(pre_save, sender=CourseTest)
def limit_tests_per_course(sender, instance, **kwargs):
    settings = Settings.objects.first()
    max_tests = settings.max_tests_per_course if settings else 10
    if instance.course and instance.course.tests.exclude(id=instance.id).count() >= max_tests:
        raise ValidationError(f"Bir kurs uchun maksimal {max_tests} ta test qo'shilishi mumkin.")




class Quiz(models.Model):
    section = models.ForeignKey(
        'CourseSection',
        related_name='quizzes',
        on_delete=models.CASCADE
    )  # Viktorina qaysi bo'limga tegishli
    title = models.CharField(max_length=200)  # Viktorina nomi
    description = RichTextField(blank=True, null=True)  # Asosiy ma'lumotlar maydoni
    max_questions = models.PositiveIntegerField(default=5)  # Maksimal savollar soni
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.section.title} - {self.title}"


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE
    )  # Qaysi viktorinaga tegishli
    text = models.TextField()  # Savol matni
    correct_answer = models.BooleanField()  # To‘g‘ri javob (True/False)

    def __str__(self):
        return f"{self.quiz.title} - {self.text}"


class QuizResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='quiz_results',
        on_delete=models.CASCADE
    )  # Foydalanuvchi
    quiz = models.ForeignKey(
        Quiz,
        related_name='results',
        on_delete=models.CASCADE
    )  # Viktorina
    score = models.PositiveIntegerField()  # To‘plangan ball
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
