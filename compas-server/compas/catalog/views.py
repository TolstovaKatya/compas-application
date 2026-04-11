from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout

from catalog.forms import UserRegistrationForm, UserLoginForm
from catalog.models import Users, Lessons, Quizzes, QuizzQuestions, QuestionAnswers, AnswerType


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Lessons, Quizzes, QuizzQuestions, QuestionAnswers
from .serializaters import LessonDetailSerializer, CheckAnswerSerializer


@login_required
def profile(request):
    return render(request,'profile.html', {
        'user':request.user,
    })

@staff_member_required
def users_list(request):
    users = Users.objects.all()
    return render(request,'users_list.html', {
        'users':users,
    })

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request,'registration/registration.html', {'form':form})


def user_login(request):

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/login')

def lessons_list(request):
    lessons = Lessons.objects.all().order_by('id') #взять все
    return render(request,'lessons_list.html', {
        'lessons':lessons,
    })

class LessonDetailView(APIView):
    # lesson = get_object_or_404(Lessons,id=lesson_id)
    # quiz = Quizzes.objects.filter(id_lesson=lesson_id).first()
    # questions = []
    # results = None
    #
    # if quiz:
    #     questions = QuizzQuestions.objects.filter(id_quiz = quiz).prefetch_related("questionanswers_set")
    #
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     results = {}
    #     for question in questions:
    #         selected_answer_id = request.POST.get(f'question_{question.id}')
    #         if selected_answer_id:
    #             selected_answer = QuestionAnswers.objects.get(id=selected_answer_id)
    #             is_correct = selected_answer.is_correct and selected_answer.is_correct.type == "correct"
    #             results[question.id] = {
    #                 'is_correct': is_correct,
    #                 'selected_answer': selected_answer.answer_text,
    #             }
    #         else:
    #             results[question.id] = {
    #                 'is_correct': False,
    #                 'selected_answer': None,
    #             }
    #     return JsonResponse(results)
    #
    # # if questions:
    # #     results = {}
    # #     for question in questions:
    # #         selected_answer_id = request.POST.get(f'question_{question.id}')
    # #
    # #         if selected_answer_id:
    # #             selected_answer = QuestionAnswers.objects.get(id = selected_answer_id)
    # #             is_correct = (selected_answer.is_correct and selected_answer.is_correct.type == 'correct')
    # #             results[question.id] = {
    # #                 'correct': is_correct,
    # #                 'selected_answer': selected_answer.answer_text
    # #             }
    #
    # return render(request,'lessons_detail.html', {
    #     'lesson' : lesson,
    #     'questions' : questions,})


# def test(request, lesson_id, ):
#     quiz = get_object_or_404(Quizzes,id_lesson=lesson_id)
#     question = get_object_or_404(QuizzQuestions, id_quiz=quiz_id)
#     return render(request,'test.html', {'quiz': quiz})
#
# def question(request, quiz_id):
#     question = get_object_or_404(QuizzQuestions,id_quiz=quiz_id)
#     ret
    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lessons, id=lesson_id)
        serializer = LessonDetailSerializer(lesson)
        return Response(serializer.data)

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lessons, id=lesson_id)

        check_serializer = CheckAnswerSerializer(data=request.data)
        if not  check_serializer.is_valid():
            return Response(check_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_answers = check_serializer.validated_data['answers'] #ответы выбранные пользователем
        results = {}

        quiz = Quizzes.objects.filter(id_lesson=lesson_id).first()

        questions = QuizzQuestions.objects.filter(id_quiz=quiz).prefetch_related("questionanswers_set")
        questions_dict = {q.id: q for q in questions}

        selected_answers = user_answers.values()
        selected_answers_dict = {
            a.id: a
            for a in QuestionAnswers.objects.filter(id__in = selected_answers)
        }

        for question_id, selected_answer_id in user_answers.items():
            question = questions_dict.get(question_id)
            selected_answer = selected_answers_dict.get(selected_answer_id)

            is_correct = False
            if selected_answer.is_correct and selected_answer.is_correct.type == 'correct':
                is_correct = True

            results[str(question_id)] = {
                   'is_correct': is_correct,
                   'selected_answer': selected_answer.answer_text,
                 }

        # Возвращаем JSON с результатами
        return Response(results, status=status.HTTP_200_OK)





