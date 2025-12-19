from django import template

register = template.Library()

@register.filter
def duration_format(seconds):
    """Convert seconds to MM:SS format"""
    if not seconds or seconds == 0:
        return "0:00"
    
    try:
        seconds = int(seconds)
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02d}"
    except (ValueError, TypeError):
        return "0:00"

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary using key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, {})
    return {}

@register.simple_tag
def get_video_progress(video_progress_data, video_id):
    """Get video progress data for a specific video"""
    if isinstance(video_progress_data, dict):
        return video_progress_data.get(video_id, {
            'is_completed': False,
            'completion_percentage': 0,
            'watched_duration': 0,
            'last_position': 0
        })
    return {
        'is_completed': False,
        'completion_percentage': 0,
        'watched_duration': 0,
        'last_position': 0
    }