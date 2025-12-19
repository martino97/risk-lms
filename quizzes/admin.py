from django.contrib import admin
from .models import Question, QuestionOption, QuizAttempt, QuizAnswer
from risk_lms.admin import risk_admin_site

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4
    fields = ['option_text', 'is_correct', 'order_index']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'get_course_or_interactive', 'topic', 'difficulty', 'question_type', 'points', 'options_count']
    list_filter = ['course', 'interactive_course', 'topic', 'difficulty', 'question_type']
    search_fields = ['question_text', 'course__title', 'interactive_course__title']
    inlines = [QuestionOptionInline]
    
    fieldsets = (
        ('Question Details', {
            'fields': ('course', 'interactive_course', 'question_text', 'question_type')
        }),
        ('Organization', {
            'fields': ('topic', 'difficulty', 'points')
        }),
        ('Additional Info', {
            'fields': ('explanation',),
            'classes': ('collapse',)
        }),
    )
    
    def question_text_short(self, obj):
        return obj.question_text[:75] + '...' if len(obj.question_text) > 75 else obj.question_text
    question_text_short.short_description = 'Question'
    
    def get_course_or_interactive(self, obj):
        if obj.interactive_course:
            return f"📱 {obj.interactive_course.title}"
        elif obj.course:
            return f"📚 {obj.course.title}"
        return "-"
    get_course_or_interactive.short_description = 'Course/Module'
    
    def options_count(self, obj):
        return obj.options.count()
    options_count.short_description = 'Options'

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_course_or_interactive', 'score', 'passed', 'started_at', 'completed_at']
    list_filter = ['passed', 'course', 'interactive_course', 'started_at']
    search_fields = ['user__email', 'course__title', 'interactive_course__title']
    
    def get_course_or_interactive(self, obj):
        if obj.interactive_course:
            return f"📱 {obj.interactive_course.title}"
        elif obj.course:
            return f"📚 {obj.course.title}"
        return "-"
    get_course_or_interactive.short_description = 'Course/Module'

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']

# Register with custom admin site
risk_admin_site.register(Question, QuestionAdmin)
risk_admin_site.register(QuizAttempt, QuizAttemptAdmin)
risk_admin_site.register(QuizAnswer, QuizAnswerAdmin)
