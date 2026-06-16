from django.test import TestCase

# Create your tests here.

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from lessons.models import Users, Lessons, Quizzes, QuizzQuestions, QuestionAnswers, AnswerType

# фикстуры
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return Users.objects.create_user(username='test_user', password='test123', email='test@chelgu.ru')

@pytest.fixture
def lesson(db):
    return Lessons.objects.create(title='Урок 1: Введение', task_indexs=1)

@pytest.fixture
def quiz(db, lesson):
    return Quizzes.objects.create(id_lesson=lesson, title='Тест к уроку 1', max_score=100)

@pytest.fixture
def question(db, quiz):
    return QuizzQuestions.objects.create(id_quiz=quiz, question_text='...?')

@pytest.fixture
def correct_answer(db, question):
    at = AnswerType.objects.create(type='correct')
    return QuestionAnswers.objects.create(id_quiz_questions=question, answer_text='Эскиз', is_correct=at)

@pytest.fixture
def wrong_answer(db, question):
    at = AnswerType.objects.create(type='wrong')
    return QuestionAnswers.objects.create(id_quiz_questions=question, answer_text='3D-модель', is_correct=at)


# тест-кейсы
@pytest.mark.django_db
def test_registration_and_token(api_client):
    """регистрация возвращает токен и данные пользователя"""
    url = reverse('RegistrationView')
    payload = {
        'username': 'new_user', 'email': 'new@chelgu.ru',
        'first_name': 'Иван', 'last_name': 'Петров',
        'password': 'securePass123', 'password2': 'securePass123'
    }
    response = api_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'token' in response.data
    assert response.data['user']['username'] == 'new_user'


@pytest.mark.django_db
def test_login_and_protected_route(api_client, user):
    """авторизация и доступ к защищённому эндпоинту"""
    login_url = reverse('LoginView')
    resp = api_client.post(login_url, {'username': 'test_user', 'password': 'test123'})
    assert resp.status_code == status.HTTP_200_OK
    token = resp.data['token']

    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    profile_url = reverse('SignupView')
    resp = api_client.get(profile_url)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['user']['email'] == 'test@chelgu.ru'


@pytest.mark.django_db
def test_get_test_structure(api_client, quiz, question, correct_answer, wrong_answer):
    """загрузка теста с вопросами и ответами"""
    url = reverse('get_test', kwargs={'lesson_id': quiz.id_lesson.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'questions' in response.data
    assert len(response.data['questions']) == 1
    assert len(response.data['questions'][0]['answers']) == 2


@pytest.mark.django_db
def test_check_correct_answer(api_client, user, lesson, question, correct_answer):
    """отправка правильного ответа (последний вопрос)"""
    api_client.force_authenticate(user=user)
    url = reverse('single', kwargs={'lesson_id': lesson.id})
    payload = {
        'answers': [{'question_id': question.id, 'answer_id': correct_answer.id}],
        'is_last': True
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data[str(question.id)]['is_correct'] is True
    assert response.data['quiz_completed'] is True


@pytest.mark.django_db
def test_check_wrong_answer(api_client, user, lesson, question, wrong_answer):
    """отправка неправильного ответа"""
    api_client.force_authenticate(user=user)
    url = reverse('single', kwargs={'lesson_id': lesson.id})

    payload = {
        'answers': [{'question_id': question.id, 'answer_id': wrong_answer.id}],
        'is_last': False
    }

    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data[str(question.id)]['is_correct'] is False