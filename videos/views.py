from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Video, VideoProgress

@login_required
def video_player_view(request, video_id):
    """Video player with progress tracking"""
    video = get_object_or_404(Video, id=video_id)
    progress, _ = VideoProgress.objects.get_or_create(
        user=request.user,
        video=video
    )
    
    context = {
        'video': video,
        'progress': progress,
        'subtitles': video.subtitles.all(),
    }
    return render(request, 'videos/player.html', context)

@login_required
@require_POST
def update_progress_view(request, video_id):
    """AJAX endpoint to update video progress (prevent skipping)"""
    video = get_object_or_404(Video, id=video_id)
    progress, _ = VideoProgress.objects.get_or_create(
        user=request.user,
        video=video
    )
    
    # Handle manual completion request
    if request.POST.get('action') == 'complete':
        completion_ok = False
        
        if video.duration > 0:
            # For videos with known duration, check 95% rule
            completion_ok = progress.completion_percentage() >= 95
        else:
            # For videos with unknown duration, check if watched at least 30 seconds
            completion_ok = progress.watched_duration >= 30
        
        if completion_ok:
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()
            
            return JsonResponse({
                'success': True,
                'is_completed': True,
                'completion_percentage': progress.completion_percentage(),
                'message': 'Video marked as complete!'
            })
        else:
            min_requirement = "95% of video" if video.duration > 0 else "30 seconds"
            return JsonResponse({
                'success': False,
                'error': f'Must watch {min_requirement} to mark complete'
            })
    
    # Regular progress update
    watched_duration = int(request.POST.get('watched_duration', 0))
    last_position = int(request.POST.get('last_position', 0))
    
    # Update progress
    progress.watched_duration = max(progress.watched_duration, watched_duration)
    progress.last_position = last_position
    
    # Auto-complete at 95% watched OR 60+ seconds for unknown duration
    if video.duration > 0:
        # For videos with known duration, use 95% rule
        if progress.watched_duration >= video.duration * 0.95:
            progress.is_completed = True
            if not progress.completed_at:
                progress.completed_at = timezone.now()
    else:
        # For videos with unknown duration, use time-based completion (60 seconds)
        if progress.watched_duration >= 60:
            progress.is_completed = True
            if not progress.completed_at:
                progress.completed_at = timezone.now()
    
    progress.save()
    
    return JsonResponse({
        'success': True,
        'is_completed': progress.is_completed,
        'completion_percentage': progress.completion_percentage(),
        'watched_duration': progress.watched_duration,
        'last_position': progress.last_position
    })

@login_required
def get_progress_view(request, video_id):
    """Get current video progress for user"""
    video = get_object_or_404(Video, id=video_id)
    try:
        progress = VideoProgress.objects.get(user=request.user, video=video)
        return JsonResponse({
            'success': True,
            'is_completed': progress.is_completed,
            'completion_percentage': progress.completion_percentage(),
            'watched_duration': progress.watched_duration,
            'last_position': progress.last_position,
            'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
        })
    except VideoProgress.DoesNotExist:
        return JsonResponse({
            'success': True,
            'is_completed': False,
            'completion_percentage': 0,
            'watched_duration': 0,
            'last_position': 0,
            'completed_at': None
        })

@login_required
def get_subtitles_view(request, video_id):
    """Get available subtitles for video"""
    video = get_object_or_404(Video, id=video_id)
    subtitles = video.subtitles.all()
    
    subtitle_data = []
    for subtitle in subtitles:
        subtitle_data.append({
            'language_code': subtitle.language_code,
            'language_name': subtitle.language_name,
            'file_url': subtitle.subtitle_file.url if subtitle.subtitle_file else None
        })
    
    return JsonResponse({
        'success': True,
        'subtitles': subtitle_data
    })
