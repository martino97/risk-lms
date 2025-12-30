from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Course(models.Model):
    """Course model"""
    DEPARTMENT_CHOICES = [
        ('all', 'All Departments'),
        ('operations', 'Operations'),
        ('retail_banking', 'Retail Banking'),
        ('corporate_banking', 'Corporate Banking'),
        ('risk_management', 'Risk Management'),
        ('compliance', 'Compliance'),
        ('finance', 'Finance'),
        ('it', 'Information Technology'),
        ('hr', 'Human Resources'),
        ('audit', 'Internal Audit'),
        ('marketing', 'Marketing'),
        ('branch_network', 'Branch Network'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_courses')
    is_published = models.BooleanField(default=False)
    passing_score = models.IntegerField(default=80)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    target_departments = models.JSONField(default=list, blank=True, help_text='List of department keys that should be enrolled/targeted')
    
    # Course completion time limits
    completion_time_enabled = models.BooleanField(
        default=False,
        help_text='Enable time limit for course completion'
    )
    completion_time_limit = models.IntegerField(
        default=0,
        help_text='Time limit for course completion in days (0 = no limit)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

    def targets_department(self, department_key):
        targets = self.target_departments or []
        return 'all' in targets or (department_key in targets)
    
    def get_total_videos(self):
        return self.videos.count()
    
    def get_total_questions(self):
        return self.questions.count()
    
    def get_time_limit_display(self):
        """Get human readable time limit"""
        if not self.completion_time_enabled or self.completion_time_limit <= 0:
            return "No time limit"
        
        days = self.completion_time_limit
        if days == 1:
            return "1 day"
        elif days < 7:
            return f"{days} days"
        elif days == 7:
            return "1 week"
        elif days < 30:
            weeks = days // 7
            remaining_days = days % 7
            if remaining_days == 0:
                return f"{weeks} weeks"
            else:
                return f"{weeks} weeks {remaining_days} days"
        else:
            months = days // 30
            remaining_days = days % 30
            if remaining_days == 0:
                return f"{months} months"
            else:
                return f"{months} months {remaining_days} days"

class Enrollment(models.Model):
    """Course enrollment model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Deadline for course completion'
    )
    
    class Meta:
        db_table = 'enrollments'
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.title}"
    
    def save(self, *args, **kwargs):
        """Set deadline based on course completion time limit"""
        # Set deadline if conditions are met and enrolled_at will be available
        if (not self.deadline and 
            self.course.completion_time_enabled and 
            self.course.completion_time_limit > 0):
            
            # If this is a new object, enrolled_at will be set after save
            # Use current time for calculation
            if not self.enrolled_at:
                from django.utils import timezone
                base_time = timezone.now()
            else:
                base_time = self.enrolled_at
                
            self.deadline = base_time + timedelta(days=self.course.completion_time_limit)
        
        super().save(*args, **kwargs)
    
    def is_overdue(self):
        """Check if enrollment is overdue"""
        if self.deadline and not self.is_completed:
            return timezone.now() > self.deadline
        return False
    
    def days_remaining(self):
        """Get days remaining for completion"""
        if self.deadline and not self.is_completed:
            remaining = self.deadline - timezone.now()
            return max(0, remaining.days)
        return None
