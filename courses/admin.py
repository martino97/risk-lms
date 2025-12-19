from django.contrib import admin
from .models import Course, Enrollment
from risk_lms.admin import risk_admin_site

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_published', 'passing_score', 'created_at', 'video_count', 'question_count']
    list_filter = ['is_published', 'created_at', 'created_by']
    search_fields = ['title', 'description']
    list_editable = ['is_published']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'thumbnail')
        }),
        ('Settings', {
            'fields': ('passing_score', 'is_published')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new course
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'is_completed']
    list_filter = ['is_completed', 'enrolled_at']
    search_fields = ['user__email', 'course__title']

# Register with custom admin site
risk_admin_site.register(Course, CourseAdmin)
risk_admin_site.register(Enrollment, EnrollmentAdmin)
