# catalog/admin.py
from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget  # виджет rich-text редактора
from .models import Lessons, Quizzes, QuizzQuestions, QuestionAnswers
import nested_admin

class LessonForm(forms.ModelForm):

    """
    Форма для модели Lessons с полями описания,
    использующими визуальный редактор CKEditor.
    """

    description = forms.CharField(
        widget=CKEditorWidget(config_name='default'),
        required=False,
        label='Описание урока'
    )

    class Meta:
        model = Lessons
        fields = '__all__'


class QuestionAnswersInline(nested_admin.NestedTabularInline):
    model = QuestionAnswers
    extra = 1
    fields = ['answer_text', 'is_correct']
    min_num = 1
    can_delete = True

    labels = {
        'answer_text': 'Текст ответа',
        'is_correct': 'Правильный ответ',
    }
    help_texts = {
        'answer_text': 'Введите вариант ответа',
        'is_correct': 'Отметьте галочкой правильный ответ',
    }


class QuizzQuestionsInline(nested_admin.NestedStackedInline):
    model = QuizzQuestions
    extra = 1
    fields = ['question_text']
    min_num = 1
    can_delete = True
    inlines = [QuestionAnswersInline]

    verbose_name = 'Вопрос'
    verbose_name_plural = 'Вопросы теста'


class QuizzesInline(nested_admin.NestedStackedInline):
    model = Quizzes
    extra = 1
    inlines = [QuizzQuestionsInline] # вопросы внутри теста
    fields = ['title']
    show_change_link = True
    can_delete = True

    verbose_name = 'Тест'
    verbose_name_plural = 'Тесты к уроку'


@admin.register(Lessons)
class LessonsAdmin(nested_admin.NestedModelAdmin):
    list_display = ['id', 'title', 'task_complexity', 'video_url']
    search_fields = ['title', 'description']
    list_filter = ['task_complexity']
    form = LessonForm
    inlines = [QuizzesInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description'),
            'description': 'Заполните название и описание урока'
        }),
        ('Мультимедиа', {
            'fields': ('video_url', 'task_complexity'),
            'description': 'URL видео и сложность урока'
        }),
    )


#@admin.register(Quizzes)
class QuizzesAdmin(nested_admin.NestedModelAdmin):
    list_display = ['id', 'title', 'id_lesson']
    inlines = [QuizzQuestionsInline] #вопросы внутри теста
    list_filter = ['id_lesson']
    search_fields = ['title']


#@admin.register(nested_admin.NestedModelAdmin)
class QuizzQuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_text', 'id_quiz']
    inlines = [QuestionAnswersInline] # ответы внутри вопроса
    list_filter = ['id_quiz']
    search_fields = ['question_text']


#@admin.register(nested_admin.NestedModelAdmin)
class QuestionAnswersAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer_text', 'is_correct', 'id_quiz_questions']
    list_filter = ['is_correct', 'id_quiz_questions']
    search_fields = ['answer_text']