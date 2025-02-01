from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from modeltranslation.admin import TranslationAdmin
from .models import Course, CourseSection, Instructor, Category, Path, CourseTest, CourseProgress, Question, Settings, DifficultyLevel, Quiz, QuizQuestion, QuizResult
#from .utils import parse_txt_file
import logging
import pandas as pd

# Loglash uchun logger
logger = logging.getLogger(__name__)


class CourseSectionInline(admin.TabularInline):
    model = CourseSection
    extra = 1
    ordering = ("order",)


# Kurslar uchun Admin Paneli
@admin.register(Course)
class CourseAdmin(TranslationAdmin):  # TranslationAdmin bilan tarjima qo‘llab-quvvatlanadi
    list_display = ("title", "instructor", "category", "created_at", "image_tag", 'slug')
    list_filter = ("category", "created_at")
    search_fields = ("title", "description")
    inlines = [CourseSectionInline]
    prepopulated_fields = {'slug': ('title',)}

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" style="width: 100px; height: auto;" />'
            )
        return "No Image"

    image_tag.short_description = "Image Preview"

# Instruktorlar uchun Admin Paneli
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Kategoriyalar uchun Admin Paneli
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Yo'nalishlar uchun Admin Paneli
@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

# Kurs bo'limlari uchun Admin Paneli
@admin.register(CourseSection)
class CourseSectionAdmin(TranslationAdmin):  # TranslationAdmin ishlatamiz
    list_display = ('title', 'course', 'order', 'has_additional_info', 'is_completed')
    list_filter = ('course',)
    search_fields = ('title', 'course__title', 'content')
    ordering = ('course', 'order')
    readonly_fields = ('duration',)

    def has_additional_info(self, obj):
        return bool(obj.additional_info)

    has_additional_info.boolean = True
    has_additional_info.short_description = "Qo'shimcha ma'lumot mavjudmi?"

    def is_completed(self, obj):
        return obj.is_completed

    is_completed.boolean = True
    is_completed.short_description = "Is Completed?"

# Savollar uchun Admin Paneli
@admin.register(Question)
class QuestionAdmin(TranslationAdmin):
    list_display = ('text', 'test', 'correct_answer')
    list_filter = ('test',)
    search_fields = ('text', 'correct_answer')
    ordering = ('test', 'text')
    list_editable = ('correct_answer',)

@admin.action(description='Mark selected progress as completed')
def mark_as_completed(modeladmin, request, queryset):
    queryset.update(is_completed=True)

@admin.action(description='Mark selected progress as not completed')
def mark_as_not_completed(modeladmin, request, queryset):
    queryset.update(is_completed=False)

@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_completed')
    list_filter = ('is_completed', 'course')
    search_fields = ('user__username', 'course__title')
    ordering = ('course', 'user')
    actions = [mark_as_completed, mark_as_not_completed]



@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("max_tests_per_user", "description")
    list_display_links = ("description",)
    list_editable = ("max_tests_per_user",)


@admin.register(CourseTest)
class CourseTestAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "is_virtual_lab", "import_questions_button")  # Buttonni qo'shish
    list_filter = ("course", "is_virtual_lab")
    search_fields = ("title", "description")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-excel/<int:test_id>/",
                self.admin_site.admin_view(self.import_questions_view),
                name="import_questions_from_excel",
            ),
        ]
        return custom_urls + urls

    def import_questions_view(self, request, test_id):
        test = CourseTest.objects.get(pk=test_id)
        if request.method == "POST" and "file" in request.FILES:
            excel_file = request.FILES["file"]
            try:
                data = pd.read_excel(excel_file)
                required_columns = ["Savol (uz)", "Savol (ru)", "To'g'ri javob (uz)", "To'g'ri javob (ru)",
                                    "Variant B (uz)", "Variant B (ru)", "Variant C (uz)", "Variant C (ru)",
                                    "Variant D (uz)", "Variant D (ru)"]

                if not all(col in data.columns for col in required_columns):
                    raise ValueError("Required columns are missing: " + ", ".join(required_columns))

                for _, row in data.iterrows():
                    Question.objects.create(
                        test=test,
                        text_uz=row["Savol (uz)"],
                        text_ru=row["Savol (ru)"],
                        correct_answer_uz=row["To'g'ri javob (uz)"],
                        correct_answer_ru=row["To'g'ri javob (ru)"],
                        option_a_uz=row["To'g'ri javob (uz)"],
                        option_a_ru=row["To'g'ri javob (ru)"],
                        option_b_uz=row["Variant B (uz)"],
                        option_b_ru=row["Variant B (ru)"],
                        option_c_uz=row.get("Variant C (uz)", ""),
                        option_c_ru=row.get("Variant C (ru)", ""),
                        option_d_uz=row.get("Variant D (uz)", ""),
                        option_d_ru=row.get("Variant D (ru)", ""),
                    )
                messages.success(request, "Savollar tarjima bilan yuklandi!")
                return redirect("..")
            except Exception as e:
                logger.error(f"Excel importida xatolik: {e}")
                messages.error(request, f"Xatolik: {e}")
        return render(request, "admin/import_questions.html", {"title": "Import Questions from Excel", "test": test})

    logger.debug("Admin file has been updated.")

    def import_questions_button(self, obj):
        url = reverse("admin:import_questions_from_excel", args=[obj.id])
        return format_html('<a class="button" href="{}">Import Questions from Excel</a>', url)

    import_questions_button.short_description = "Import Questions"

# @admin.register(Settings)
# class SettingsAdmin(admin.ModelAdmin):
#     list_display = ("id", "max_tests_per_course")  # `id` birinchi o'rinda
#     list_display_links = ("id",)  # `id` ustuniga havola berish
#     list_editable = ("max_tests_per_course",)  # Tahrir qilish mumkin

# @admin.register(Settings)
# class SettingsAdmin(admin.ModelAdmin):
#     list_display = ("max_tests_per_user", "description")  # Yana bir ustun qo'shildi
#     list_display_links = ("description",)  # "description" havola sifatida
#     list_editable = ("max_tests_per_user",)  # Foydalanuvchi tahrirlay oladi

def get_max_tests_per_user():
    settings = Settings.objects.first()  # Admin tomonidan sozlangan birinchi yozuvni olish
    return settings.max_tests_per_user if settings else 10  # Agar sozlama yo'q bo'lsa, standart qiymat


@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Ko'rsatishni xohlagan maydonlarni qo'shing
    search_fields = ('name',)  # Qidiruvni qo'llash uchun


@admin.register(Quiz)
class QuizAdmin(TranslationAdmin):
    list_display = ['title', 'section', 'max_questions', 'created_at']
    list_filter = ['section', 'created_at']
    search_fields = ['title', 'section__title']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'text', 'correct_answer']
    list_filter = ['quiz']
    search_fields = ['text', 'quiz__title']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'completed_at']
    list_filter = ['quiz', 'completed_at']
    search_fields = ['user__username', 'quiz__title']

