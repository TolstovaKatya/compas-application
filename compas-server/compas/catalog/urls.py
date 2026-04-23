# Используйте include() чтобы добавлять URL из каталога приложения
from django.urls import include
from django.urls import path
from . import views
from .views import LessonDetailView, lessons_list, get_test, CheckAnswerView, SingleQuestion

urlpatterns = [
    path('api/lessons/', lessons_list, name="lessons"),
    path('api/lessons/<int:lesson_id>/', LessonDetailView.as_view(), name="lesson-detail-view<int:lesson_id>"),

    path('api/lessons/<int:lesson_id>/test', get_test, name="get_test"),
    path('api/lessons/<int:lesson_id>/test/submit', CheckAnswerView.as_view(), name="check"),

    path('api/lessons/<int:lesson_id>/test/single', SingleQuestion.as_view(), name="single"),
]