from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('user/<int:user_id>/', views.user_progress_view, name='user_progress'),
    path('course/<int:course_id>/', views.course_progress_view, name='course_progress'),
    path('analytics/', views.course_analytics_view, name='course_analytics'),
]
