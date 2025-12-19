from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

class RiskLMSAdminSite(admin.AdminSite):
    """
    Custom Admin Site that only allows:
    - Head of Risk
    - Risk & Compliance Specialist
    - Superusers (for system management)
    
    Regular 'admin' role users CANNOT access.
    """
    site_header = "Risk LMS - Content Management"
    site_title = "Risk LMS Admin"
    index_title = "Upload Training Content"
    
    def has_permission(self, request):
        """
        Check if user can access admin panel.
        Only Head of Risk, Risk & Compliance Specialist, and Superusers allowed.
        """
        if not request.user.is_authenticated:
            return False
        
        # Superusers always have access
        if request.user.is_superuser:
            return True
        
        # Check if user has the correct role AND is_staff
        return (request.user.is_staff and 
                request.user.role in ['head_of_risk', 'risk_compliance_specialist'])

# Create instance of custom admin site
risk_admin_site = RiskLMSAdminSite(name='risk_admin')
