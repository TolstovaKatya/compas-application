# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BigAutoField
from psycopg2.errorcodes import UNIQUE_VIOLATION

class AnswerType(models.Model):
    type = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'answer_type'


class Complexity(models.Model):
    complexity = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'complexity'


class Lessons(models.Model):
    task_indexs = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    video_url = models.TextField(blank=True, null=True)
    task_complexity = models.ForeignKey('Complexity', models.SET_NULL, db_column='task_complexity', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lessons'


class QuestionAnswers(models.Model):
    id_quiz_questions = models.ForeignKey('QuizzQuestions', models.SET_NULL, db_column='id_quiz_questions', blank=True, null=True)
    answer_text = models.TextField(blank=True, null=True)
    is_correct = models.ForeignKey('AnswerType', models.SET_NULL, db_column='is_correct', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'question_answers'


class QuizzQuestions(models.Model):
    id_quiz = models.ForeignKey('Quizzes', models.SET_NULL, db_column='id_quiz', blank=True, null=True)
    question_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'quizz_questions'


class Quizzes(models.Model):
    id_lesson = models.ForeignKey('Lessons', models.SET_NULL, db_column='id_lesson', blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    max_score = models.IntegerField(default=100) # максимальный балл за тест

    class Meta:
        managed = True
        db_table = 'quizzes'


class Roles(models.Model):
    role_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'roles'


class Status(models.Model):
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'status'


class UserLessonProgress(models.Model):
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, db_column='id_user', blank=True, null=True)
    id_lesson = models.ForeignKey('Lessons', models.SET_NULL, db_column='id_lesson', blank=True, null=True)
    status = models.ForeignKey('Status', models.SET_NULL, db_column='status', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_lesson_progress'


class UserQuizProgress(models.Model):
    max_score = models.IntegerField(default=100)
    score = models.IntegerField(default=0) # балл пользователя за конкретный тест
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column='id_user', blank=True, null=True)
    id_quiz = models.ForeignKey('Quizzes', models.CASCADE, db_column='id_quiz', blank=True, null=True)

    status = models.CharField(max_length=20, default='in_progress', choices=[('in_progress', 'В процессе'), ('completed', 'Завершен')])

    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)

    attempt_number = models.IntegerField(default=1)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_quiz_progress'

    def save(self, *args, **kwargs): # функция для установления номера попытки
        if not self.pk and self.id_quiz and self.id_user:
            last_attempt = UserQuizProgress.objects.filter(
                id_user=self.id_user,
                id_quiz=self.id_quiz,
            ).order_by('-attempt_number').first()

            self.attempt_number = (last_attempt.attempt_number + 1) if last_attempt else 1

        if self.score and not self.completed_at:
            self.completed_at = timezone.now()

        return super().save(*args, **kwargs)


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        'Roles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'users'

