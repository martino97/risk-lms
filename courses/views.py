from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Course, Enrollment
from videos.models import Video, VideoProgress, InteractiveCourse, InteractiveCourseProgress
from quizzes.models import Question, QuizAttempt
from certificates.models import Certificate
from accounts.models import User
import re

@login_required
def dashboard_view(request):
    """Main dashboard view"""
    if request.user.is_risk_admin():
        # Risk Admin dashboard
        from accounts.models import User
        
        # Basic counts
        total_bankers = User.objects.filter(role='banker').count()
        total_courses = Course.objects.count()
        total_videos = Video.objects.count()
        total_questions = Question.objects.count()
        courses = Course.objects.all()
        
        # Real enrollment and completion statistics
        interactive_courses = InteractiveCourse.objects.filter(is_active=True)
        
        # Total enrollments (users who started any course)
        total_enrollments = InteractiveCourseProgress.objects.values('user').distinct().count()
        
        # Total completed (passed quiz and got certificate)
        total_certificates = Certificate.objects.filter(is_valid=True).count()
        
        # Users in progress (started but not completed)
        users_with_certificates = Certificate.objects.filter(is_valid=True).values_list('user_id', flat=True)
        users_in_progress = InteractiveCourseProgress.objects.exclude(
            user_id__in=users_with_certificates
        ).values('user').distinct().count()
        
        # Not enrolled (haven't started any course)
        enrolled_user_ids = InteractiveCourseProgress.objects.values_list('user_id', flat=True).distinct()
        not_enrolled = total_bankers - len(set(enrolled_user_ids))
        
        # Compliance rate (certified / total bankers)
        compliance_rate = round((total_certificates / total_bankers * 100) if total_bankers > 0 else 0, 1)
        
        # Pending certifications (completed content but no certificate)
        pending_certifications = InteractiveCourseProgress.objects.filter(
            content_completed=True
        ).exclude(
            user_id__in=users_with_certificates
        ).count()
        
        context = {
            'total_bankers': total_bankers,
            'total_courses': total_courses,
            'total_videos': total_videos,
            'total_questions': total_questions,
            'courses': courses,
            # New analytics data
            'total_enrollments': total_enrollments,
            'total_certificates': total_certificates,
            'users_in_progress': users_in_progress,
            'not_enrolled': not_enrolled,
            'compliance_rate': compliance_rate,
            'pending_certifications': pending_certifications,
            'total_users': total_bankers,  # For template compatibility
        }
    else:
        # Banker dashboard
        enrolled_courses = Enrollment.objects.filter(user=request.user).select_related('course')
        videos_completed = VideoProgress.objects.filter(user=request.user, is_completed=True).count()
        quizzes_passed = QuizAttempt.objects.filter(user=request.user, passed=True).count()
        certificates_earned = Certificate.objects.filter(user=request.user, is_valid=True).count()
        
        # Get total videos across all enrolled courses for progress calculation
        total_videos_enrolled = 0
        course_progress_data = []
        
        for enrollment in enrolled_courses:
            course = enrollment.course
            course_videos = course.videos.count()
            course_completed_videos = VideoProgress.objects.filter(
                user=request.user,
                video__course=course,
                is_completed=True
            ).count()
            
            total_videos_enrolled += course_videos
            
            course_progress = (course_completed_videos / course_videos * 100) if course_videos > 0 else 0
            course_progress_data.append({
                'course': course,
                'total_videos': course_videos,
                'completed_videos': course_completed_videos,
                'progress_percentage': course_progress
            })
        
        overall_progress = (videos_completed / total_videos_enrolled * 100) if total_videos_enrolled > 0 else 0
        
        context = {
            'enrolled_courses': enrolled_courses,
            'videos_completed': videos_completed,
            'quizzes_passed': quizzes_passed,
            'certificates_earned': certificates_earned,
            'total_videos_enrolled': total_videos_enrolled,
            'overall_progress': overall_progress,
            'course_progress_data': course_progress_data,
        }
    
    return render(request, 'courses/dashboard.html', context)

@login_required
def course_list_view(request):
    """List all published courses"""
    courses = Course.objects.all()
    user_enrolled_courses = []
    
    if not request.user.is_risk_admin():
        # For bankers, get their enrolled courses
        enrolled_course_ids = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
        user_enrolled_courses = Course.objects.filter(id__in=enrolled_course_ids)
    
    context = {
        'courses': courses,
        'user_enrolled_courses': user_enrolled_courses,
    }
    return render(request, 'courses/course_list.html', context)

