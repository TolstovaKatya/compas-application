from email.policy import default

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from compas.lessons.forms import UserRegistrationForm, UserLoginForm
from compas.lessons.models import Users, Lessons, Quizzes, QuizzQuestions, QuestionAnswers, AnswerType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication
from django.shortcuts import get_object_or_404
from .models import Lessons, Quizzes, QuizzQuestions, QuestionAnswers, UserQuizProgress
from .serializaters import LessonDetailSerializer, CheckAnswerSerializer, LessonSerializer, QuizzesSerializer, \
    QuestionAnswersSerializer
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([AllowAny])
def lessons_list(request):
    lessons = Lessons.objects.all().order_by('id') #взять все
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lessons, id=lesson_id)
        serializer = LessonDetailSerializer(lesson)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_test(request, lesson_id):
    test = Quizzes.objects.filter(id_lesson=lesson_id).first()
    if not test:
        return Response({
            'error': 'No any tests for this lesson'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = QuizzesSerializer(test)
    return Response(serializer.data)

class CheckAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lessons, id=lesson_id)

        check_serializer = CheckAnswerSerializer(data=request.data)
        if not check_serializer.is_valid():
            return Response(check_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_answers = check_serializer.validated_data['answers']  # ответы выбранные пользователем
        results = {}

        quiz = Quizzes.objects.filter(id_lesson=lesson_id).first()

        questions = QuizzQuestions.objects.filter(id_quiz=quiz).prefetch_related("questionanswers_set")
        questions_dict = {q.id: q for q in questions}

        answer_ids = [item['answer_id'] for item in user_answers]
        selected_answers = QuestionAnswers.objects.filter(id__in=answer_ids)
        selected_answers_dict = {
            a.id: a
            for a in selected_answers
        }

        for item in user_answers:
            question_id = item["question_id"]
            answer_id = item["answer_id"]

            selected_answer = selected_answers_dict.get(answer_id)

            is_correct = False
            if selected_answer.is_correct and selected_answer.is_correct.type == 'correct':
                is_correct = True

            results[str(question_id)] = {
                'is_correct': is_correct,
                'selected_answer': selected_answer.answer_text,
            }

        # Возвращаем JSON с результатами
        return Response(results, status=status.HTTP_200_OK)


class SingleQuestion(APIView):
    permission_classes = [AllowAny]

    # authentication_classes убраны или оставлены опционально, так как permission AllowAny

    def get(self, request, lesson_id):
        quiz = Quizzes.objects.filter(id_lesson=lesson_id).first()
        if not quiz:
            return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizzesSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, lesson_id):
        check_serializer = CheckAnswerSerializer(data=request.data)
        if not check_serializer.is_valid():
            return Response(check_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_answer = check_serializer.validated_data['answers']

        # Получаем дополнительные параметры от клиента
        is_last_question = request.data.get('is_last', False)
        correct_count_from_client = int(request.data.get('correct_count', 0))
        wrong_count_from_client = int(request.data.get('wrong_count', 0))

        result = {}
        quiz = Quizzes.objects.filter(id_lesson=lesson_id).first()

        if not quiz:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        for answer in user_answer:
            question_id = answer["question_id"]
            answer_id = answer["answer_id"]

            try:
                selected_answer_obj = QuestionAnswers.objects.get(id=answer_id)

                # Безопасная проверка правильности
                # Предполагаем, что is_correct - это ForeignKey на таблицу типов ответов
                answer_type = selected_answer_obj.is_correct
                is_correct = False

                if answer_type and hasattr(answer_type, 'type'):
                    if answer_type.type == "correct":
                        is_correct = True
                elif answer_type and str(answer_type).lower() == "correct":
                    # Если вдруг там хранится строка или булево (на всякий случай)
                    is_correct = True

                # Если поле is_correct само по себе булево в модели QuestionAnswers (частый кейс)
                if hasattr(selected_answer_obj, 'is_correct') and isinstance(selected_answer_obj.is_correct, bool):
                    is_correct = selected_answer_obj.is_correct

            except QuestionAnswers.DoesNotExist:
                is_correct = False
                selected_answer_obj = None

            answer_text = selected_answer_obj.answer_text if selected_answer_obj else "Unknown"

            # Обновляем счетчики на основе текущего ответа
            current_correct_count = correct_count_from_client + (1 if is_correct else 0)
            current_wrong_count = wrong_count_from_client + (0 if is_correct else 1)

            result[str(question_id)] = {
                'is_correct': is_correct,
                'selected_answer': answer_id,
                'answer_text': answer_text,
            }

        total_questions = QuizzQuestions.objects.filter(id_quiz=quiz).count()

        # Логика завершения теста
        if is_last_question and total_questions > 0:
            # Формула: (правильные - 0.1 * ошибки) / всего * 100
            raw_score = current_correct_count - (0.1 * current_wrong_count)
            score = max(0, (raw_score / total_questions) * 100)

            user = request.user if request.user.is_authenticated else None

            UserQuizProgress.objects.create(
                id_user=user,
                id_quiz=quiz,
                score=round(score, 2),
                max_score=100,
                status='completed',
                correct_answers=current_correct_count,
                wrong_answers=current_wrong_count,
                completed_at=timezone.now()
            )

            result['quiz_completed'] = True
            result['final_score'] = round(score, 2)
            result['correct_count'] = current_correct_count
            result['wrong_count'] = current_wrong_count
        else:
            result['quiz_completed'] = False
            result['correct_count'] = current_correct_count
            result['wrong_count'] = current_wrong_count

        return Response(result, status=status.HTTP_200_OK)

class UserQuizzAttemptsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        attempts_data = []

        attempts = UserQuizProgress.objects.filter(id_user=user, status='completed').select_related(
            'id_quiz', 'id_quiz__id_lesson').order_by('-completed_at')

        for attempt in attempts:
            attempts_data.append({
                'attempt_id': attempt.id,
                'attempt_number': attempt.attempt_number,
                'quiz_id': attempt.id_quiz.id,
                'lesson_id': attempt.id_quiz.id_lesson.id,
                'score': attempt.score,
                'correct_answers': attempt.correct_answers,
                'wrong_answers': attempt.wrong_answers,
                'completed_at': attempt.completed_at.strftime("%Y-%m-%d %H:%M:%S"),
            })

        total_attempts = attempts.count()

        return Response({'attempts': attempts_data, 'total_attempts': total_attempts}, status=status.HTTP_200_OK, content_type="application/json")
