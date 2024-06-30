from django.urls import path
from .views import (
    HomeView, VocabularyRegistView, VocabularylistView,
    VocabularyUpdateView, QuizView, problem_view,
    AnswerListView, VocabularyDeleteView, answer_view,
)



app_name = 'vocabularies'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('vocabulary_regist/', VocabularyRegistView.as_view(), name='vocabulary_regist'),
    path('vocabulary_list/', VocabularylistView.as_view(), name='vocabulary_list'),
    path('vocabulary_update/<int:pk>', VocabularyUpdateView.as_view(), name='vocabulary_update'),
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('problem_view/', problem_view, name='problem_view'),
    path('answer_view/', answer_view, name='answer_view'),
    path('answer_list/', AnswerListView.as_view(), name='answer_list'),
    path('vocabulary_delete/<int:pk>', VocabularyDeleteView.as_view(), name='vocabulary_delete'),
]
