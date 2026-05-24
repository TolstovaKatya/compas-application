from django.core.serializers import serialize
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializaters import UserRegistrationSerializer, UserSerializer, UserLoginSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={
            200: {
                "type": "object"
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                    "error": {"type": "string"}
                },
                "description": "Неверные учётные данные или отсутствующие поля"
            },
            500: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                    "error": {"type": "string"}
                },
                "description": "Внутренняя ошибка сервера"
            }
        },
        operation_id="registration_user"
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'user': UserSerializer(user).data}, status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(
        request=UserLoginSerializer,
        responses={
            200: {
                "type": "object"
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                    "error": {"type": "string"}
                },
                "description": "Неверные учётные данные или отсутствующие поля"
            },
            500: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                    "error": {"type": "string"}
                },
                "description": "Внутренняя ошибка сервера"
            }
        },
        operation_id="login_user"
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data}, status.HTTP_200_OK)

        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({'user': UserSerializer(request.user).data})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "description": "Токен удалён, сессия завершена"
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                    "error": {"type": "string"}
                },
                "description": "Отсутствует или недействителен токен авторизации"
            },
            500: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                    "error": {"type": "string"}
                },
                "description": "Внутренняя ошибка сервера"
            }
        },
        description="Аннулирует токен авторизации текущего пользователя",
    )
    def post(self, request):
        logout(request)
        try:
            request.user.auth_token.delete()
        except:
            pass
        return Response({"message": "Logout successful"})


