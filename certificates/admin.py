from django.contrib import admin
from .models import Certificate
from risk_lms.admin import risk_admin_site

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'user', 'overall_score', 'issue_date', 'is_valid']
    list_filter = ['is_valid', 'issue_date']
    search_fields = ['certificate_number', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['certificate_number', 'qr_code', 'verification_url']

# Register with custom admin site
risk_admin_site.register(Certificate, CertificateAdmin)
