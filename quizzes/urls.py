from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    # Course quizzes
    path('<int:course_id>/start/', views.start_quiz_view, name='start'),
    path('attempt/<int:attempt_id>/', views.take_quiz_view, name='take'),
    path('attempt/<int:attempt_id>/submit/', views.submit_quiz_view, name='submit'),
    path('attempt/<int:attempt_id>/results/', views.quiz_results_view, name='results'),
    
    # Interactive course quizzes
    path('interactive/<int:interactive_id>/start/', views.start_interactive_quiz, name='start_interactive'),
    path('interactive/<int:interactive_id>/questions/', views.manage_interactive_questions, name='manage_interactive_questions'),
    path('interactive/<int:interactive_id>/questions/add/', views.add_interactive_question, name='add_interactive_question'),
    path('interactive/question/<int:question_id>/edit/', views.edit_interactive_question, name='edit_interactive_question'),
    path('interactive/question/<int:question_id>/delete/', views.delete_interactive_question, name='delete_interactive_question'),
]
