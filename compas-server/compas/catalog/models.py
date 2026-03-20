# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BigAutoField
from psycopg2.errorcodes import UNIQUE_VIOLATION


#all autoincrement id meens as default
#
# class User(AbstractUser):
#     role = models.ForeignKey('Roles', models.SET_NULL, db_column='id', blank=True, null=False)
#
#     class Meta:
#         managed = True
#         db_table = 'users'



class AnswerType(models.Model):
    type = models.CharField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'answer_type'

#groups of users like
#will be 'teachers', 'students'
# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = True
#         db_table = 'auth_group'

#user group rights
# class AuthGroupPermission(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey('AuthGroup', models.SET_NULL)
#     permission = models.ForeignKey('AuthPermission', models.SET_NULL)
#
#     class Meta:
#         managed = True
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),) #unique pair of group and permission

#list of rights
# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.SET_NULL)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = True
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)

#description of user
# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.EmailField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = True
#         db_table = 'auth_user'


# class AuthUserGroup(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey('AuthUser', models.SET_NULL)
#     group = models.ForeignKey('AuthGroup', models.SET_NULL)
#
#     class Meta:
#         managed = True
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermission(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey('AuthUser', models.SET_NULL)
#     permission = models.ForeignKey('AuthPermission', models.SET_NULL)
#
#     class Meta:
#         managed = True
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class CatalogMymodel(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     my_field_name = models.CharField(max_length=100)
#
#     class Meta:
#         managed = True
#         db_table = 'catalog_mymodel'


class Complexity(models.Model):
    complexity = models.CharField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'complexity'


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.SET_NULL, blank=True, null=True)
#     user = models.ForeignKey('AuthUser', models.SET_NULL)
#
#     class Meta:
#         managed = True
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = True
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigration(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = True
#         db_table = 'django_migrations'
#
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = True
#         db_table = 'django_session'


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

    class Meta:
        managed = True
        db_table = 'quizzes'


class Roles(models.Model):
    role_name = models.CharField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'roles'


class Status(models.Model):
    status = models.CharField(blank=True, null=True)

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
    max_score = models.IntegerField()
    score = models.IntegerField()
    id_user = models.ForeignKey( settings.AUTH_USER_MODEL, models.SET_NULL, db_column='id_user', blank=True, null=True)
    id_quiz = models.ForeignKey('Quizzes', models.SET_NULL, db_column='id_quiz', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_quiz_progress'


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