@login_required
def course_detail_view(request, course_id):
    """Course detail view"""
    course = get_object_or_404(Course, id=course_id, is_published=True)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    videos = course.videos.all().order_by('order_index')
    
    # Get video progress for enrolled users and attach to video objects
    videos_with_progress = []
    total_videos = videos.count()
    completed_videos = 0
    
    for video in videos:
        video_data = {
            'video': video,
            'progress': {
                'is_completed': False,
                'completion_percentage': 0,
                'watched_duration': 0,
                'last_position': 0
            }
        }
        
        if is_enrolled:
            try:
                progress = VideoProgress.objects.get(user=request.user, video=video)
                video_data['progress'] = {
                    'is_completed': progress.is_completed,
                    'completion_percentage': progress.completion_percentage(),
                    'watched_duration': progress.watched_duration,
                    'last_position': progress.last_position
                }
                if progress.is_completed:
                    completed_videos += 1
            except VideoProgress.DoesNotExist:
                pass
        
        videos_with_progress.append(video_data)
    
    # Get interactive courses for this course
    interactive_courses = InteractiveCourse.objects.filter(course=course).order_by('order_index')
    total_interactive = interactive_courses.count()
    completed_interactive = 0
    
    # Get interactive course progress for enrolled users
    interactive_courses_with_progress = []
    for ic in interactive_courses:
        ic_data = {
            'course': ic,
            'progress': None,
            'is_completed': False
        }
        if is_enrolled:
            try:
                progress = InteractiveCourseProgress.objects.get(user=request.user, interactive_course=ic)
                ic_data['progress'] = progress
                ic_data['is_completed'] = progress.is_completed
                if progress.is_completed:
                    completed_interactive += 1
            except InteractiveCourseProgress.DoesNotExist:
                pass
        interactive_courses_with_progress.append(ic_data)
    
    # Calculate overall course progress (videos + interactive courses combined)
    total_content = total_videos + total_interactive
    completed_content = completed_videos + completed_interactive
    course_progress_percentage = (completed_content / total_content * 100) if total_content > 0 else 0
    
    # Check if all content is completed (for quiz access)
    all_videos_completed = completed_videos >= total_videos if total_videos > 0 else True
    all_interactive_completed = completed_interactive >= total_interactive if total_interactive > 0 else True
    all_content_completed = all_videos_completed and all_interactive_completed
    
    # Get quiz data for enrolled users
    user_quiz_attempts = None
    best_quiz_score = None
    if is_enrolled:
        from quizzes.models import QuizAttempt
        user_quiz_attempts = QuizAttempt.objects.filter(
            user=request.user, 
            course=course,
            completed_at__isnull=False
        ).order_by('-score')
        
        if user_quiz_attempts.exists():
            best_quiz_score = user_quiz_attempts.first().score
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'videos': videos,
        'videos_with_progress': videos_with_progress,
        'total_videos': total_videos,
        'completed_videos': completed_videos,
        'total_interactive': total_interactive,
        'completed_interactive': completed_interactive,
        'total_content': total_content,
        'completed_content': completed_content,
        'course_progress_percentage': course_progress_percentage,
        'all_content_completed': all_content_completed,
        'all_videos_completed': all_videos_completed,
        'all_interactive_completed': all_interactive_completed,
        'user_quiz_attempts': user_quiz_attempts,
        'best_quiz_score': best_quiz_score,
        'interactive_courses': interactive_courses,
        'interactive_courses_with_progress': interactive_courses_with_progress,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def enroll_course_view(request, course_id):
    """Enroll in a course"""
    course = get_object_or_404(Course, id=course_id, is_published=True)
    
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    if created:
        messages.success(request, f'Successfully enrolled in {course.title}!')
    else:
        messages.info(request, f'You are already enrolled in {course.title}.')
    
    return redirect('courses:course_detail', course_id=course.id)


def _normalize_department_key(raw_value):
    if not raw_value:
        return ''
    value = str(raw_value).strip().lower()

    # Map known labels -> keys
    label_to_key = {label.lower(): key for key, label in Course.DEPARTMENT_CHOICES}
    if value in label_to_key:
        return label_to_key[value]

    # Common variants / free-text normalization
    value = value.replace('&', 'and')
    value = re.sub(r'[^a-z0-9]+', '_', value).strip('_')
    if value in label_to_key:
        return label_to_key[value]
    if value in {k for k, _ in Course.DEPARTMENT_CHOICES}:
        return value
    if value in {'information_technology', 'informationtechnology'}:
        return 'it'
    if value in {'human_resources', 'humanresource'}:
        return 'hr'

    return value


@login_required
def bulk_enroll_department_view(request, course_id):
    """Risk admin tool to bulk-enroll bankers by department."""
    if not request.user.is_risk_admin():
        messages.error(request, 'Unauthorized access.')
        return redirect('courses:dashboard')

    course = get_object_or_404(Course, id=course_id)

    bankers = User.objects.filter(role='banker', is_active=True)

    def matching_users(department_key):
        if department_key == 'all':
            return list(bankers)
        matched = []
        for user in bankers:
            if _normalize_department_key(user.department) == department_key:
                matched.append(user)
        return matched

    selected_department = request.POST.get('department') if request.method == 'POST' else ''
    preview_department = selected_department or (course.target_departments[0] if course.target_departments else '')
    preview_department = preview_department if preview_department in {k for k, _ in Course.DEPARTMENT_CHOICES} else ''
    eligible_preview = matching_users(preview_department) if preview_department else []

    if request.method == 'POST':
        department_key = request.POST.get('department') or ''
        valid_keys = {k for k, _ in Course.DEPARTMENT_CHOICES}
        if department_key not in valid_keys:
            messages.error(request, 'Please select a valid department.')
            return redirect('courses:bulk_enroll', course_id=course.id)

        eligible = matching_users(department_key)
        created_count = 0
        for user in eligible:
            _, created = Enrollment.objects.get_or_create(user=user, course=course)
            if created:
                created_count += 1

        messages.success(
            request,
            f'Bulk enrollment complete: {created_count} new enrollments created for "{course.title}".',
        )
        return redirect('courses:course_detail', course_id=course.id)

    context = {
        'course': course,
        'department_choices': Course.DEPARTMENT_CHOICES,
        'eligible_preview_count': len(eligible_preview),
        'preview_department': preview_department,
        'bankers_count': bankers.count(),
    }
    return render(request, 'courses/bulk_enroll.html', context)

@login_required
def my_courses_view(request):
    """View user's enrolled courses"""
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'courses/my_courses.html', context)
