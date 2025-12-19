from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from courses.models import Enrollment
from videos.models import VideoProgress
from quizzes.models import QuizAttempt
from accounts.models import User

@login_required
def user_progress_view(request, user_id):
    """View individual user's progress across all courses"""
    user = get_object_or_404(User, id=user_id)
    
    # Get all enrollments
    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    
    progress_data = []
    for enrollment in enrollments:
        course = enrollment.course
        
        # Get video completion stats
        total_videos = course.videos.count()
        completed_videos = VideoProgress.objects.filter(
            user=user,
            video__course=course,
            is_completed=True
        ).count()
        
        # Get quiz attempts
        quiz_attempts = QuizAttempt.objects.filter(
            user=user,
            course=course,
            completed_at__isnull=False
        )
        
        best_quiz_score = quiz_attempts.aggregate(Avg('score'))['score__avg'] or 0
        
        progress_data.append({
            'course': course,
            'enrollment': enrollment,
            'total_videos': total_videos,
            'completed_videos': completed_videos,
            'video_progress': (completed_videos / total_videos * 100) if total_videos > 0 else 0,
            'quiz_attempts': quiz_attempts.count(),
            'best_quiz_score': best_quiz_score,
        })
    
    # Calculate summary statistics
    total_courses = len(progress_data)
    completed_courses = sum(1 for data in progress_data if data['video_progress'] >= 100)
    total_videos_all = sum(data['total_videos'] for data in progress_data)
    completed_videos_all = sum(data['completed_videos'] for data in progress_data)
    overall_progress = (completed_videos_all / total_videos_all * 100) if total_videos_all > 0 else 0
    
    # Get certificates count
    from certificates.models import Certificate
    certificates_count = Certificate.objects.filter(user=user, is_valid=True).count()
    
    # Get recent activity
    recent_progress = VideoProgress.objects.filter(user=user).order_by('-updated_at')[:5]
    recent_activity = []
    for progress in recent_progress:
        recent_activity.append({
            'video_title': progress.video.title,
            'course_title': progress.video.course.title,
            'is_completed': progress.is_completed,
            'completion_percentage': progress.completion_percentage(),
            'updated_at': progress.updated_at
        })
    
    context = {
        'progress_user': user,
        'progress_data': progress_data,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'total_videos': total_videos_all,
        'completed_videos': completed_videos_all,
        'overall_progress': overall_progress,
        'certificates_count': certificates_count,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'progress/user_progress.html', context)

