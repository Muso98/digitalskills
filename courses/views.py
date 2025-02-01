from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from .models import Course, CourseSection, CourseTest, Question, CourseProgress, DifficultyLevel, CourseSectionProgress, Quiz, QuizQuestion, QuizResult
from .utils import get_max_tests_per_user
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Sum
from django.utils.translation import get_language
import random
import slug



def not_found(request):
    return render(request, 'courses/not_found.html', {'error': 'Course not found.'})

def course_filter_grid(request):
    lang = get_language()  # Joriy tilni olish

    courses = Course.objects.select_related('category', 'difficulty_level')

    # Tilga mos kurs nomini chiqarish
    for course in courses:
        if lang == "ru":
            course.title = course.title_ru  # Ruscha nom
            course.description = course.description_ru
        else:
            course.title = course.title_uz  # O‘zbekcha nom (asosiy)

    return render(request, 'courses/course-filter-grid.html', {
        'courses': courses,
        'lang': lang
    })




@login_required
def course_single(request, slug, section_id=None):
    lang = get_language()  # Joriy tilni olish
    course = get_object_or_404(Course, slug=slug)
    progress = CourseProgress.objects.filter(user=request.user, course=course).first()
    sections = CourseSection.objects.filter(course=course).order_by('order')
    is_completed = progress.is_completed if progress else False
    active_section = None
    additional_info = RichTextUploadingField(blank=True, null=True)

    tests = CourseTest.objects.filter(course=course)

    available_tests = tests if is_completed else []

    if section_id:
        active_section = get_object_or_404(CourseSection, id=section_id, course=course)
    else:
        active_section = sections.first()

    previous_section = sections.filter(order__lt=active_section.order).last()
    next_section = sections.filter(order__gt=active_section.order).first()

    section_progress = {
        section.id: CourseSectionProgress.objects.filter(user=request.user, section=section, is_completed=True).exists()
        for section in sections
    }

    can_access_next = (
        CourseSectionProgress.objects.filter(user=request.user, section=active_section, is_completed=True).exists()
    )

    next_section = (
        sections.filter(order__gt=active_section.order)
        .first() if CourseSectionProgress.objects.filter(user=request.user, section=active_section,
                                                         is_completed=True).exists() else None
    )

    if lang == "ru":
        course.title = course.title_ru
        course.description = course.description_ru
        for section in sections:
            section.title = section.title_ru
            section.content = section.content_ru
    else:
        course.title = course.title_uz
        course.description = course.description_uz

    return render(request, 'courses/course-single.html', {
        'course': course,
        'lang': lang,
        'sections': sections,
        'active_section': active_section,
        'additional_info': additional_info,
        'previous_section': previous_section,
        'next_section': next_section if section_progress.get(active_section.id, False) else None,
        'tests': available_tests,
        'is_completed': is_completed,
        'section_progress': section_progress,
    })



def update_course_progress(user, course):
    sections = course.sections.all()
    completed_sections = CourseSectionProgress.objects.filter(user=user, section__in=sections, is_completed=True).count()
    if completed_sections == sections.count():  # Agar barcha bo‘limlar tugallangan bo‘lsa
        CourseProgress.objects.update_or_create(user=user, course=course, defaults={'is_completed': True})
    else:  # Tugallanmagan bo‘lsa
        CourseProgress.objects.update_or_create(user=user, course=course, defaults={'is_completed': False})


@login_required
def complete_section(request, section_id):
    section = get_object_or_404(CourseSection, id=section_id)

    progress, created = CourseSectionProgress.objects.get_or_create(user=request.user, section=section)
    if not progress.is_completed:
        progress.is_completed = True
        progress.save()

    # Kursning umumiy progressini yangilash
    update_course_progress(request.user, section.course)

    # Keyingi bo‘limni aniqlash
    next_section = CourseSection.objects.filter(
        course=section.course,
        order__gt=section.order
    ).first()

    if next_section:
        # Agar keyingi bo‘lim mavjud bo‘lsa
        messages.success(request, _("Bo'lim tugallandi! Endi keyingi darsga kirishingiz mumkin."))
        return redirect('courses:course_single_section', slug=section.course.slug, section_id=next_section.id)
    else:
        # Agar keyingi bo‘lim mavjud bo‘lmasa, kurs sahifasiga qaytish
        messages.success(request, _("Bo'lim tugallandi! Siz kursni tugatdingiz."))
        return redirect('courses:course_single', slug=section.course.slug)


@login_required
def course_test(request, slug, test_id):
    course = get_object_or_404(Course, slug=slug)
    test = get_object_or_404(CourseTest, id=test_id, course=course)
    session_questions_key = f"test_{test_id}_questions"
    session_answers_key = f"test_{test_id}_progress"

    questions_in_session = request.session.get(session_questions_key, [])
    if not questions_in_session:
        max_tests = get_max_tests_per_user()
        questions = list(test.questions.all())
        random.shuffle(questions)
        questions_in_session = [q.id for q in questions[:max_tests]]
        request.session[session_questions_key] = questions_in_session
        request.session[session_answers_key] = {}

    user_answers = request.session.get(session_answers_key, {})

    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("question_"):
                question_id = key.split("_")[1]
                user_answers[str(question_id)] = value
        request.session[session_answers_key] = user_answers

        if len(user_answers) == len(questions_in_session):
            return redirect('courses:course_test_result', slug=course.slug, test_id=test.id)

        messages.success(request, _("Javobingiz saqlandi."))
        return redirect('courses:course_test', slug=course.slug, test_id=test.id)

    questions = Question.objects.filter(id__in=questions_in_session)
    questions_with_options = []
    for question in questions:
        options = [question.option_a, question.option_b, question.option_c, question.option_d]
        random.shuffle(options)
        questions_with_options.append({'question': question, 'options': options})

    return render(request, 'courses/test.html', {
        'course': course,
        'test': test,
        'questions_with_options': questions_with_options,
    })


