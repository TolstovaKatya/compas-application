from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from catalog.forms import UserRegistrationForm, UserLoginForm
from catalog.models import Users, Lessons, Quizzes, QuizzQuestions, QuestionAnswers, AnswerType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication
from django.shortcuts import get_object_or_404
from .models import Lessons, Quizzes, QuizzQuestions, QuestionAnswers
from .serializaters import LessonDetailSerializer, CheckAnswerSerializer, LessonSerializer, QuizzesSerializer, \
    QuestionAnswersSerializer
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
def lessons_list(request):
    lessons = Lessons.objects.all().order_by('id') #взять все
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated]

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

    def get(self, request, lesson_id):
        question = Quizzes.objects.filter(id_lesson=lesson_id)

        for question in question:
            serializer = QuizzesSerializer(question)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, lesson_id):
        check_serializer = CheckAnswerSerializer(data=request.data)
        if not check_serializer.is_valid():
            return Response(check_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_answer = check_serializer.validated_data['answers']

        result = {}

        quiz = Quizzes.objects.filter(id_lesson=lesson_id).first()

        question = QuizzQuestions.objects.filter(id_quiz=quiz)


        for answer in user_answer:
            question_id = answer["question_id"]
            answer_id = answer["answer_id"]

            selected_answer = QuestionAnswers.objects.get(id=answer_id).is_correct

            answer_text = QuestionAnswers.objects.get(id=answer_id).answer_text

            if selected_answer.type == "correct":
                is_correct = True
            else:
                is_correct = False

            result[str(question_id)] = {
                'is_correct': is_correct,
                'selected_answer': answer_id,
                'answer_text': answer_text,
            }
            print(is_correct, answer_id, answer_text)

        return Response(result, status=status.HTTP_200_OK, content_type="application/json")