@login_required
def course_progress_view(request, course_id):
    """View all users' progress for a specific course (Admin view)"""
    from courses.models import Course
    
    if not request.user.is_risk_admin():
        return redirect('courses:dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related('user')
    
    progress_data = []
    for enrollment in enrollments:
        user = enrollment.user
        
        # Get video completion stats
        total_videos = course.videos.count()
        completed_videos = VideoProgress.objects.filter(
            user=user,
            video__course=course,
            is_completed=True
        ).count()
        
        # Get quiz attempts
        quiz_attempts = QuizAttempt.objects.filter(
            user=user,
            course=course,
            completed_at__isnull=False
        )
        
        best_quiz_score = quiz_attempts.aggregate(Avg('score'))['score__avg'] or 0
        
        progress_data.append({
            'user': user,
            'enrollment': enrollment,
            'total_videos': total_videos,
            'completed_videos': completed_videos,
            'video_progress': (completed_videos / total_videos * 100) if total_videos > 0 else 0,
            'quiz_attempts': quiz_attempts.count(),
            'best_quiz_score': best_quiz_score,
        })
    
    # Calculate average progress
    if progress_data:
        total_progress = sum(data['video_progress'] for data in progress_data)
        average_progress = int(total_progress / len(progress_data))
    else:
        average_progress = 0
    
    context = {
        'course': course,
        'progress_data': progress_data,
        'average_progress': average_progress,
    }
    
    return render(request, 'progress/course_progress.html', context)


@login_required
def course_analytics_view(request):
    """
    Analytics dashboard for Head of Risk and Risk & Compliance Specialist.
    Shows enrollment stats, completion rates, and user progress across all courses.
    """
    from courses.models import Course
    from videos.models import InteractiveCourse, InteractiveCourseProgress
    from certificates.models import Certificate
    from django.utils import timezone
    from datetime import timedelta
    
    # Only Head of Risk and Risk & Compliance Specialist can access
    if not request.user.is_risk_admin():
        return redirect('courses:dashboard')
    
    # Get all bankers (potential learners)
    all_bankers = User.objects.filter(role='banker')
    total_bankers = all_bankers.count()
    
    # Get all courses
    courses = Course.objects.all()
    interactive_courses = InteractiveCourse.objects.filter(is_active=True)
    
    # Course-specific analytics
    course_analytics = []
    
    for course in courses:
        # Get interactive courses for this course
        ic_list = course.interactive_courses.filter(is_active=True)
        
        for ic in ic_list:
            # Users who have started (have progress record)
            enrolled_users = InteractiveCourseProgress.objects.filter(
                interactive_course=ic
            ).select_related('user')
            
            enrolled_count = enrolled_users.count()
            enrolled_user_ids = enrolled_users.values_list('user_id', flat=True)
            
            # Users who completed content (100%)
            completed_content = enrolled_users.filter(content_completed=True)
            completed_content_count = completed_content.count()
            
            # Users who passed the quiz (got certificate)
            certificates = Certificate.objects.filter(
                interactive_course=ic,
                is_valid=True
            )
            passed_quiz_count = certificates.count()
            
            # Users currently in progress (started but not completed)
            in_progress_count = enrolled_count - completed_content_count
            
            # Users who haven't enrolled at all
            not_enrolled_count = total_bankers - enrolled_count
            
            # Calculate average completion percentage
            avg_completion = enrolled_users.aggregate(
                avg=Avg('completion_percentage')
            )['avg'] or 0
            
            # Get recent activity (last 7 days)
            seven_days_ago = timezone.now() - timedelta(days=7)
            recent_activity = enrolled_users.filter(
                updated_at__gte=seven_days_ago
            ).count()
            
            course_analytics.append({
                'course': course,
                'interactive_course': ic,
                'total_bankers': total_bankers,
                'enrolled_count': enrolled_count,
                'not_enrolled_count': not_enrolled_count,
                'in_progress_count': in_progress_count,
                'completed_content_count': completed_content_count,
                'passed_quiz_count': passed_quiz_count,
                'avg_completion': round(avg_completion, 1),
                'recent_activity': recent_activity,
                'enrollment_rate': round((enrolled_count / total_bankers * 100) if total_bankers > 0 else 0, 1),
                'completion_rate': round((passed_quiz_count / enrolled_count * 100) if enrolled_count > 0 else 0, 1),
            })
    
    # Overall statistics
    total_enrollments = InteractiveCourseProgress.objects.count()
    total_completed = InteractiveCourseProgress.objects.filter(content_completed=True).count()
    total_certificates = Certificate.objects.filter(is_valid=True).count()
    
    # Get detailed user list with their status
    user_progress_list = []
    
    for banker in all_bankers:
        user_data = {
            'user': banker,
            'full_name': banker.get_full_name() or banker.username,
            'email': banker.email,
            'last_login': banker.last_login,
            'has_logged_in': banker.last_login is not None,
            'courses': []
        }
        
        for ic in interactive_courses:
            progress = InteractiveCourseProgress.objects.filter(
                user=banker,
                interactive_course=ic
            ).first()
            
            certificate = Certificate.objects.filter(
                user=banker,
                interactive_course=ic,
                is_valid=True
            ).first()
            
            if progress:
                status = 'completed' if certificate else ('in_progress' if progress.completion_percentage < 100 else 'awaiting_quiz')
                course_data = {
                    'course': ic,
                    'status': status,
                    'progress': progress.completion_percentage,
                    'has_certificate': bool(certificate),
                    'last_activity': progress.updated_at,
                    'started_at': progress.started_at,
                }
            else:
                course_data = {
                    'course': ic,
                    'status': 'not_started',
                    'progress': 0,
                    'has_certificate': False,
                    'last_activity': None,
                    'started_at': None,
                }
            
            user_data['courses'].append(course_data)
        
        user_progress_list.append(user_data)
    
    # Sort users: in_progress first, then not_started, then completed
    def sort_key(user_data):
        statuses = [c['status'] for c in user_data['courses']]
        if 'in_progress' in statuses:
            return 0
        elif 'not_started' in statuses:
            return 1
        else:
            return 2
    
    user_progress_list.sort(key=sort_key)
    
    context = {
        'course_analytics': course_analytics,
        'total_bankers': total_bankers,
        'total_enrollments': total_enrollments,
        'total_completed': total_completed,
        'total_certificates': total_certificates,
        'overall_enrollment_rate': round((total_enrollments / total_bankers * 100) if total_bankers > 0 else 0, 1),
        'overall_completion_rate': round((total_certificates / total_enrollments * 100) if total_enrollments > 0 else 0, 1),
        'user_progress_list': user_progress_list,
        'interactive_courses': interactive_courses,
    }
    
    return render(request, 'progress/course_analytics.html', context)
