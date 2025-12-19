from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model with role-based access"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('head_of_risk', 'Head of Risk'),
        ('risk_compliance_specialist', 'Risk & Compliance Specialist'),
        ('banker', 'Banker'),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='banker')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def is_risk_admin(self):
        """Check if user can manage courses (Admin, Head of Risk and Risk & Compliance Specialist)"""
        return self.role in ['admin', 'head_of_risk', 'risk_compliance_specialist'] or self.is_superuser
    
    def is_banker(self):
        """Check if user is a regular banker"""
        return self.role == 'banker'
    
    def can_upload_content(self):
        """Check if user can upload courses and videos (Admin, Head of Risk and Risk & Compliance Specialist)"""
        return self.role in ['admin', 'head_of_risk', 'risk_compliance_specialist'] or self.is_superuser
    
    def save(self, *args, **kwargs):
        """Override save to set is_staff based on role"""
        # Set is_staff based on role
        if self.role in ['admin', 'head_of_risk', 'risk_compliance_specialist']:
            self.is_staff = True
        elif not self.is_superuser:
            self.is_staff = False
        super().save(*args, **kwargs)
