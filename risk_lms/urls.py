"""
URL configuration for Risk LMS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .admin import risk_admin_site

urlpatterns = [
    # Custom admin site - Only Head of Risk and Risk & Compliance Specialist can access
    path('admin/', risk_admin_site.urls),
    
    # Content Management Panel (for uploading content with recording and translation)
    path('content/', include('content_management.urls')),
    
    path('', RedirectView.as_view(url='/courses/', permanent=False)),
    
    # App URLs
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('videos/', include('videos.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('progress/', include('progress.urls')),
    path('certificates/', include('certificates.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
