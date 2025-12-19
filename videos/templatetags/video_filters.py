from django import template

register = template.Library()

@register.filter
def duration_format(seconds):
    """Convert seconds to MM:SS format"""
    if not seconds:
        return "0:00"
    
    try:
        seconds = int(seconds)
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02d}"
    except (ValueError, TypeError):
        return "0:00"

@register.filter
def file_size_format(bytes):
    """Convert bytes to human readable format"""
    if not bytes:
        return "0 B"
    
    try:
        bytes = int(bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"
    except (ValueError, TypeError):
        return "0 B"