from django.db import models
from django.conf import settings
from courses.models import Course
from videos.models import InteractiveCourse
import random

class Question(models.Model):
    """Question bank for quizzes - can belong to Course or InteractiveCourse"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('multiple_answer', 'Multiple Answer'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    # Can belong to either a Course or an InteractiveCourse
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    interactive_course = models.ForeignKey(InteractiveCourse, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    topic = models.CharField(max_length=255, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='medium')
    points = models.IntegerField(default=1)
    explanation = models.TextField(blank=True, help_text="Explanation shown after answering")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['topic', 'created_at']
    
    def __str__(self):
        if self.interactive_course:
            return f"{self.interactive_course.title} - {self.question_text[:50]}"
        elif self.course:
            return f"{self.course.title} - {self.question_text[:50]}"
        return f"Unlinked - {self.question_text[:50]}"

class QuestionOption(models.Model):
    """Options for multiple choice questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order_index = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'question_options'
        ordering = ['order_index']
    
    def __str__(self):
        return f"{self.question.question_text[:30]} - {self.option_text[:30]}"

class QuizAttempt(models.Model):
    """Quiz attempt tracking - for both Course and InteractiveCourse"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_attempts', null=True, blank=True)
    interactive_course = models.ForeignKey(InteractiveCourse, on_delete=models.CASCADE, related_name='quiz_attempts', null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Store question IDs so quiz persists across sessions
    question_ids = models.JSONField(default=list, blank=True, help_text='List of question IDs for this attempt')
    
    class Meta:
        db_table = 'quiz_attempts'
        ordering = ['-started_at']
    
    def __str__(self):
        if self.interactive_course:
            return f"{self.user.get_full_name()} - {self.interactive_course.title} - {self.score}%"
        elif self.course:
            return f"{self.user.get_full_name()} - {self.course.title} - {self.score}%"
        return f"{self.user.get_full_name()} - {self.score}%"

class QuizAnswer(models.Model):
    """User's answers to quiz questions"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    selected_options = models.ManyToManyField(QuestionOption)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'quiz_answers'
    
    def __str__(self):
        return f"{self.attempt.user.get_full_name()} - Q{self.question.id}"
