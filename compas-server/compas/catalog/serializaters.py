from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Users, Lessons, Quizzes, QuizzQuestions, QuestionAnswers, AnswerType

User = get_user_model()

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8, max_length=64)
#     password2 = serializers.CharField(write_only=True, min_length=8, max_length=64)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'name', 'lastname', 'password', 'password2']
#
#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError('Passwords must match.')
#
#         return data
#
#     def create(self, validated_data):
#         validated_data.pop('password2')
#         user = User.objects.create(**validated_data)
#         return user
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['username', 'email', 'name', 'lastname']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = [ 'id', 'title', 'description']


class QuestionAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswers
        fields = [ 'id', 'answer_text']

class QuestionSerializer(serializers.ModelSerializer):
    answers = QuestionAnswersSerializer(many=True, read_only=True)

    class Meta:
        model = QuizzQuestions
        fields = [ 'id', 'question_text', 'answers']

class LessonDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Lessons
        fields = [ 'id', 'title', 'description', 'video_url', 'questions']


class CheckAnswerSerializer(serializers.ModelSerializer):
    answers = serializers.DictField(read_only=True)

    def validate_answers(self, data):
        if not data:
            raise serializers.ValidationError("Список ответов не может быть пустым")
        return data

