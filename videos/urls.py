from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('<int:video_id>/', views.video_player_view, name='player'),
    path('<int:video_id>/update-progress/', views.update_progress_view, name='update_progress'),
    path('<int:video_id>/progress/', views.get_progress_view, name='get_progress'),
    path('<int:video_id>/subtitles/', views.get_subtitles_view, name='get_subtitles'),
]
