from django.contrib import admin
from .models import Video, VideoSubtitle, VideoProgress
from risk_lms.admin import risk_admin_site

class VideoSubtitleInline(admin.TabularInline):
    model = VideoSubtitle
    extra = 1
    fields = ['language_code', 'language_name', 'subtitle_file']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'duration_display', 'order_index', 'subtitle_count', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    list_editable = ['order_index']
    readonly_fields = ['created_at', 'thumbnail_preview']
    inlines = [VideoSubtitleInline]
    
    fieldsets = (
        ('Video Information', {
            'fields': ('course', 'title', 'description')
        }),
        ('Video File', {
            'fields': ('video_file', 'thumbnail', 'thumbnail_preview', 'duration')
        }),
        ('Display Settings', {
            'fields': ('order_index',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def duration_display(self, obj):
        minutes = obj.duration // 60
        seconds = obj.duration % 60
        return f"{minutes}m {seconds}s"
    duration_display.short_description = 'Duration'
    
    def subtitle_count(self, obj):
        return obj.subtitles.count()
    subtitle_count.short_description = 'Subtitles'
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return f'<img src="{obj.thumbnail.url}" width="200" />'
        return "No thumbnail"
    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

@admin.register(VideoSubtitle)
class VideoSubtitleAdmin(admin.ModelAdmin):
    list_display = ['video', 'language_name', 'language_code', 'video_course']
    list_filter = ['language_code', 'video__course']
    search_fields = ['video__title', 'language_name']
    
    def video_course(self, obj):
        return obj.video.course.title
    video_course.short_description = 'Course'

@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'watched_duration', 'is_completed', 'updated_at']
    list_filter = ['is_completed', 'updated_at']
    search_fields = ['user__email', 'video__title']

# Register with custom admin site
risk_admin_site.register(Video, VideoAdmin)
risk_admin_site.register(VideoSubtitle, VideoSubtitleAdmin)
risk_admin_site.register(VideoProgress, VideoProgressAdmin)
