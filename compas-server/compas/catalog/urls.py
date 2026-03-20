# Используйте include() чтобы добавлять URL из каталога приложения
from django.urls import include
from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name="profile"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('lessons/', views.lessons_list, name="lessons"),
    path('lessons/<int:lesson_id>/', views.lessons_detail, name="lesson_detail"),
    # path('test/<int:lesson_id>/', views.test, name="test"),
]