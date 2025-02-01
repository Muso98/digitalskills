from modeltranslation.translator import translator, TranslationOptions
from .models import Course, CourseSection, Quiz, Question

class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class CourseSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

class QuizTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class QuestionTranslationOptions(TranslationOptions):
    fields = ('text', 'correct_answer', 'option_a', 'option_b', 'option_c', 'option_d')

translator.register(Question, QuestionTranslationOptions)
translator.register(Course, CourseTranslationOptions)
translator.register(CourseSection, CourseSectionTranslationOptions)
translator.register(Quiz, QuizTranslationOptions)