@login_required
def course_test_result(request, slug, test_id):
    lang = get_language()
    course = get_object_or_404(Course, slug=slug)
    test = get_object_or_404(CourseTest, id=test_id, course=course)
    session_questions_key = f"test_{test_id}_questions"
    session_answers_key = f"test_{test_id}_progress"

    questions_in_session = request.session.pop(session_questions_key, [])
    user_answers = request.session.pop(session_answers_key, {})

    if not questions_in_session:
        messages.error(request, _("Siz testni tugatmadingiz!"))
        return redirect('courses:course_single', slug=course.slug)

    questions = Question.objects.filter(id__in=questions_in_session)
    correct_answers = 0
    for question in questions:
        user_answer = user_answers.get(str(question.id))
        if user_answer == str(question.correct_answer):
            correct_answers += 1

    total_questions = len(questions)
    score = round((correct_answers / total_questions) * 100, 2) if total_questions else 0

    if lang == "ru":
        result_text = "Ваш результат"
        correct_text = "Правильные ответы"
        wrong_text = "Неправильные ответы"
    else:
        result_text = "Sizning natijangiz"
        correct_text = "To'g'ri javoblar"
        wrong_text = "Noto‘g‘ri javoblar"

    if score < 75:
        messages.warning(request, _("Sizning ballingiz 75% dan past. Kursni ko'rib chiqishni tavsiya qilamiz."))

    return render(request, 'courses/test_result.html', {
        'course': course,
        'test': test,
        'questions': questions,
        'answers': user_answers,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'score': score,
        'result_text': result_text,
        'correct_text': correct_text,
        'wrong_text': wrong_text,
    })


@login_required
def switch_course(request, slug):
    current_course = get_object_or_404(Course, slug=slug)
    available_courses = Course.objects.filter(
        difficulty_level__name__in=['easy', 'medium']
    ).exclude(id=current_course.id)

    if not available_courses.exists():
        messages.error(request, _("Mavjud kurslar topilmadi."))
        return redirect('courses:course_single', course_id=current_course.id)

    return render(request, 'courses/switch_course.html', {
        'current_course': current_course,
        'available_courses': available_courses,
    })

@login_required
def mark_section_completed(request, section_id):
    section = get_object_or_404(CourseSection, id=section_id)
    progress, created = CourseProgress.objects.get_or_create(user=request.user, section=section)

    if request.method == "POST":
        progress.is_completed = True
        progress.save()
        messages.success(request, _("Section marked as completed!"))
    return redirect('courses:course_single', course_id=section.course.id)


@login_required
def quiz_view(request, slug, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)  # Quizni olish
    course = get_object_or_404(Course, slug=slug)  # Slug orqali kursni olish
    if quiz.section.course != course:
        raise Http404("Viktorina ushbu kursga tegishli emas.")  # Tekshirish: Quiz shu kursga tegishli ekanligini tasdiqlash

    questions = quiz.questions.all()[:quiz.max_questions]
    result = None  # Natija uchun bo'sh qiymat

    if request.method == 'POST':
        correct_answers = 0
        total_questions = questions.count()

        for question in questions:
            user_answer = request.POST.get(f"question_{question.id}")
            if user_answer is not None and user_answer.lower() == str(question.correct_answer).lower():
                correct_answers += 1

        # Natijani saqlash
        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=correct_answers
        )

        # Natijani ko'rsatish uchun o'zgaruvchi
        result = {
            'correct_answers': correct_answers,
            'total_questions': total_questions
        }

    return render(request, 'courses/quiz.html', {
        'quiz': quiz,
        'course': course,  # Kursni shablon uchun yuborish
        'questions': questions,
        'result': result  # Natijani render uchun yuboramiz
    })

User = get_user_model()

def dashboard_view(request):
    lang = get_language()
    total_users = User.objects.count()
    completed_students = CourseProgress.objects.filter(is_completed=True).count()
    avg_rating = QuizResult.objects.aggregate(Avg('score')).get('score__avg', 0)
    total_courses = Course.objects.count()
    total_scores = QuizResult.objects.aggregate(Sum('score')).get('score__sum', 0)

    # Diagramma ma'lumotlari
    courses = Course.objects.all()
    course_titles = [course.title_ru if lang == "ru" else course.title_uz for course in courses]
    completion_data = [
        CourseProgress.objects.filter(course=course, is_completed=True).count()
        for course in courses
    ]
    user_activity_data = [
        User.objects.filter(is_active=True).count(),
        User.objects.filter(is_active=False).count(),
        User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=30)).count()
    ]

    return render(request, 'courses/dashboard.html', {
        'total_users': total_users,
        'completed_students': completed_students,
        'avg_rating': round(avg_rating, 2) if avg_rating else 0,
        'total_courses': total_courses,
        'total_scores': total_scores,
        'course_titles': course_titles,
        'completion_data': completion_data,
        'user_activity_data': user_activity_data,
    })

