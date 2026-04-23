from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Users, Lessons, Quizzes, QuizzQuestions, QuestionAnswers, AnswerType

User = get_user_model()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = [ 'id', 'title']

#отображение ответов
class QuestionAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswers
        fields = [ 'id', 'answer_text']

#отображение вопросов с ответами
class QuestionSerializer(serializers.ModelSerializer):
    answers = QuestionAnswersSerializer(many=True, read_only=True, source='questionanswers_set')

    class Meta:
        model = QuizzQuestions
        fields = [ 'id', 'question_text', 'answers']

#отображение теста с вопросами и ответами
class QuizzesSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='quizzquestions_set')

    class Meta:
        model = Quizzes
        fields = [ 'id', 'title', 'questions']

class LessonDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Lessons
        fields = [ 'id', 'title', 'description', 'video_url', 'questions']

    def get_questions(self, obj):
        test = Quizzes.objects.filter(id_lesson=obj.id).first()
        if test:
            return QuizzesSerializer(test).data
        else:
            return None

#ответы пользователя
class UserAnswersSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()

class CheckAnswerSerializer(serializers.Serializer):
    answers = serializers.ListField(child=UserAnswersSerializer())

    def validate_answers(self, data):
        if not data:
            raise serializers.ValidationError("Список ответов не может быть пустым")
        return data

