from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('courses/', views.course_list_view, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course_view, name='enroll_course'),
    path('courses/<int:course_id>/bulk-enroll/', views.bulk_enroll_department_view, name='bulk_enroll'),
    path('my-courses/', views.my_courses_view, name='my_courses'),
]
