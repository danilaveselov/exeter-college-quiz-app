from django.apps import apps
from django.urls import path

from .views import (
    QuizListView,
    QuizDetailView,
    QuizCreateView,
    QuizUpdateView,
    QuizDeleteView,
    QuizStartView,
    QuestionCreateView,
    QuestionDeleteView,
    QuestionUpdateView
)

app_name = apps.get_app_config('quiz').name

urlpatterns = [
    path('', QuizListView.as_view(), name='list'),
    path('quiz/<slug:slug>/detail/', QuizDetailView.as_view(), name='detail'),
    path('quiz/create/new/', QuizCreateView.as_view(), name='create'),
    path('quiz/<slug:slug>/update/', QuizUpdateView.as_view(), name='update'),
    path('quiz/<slug:slug>/delete/', QuizDeleteView.as_view(), name='delete'),
    path('quiz/<slug:slug>/start/', QuizStartView.as_view(), name='start'),
    path(
        'quiz/<slug:slug>/question/create/',
        QuestionCreateView.as_view(),
        name='question_create'
    ),
    path(
        'quiz/question/<int:pk>/update/',
        QuestionUpdateView.as_view(),
        name='question_update'
    ),
    path(
        'quiz/question/<int:pk>/delete/',
        QuestionDeleteView.as_view(),
        name='question_delete'
    )
]
