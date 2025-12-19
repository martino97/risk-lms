from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.my_certificates_view, name='my_certificates'),
    path('<int:certificate_id>/', views.certificate_detail_view, name='detail'),
    path('<int:certificate_id>/download/', views.download_certificate_view, name='download'),
    path('verify/<str:certificate_number>/', views.verify_certificate_view, name='verify'),
    path('generate/', views.generate_certificate_view, name='generate'),
]
