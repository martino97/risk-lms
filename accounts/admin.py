from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from risk_lms.admin import risk_admin_site

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_active', 'can_access_admin']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'department')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email', 'role', 'phone', 'department')}),
    )
    
    def can_access_admin(self, obj):
        """Show if user can access admin panel"""
        return obj.role in ['head_of_risk', 'risk_compliance_specialist'] or obj.is_superuser
    can_access_admin.boolean = True
    can_access_admin.short_description = 'Admin Access'
    
    def has_change_permission(self, request, obj=None):
        """Only superusers can modify user roles"""
        if request.user.is_superuser:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete users"""
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        """Only superusers can add users"""
        return request.user.is_superuser

# Register with custom admin site
risk_admin_site.register(User, UserAdmin)
