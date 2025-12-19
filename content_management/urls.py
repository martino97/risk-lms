from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.content_dashboard, name='dashboard'),
    path('course/upload/', views.upload_course, name='upload_course'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/edit/', views.edit_course_settings, name='edit_course'),
    path('course/<int:course_id>/video/', views.video_upload, name='video_upload'),
    path('course/<int:course_id>/questions/', views.question_bank, name='question_bank'),
    path('video/record/save/', views.save_recorded_video, name='save_recorded_video'),
    path('video/<int:video_id>/subtitles/upload/', views.upload_subtitles_view, name='upload_subtitles'),
    path('video/<int:video_id>/delete/', views.delete_video, name='delete_video'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    
    # Interactive Course (SCORM/Captivate) Upload
    path('interactive/', views.interactive_course_list, name='interactive_list'),
    path('interactive/upload/', views.upload_interactive_course_new, name='upload_interactive_new'),
    path('interactive/<int:interactive_id>/delete/', views.delete_interactive_course, name='delete_interactive'),
    path('course/<int:course_id>/interactive/', views.upload_interactive_course, name='upload_interactive'),
    path('course/<int:course_id>/interactive/<int:interactive_id>/play/', views.play_interactive_course, name='play_interactive'),
    path('interactive/<int:interactive_id>/progress/', views.update_interactive_progress, name='update_interactive_progress'),
    
    # Interactive Course Questions
    path('interactive/<int:interactive_id>/questions/', views.interactive_question_bank, name='interactive_question_bank'),
    path('interactive/<int:interactive_id>/questions/add/', views.add_interactive_question, name='add_interactive_question'),
    path('interactive/<int:interactive_id>/questions/<int:question_id>/edit/', views.edit_interactive_question, name='edit_interactive_question'),
    path('interactive/<int:interactive_id>/questions/<int:question_id>/delete/', views.delete_interactive_question, name='delete_interactive_question'),
    
    # Excel Reports
    path('reports/enrollment/', views.download_course_enrollment_report, name='enrollment_report'),
    path('reports/performance/', views.download_user_performance_report, name='performance_report'),
]
