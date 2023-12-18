from django.urls import path
from . import views
from .views import QuizByUserListView,  QuizByUserUpdateView, QuizByUserDeleteView, QuizInfoView

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('quiz_list/<int:topic_id>/', views.quiz_list, name='quiz_list'),
    path('quiz_info/<int:quiz_id>/', QuizInfoView.as_view(), name='quiz_info'),
    path('quiz_detail/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz_result/<int:result_id>/', views.quiz_result, name='quiz_result'),
    path('quiz_history/', views.quiz_history, name='quiz_history'),
    path('my_quizzes/', QuizByUserListView.as_view(), name='quiz_by_user_list'),
    path('quizzes/', views.QuizListView.as_view(), name='quizzes'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/create_question/', views.create_question, name='create_question'),
    path('<int:quiz_id>/question/<int:question_id>/create_choice/', views.create_choice, name='create_choice'),
    path('my_quizzes/<int:pk>/', QuizByUserUpdateView.as_view(), name='update_quiz'),
    path('my_quizzes/delete/<int:pk>/', QuizByUserDeleteView.as_view(), name='quiz_by_user_delete'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
