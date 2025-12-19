from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Question, QuizAttempt, QuizAnswer, QuestionOption
from courses.models import Course, Enrollment
from certificates.models import Certificate
from videos.models import VideoProgress, InteractiveCourse, InteractiveCourseProgress
import random
import uuid

@login_required
def start_quiz_view(request, course_id):
    """Start a new quiz attempt for a course"""
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is enrolled
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    # Check if all videos are completed
    total_videos = course.videos.count()
    completed_videos = VideoProgress.objects.filter(
        user=request.user,
        video__course=course,
        is_completed=True
    ).count()
    
    if completed_videos < total_videos:
        messages.error(request, f'You must complete all videos before taking the quiz. ({completed_videos}/{total_videos} completed)')
        return redirect('courses:course_detail', course_id=course.id)
    
    # Check if all interactive courses are completed
    total_interactive = InteractiveCourse.objects.filter(course=course).count()
    completed_interactive = InteractiveCourseProgress.objects.filter(
        user=request.user,
        interactive_course__course=course,
        is_completed=True
    ).count()
    
    if completed_interactive < total_interactive:
        messages.error(request, f'You must complete all interactive modules before taking the quiz. ({completed_interactive}/{total_interactive} completed)')
        return redirect('courses:course_detail', course_id=course.id)
    
    # Get all questions for this course grouped by topic
    questions = list(Question.objects.filter(course=course))
    
    # Randomly select questions (ensure different questions each time)
    if len(questions) > 20:
        selected_questions = random.sample(questions, 20)
    else:
        selected_questions = questions
    
    # Create quiz attempt with question IDs stored in database (not session)
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        course=course,
        total_questions=len(selected_questions),
        question_ids=[q.id for q in selected_questions]  # Store in DB for persistence
    )
    
    return redirect('quizzes:take', attempt_id=quiz_attempt.id)

@login_required
def take_quiz_view(request, attempt_id):
    """Display quiz questions"""
    quiz_attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    # Check if quiz already completed
    if quiz_attempt.completed_at:
        messages.info(request, 'This quiz has already been completed.')
        return redirect('quizzes:results', attempt_id=quiz_attempt.id)
    
    # Get question IDs from database (persistent across sessions)
    question_ids = quiz_attempt.question_ids or []
    
    if not question_ids:
        messages.error(request, 'Quiz questions not found. Please start a new quiz.')
        if quiz_attempt.interactive_course:
            return redirect('content:play_interactive', 
                           course_id=quiz_attempt.interactive_course.course.id, 
                           interactive_id=quiz_attempt.interactive_course.id)
        elif quiz_attempt.course:
            return redirect('courses:course_detail', course_id=quiz_attempt.course.id)
        return redirect('courses:course_list')
    
    questions = Question.objects.filter(id__in=question_ids).prefetch_related('options')
    
    context = {
        'quiz_attempt': quiz_attempt,
        'questions': questions,
        'course': quiz_attempt.course,
        'interactive_course': quiz_attempt.interactive_course,
    }
    
    return render(request, 'quizzes/take_quiz.html', context)

@login_required
def submit_quiz_view(request, attempt_id):
    """Submit quiz and calculate score"""
    if request.method != 'POST':
        return redirect('quizzes:take', attempt_id=attempt_id)
    
    quiz_attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    # Check if quiz already completed
    if quiz_attempt.completed_at:
        messages.info(request, 'This quiz has already been submitted.')
        return redirect('quizzes:results', attempt_id=quiz_attempt.id)
    
    # Get question IDs from database (persistent across sessions)
    question_ids = quiz_attempt.question_ids or []
    questions = Question.objects.filter(id__in=question_ids).prefetch_related('options')
    
    correct_answers = 0
    
    for question in questions:
        # Get user's selected options
        selected_option_ids = request.POST.getlist(f'question_{question.id}')
        
        if selected_option_ids:
            # Create quiz answer
            quiz_answer = QuizAnswer.objects.create(
                attempt=quiz_attempt,
                question=question
            )
            
            # Get selected options
            selected_options = QuestionOption.objects.filter(id__in=selected_option_ids)
            quiz_answer.selected_options.set(selected_options)
            
            # Check if answer is correct
            correct_options = question.options.filter(is_correct=True)
            selected_correct = set(selected_options.filter(is_correct=True).values_list('id', flat=True))
            all_correct = set(correct_options.values_list('id', flat=True))
            
            if selected_correct == all_correct and len(selected_option_ids) == len(all_correct):
                quiz_answer.is_correct = True
                correct_answers += 1
            
            quiz_answer.save()
    
    # Calculate score
    score = (correct_answers / quiz_attempt.total_questions) * 100 if quiz_attempt.total_questions > 0 else 0
    quiz_attempt.score = score
    quiz_attempt.correct_answers = correct_answers
    
    # Determine passing (80% for both course and interactive course)
    passing_score = 80
    if quiz_attempt.course:
        passing_score = quiz_attempt.course.passing_score
    
    quiz_attempt.passed = score >= passing_score
    quiz_attempt.completed_at = timezone.now()
    quiz_attempt.save()
    
    # Update interactive course progress if this is an interactive course quiz
    if quiz_attempt.interactive_course and quiz_attempt.passed:
        progress = InteractiveCourseProgress.objects.filter(
            user=request.user,
            interactive_course=quiz_attempt.interactive_course
        ).first()
        
        if progress:
            progress.quiz_score = score
            progress.quiz_passed = True
            progress.quiz_attempts += 1
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()
            
            # Generate certificate for interactive course
            check_and_generate_interactive_certificate(request.user, quiz_attempt.interactive_course, score)
    
    # Check if user is eligible for certificate (for regular courses)
    if quiz_attempt.course and quiz_attempt.passed:
        check_and_generate_certificate(request.user, quiz_attempt.course)
    
    return redirect('quizzes:results', attempt_id=quiz_attempt.id)

@login_required
def quiz_results_view(request, attempt_id):
    """Display quiz results"""
    quiz_attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    # Check if user has certificate
    user_certificate = None
    if quiz_attempt.passed:
        if quiz_attempt.interactive_course:
            user_certificate = Certificate.objects.filter(
                user=request.user,
                interactive_course=quiz_attempt.interactive_course
            ).first()
        elif quiz_attempt.course:
            user_certificate = Certificate.objects.filter(
                user=request.user,
                course=quiz_attempt.course
            ).first()
    
    context = {
        'quiz_attempt': quiz_attempt,
        'user_certificate': user_certificate,
        'course': quiz_attempt.course,
        'interactive_course': quiz_attempt.interactive_course,
    }
    
    return render(request, 'quizzes/quiz_results.html', context)

def check_and_generate_certificate(user, course):
    """Check if user is eligible for certificate and generate if criteria met"""
    
    # Check if certificate already exists for this course
    existing_cert = Certificate.objects.filter(user=user, course=course).first()
    if existing_cert:
        return existing_cert
    
    # Check if all videos are completed
    total_videos = course.videos.count()
    completed_videos = VideoProgress.objects.filter(
        user=user,
        video__course=course,
        is_completed=True
    ).count()
    
    if completed_videos < total_videos:
        return None  # Not all videos completed
    
    # Check if quiz is passed with at least 80%
    passed_attempts = QuizAttempt.objects.filter(
        user=user,
        course=course,
        passed=True,
        completed_at__isnull=False
    ).order_by('-score')
    
    if not passed_attempts.exists():
        return None  # No passed quiz attempts
    
    best_attempt = passed_attempts.first()
    
    # Generate certificate
    certificate_number = f'COOP-TZ-{uuid.uuid4().hex[:8].upper()}'
    
    # Create verification URL (will be set properly when request context is available)
    from django.conf import settings
    base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
    verification_url = f'{base_url}/certificates/verify/{certificate_number}/'
    
    certificate = Certificate.objects.create(
        user=user,
        course=course,
        certificate_number=certificate_number,
        overall_score=best_attempt.score,
        verification_url=verification_url
    )
    
    # Generate QR code and PDF
    certificate.generate_qr_code()
    
    # Import here to avoid circular imports
    from certificates.views import generate_certificate_pdf
    generate_certificate_pdf(certificate)
    
    certificate.save()
    
    return certificate


def check_and_generate_interactive_certificate(user, interactive_course, score):
    """Generate certificate for interactive course completion"""
    from certificates.models import Certificate
    
    # Check if certificate already exists
    existing_cert = Certificate.objects.filter(
        user=user, 
        interactive_course=interactive_course
    ).first()
    
    if existing_cert:
        return existing_cert
    
    # Generate certificate
    certificate_number = f'COOP-IC-{uuid.uuid4().hex[:8].upper()}'
    
    from django.conf import settings
    base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
    verification_url = f'{base_url}/certificates/verify/{certificate_number}/'
    
    certificate = Certificate.objects.create(
        user=user,
        interactive_course=interactive_course,
        certificate_number=certificate_number,
        overall_score=score,
        verification_url=verification_url
    )
    
    # Generate QR code and PDF
    certificate.generate_qr_code()
    
    from certificates.views import generate_certificate_pdf
    generate_certificate_pdf(certificate)
    
    certificate.save()
    
    return certificate


# =====================================================
# INTERACTIVE COURSE QUIZ VIEWS
# =====================================================

@login_required
def start_interactive_quiz(request, interactive_id):
    """Start a quiz for an interactive course"""
    interactive_course = get_object_or_404(InteractiveCourse, id=interactive_id)
    
    # Check if user has completed all slides
    progress = InteractiveCourseProgress.objects.filter(
        user=request.user,
        interactive_course=interactive_course
    ).first()
    
    # Check completion - either content_completed flag OR highest_slide_reached >= total_slides
    total_slides = interactive_course.total_slides
    is_content_completed = False
    
    if progress:
        # Check both conditions - flag or actual slide count
        is_content_completed = progress.content_completed or progress.highest_slide_reached >= total_slides
        
        # If slides are done but flag wasn't set, fix it now
        if progress.highest_slide_reached >= total_slides and not progress.content_completed:
            progress.content_completed = True
            from django.utils import timezone
            progress.content_completed_at = timezone.now()
            progress.completion_percentage = 100
            progress.save()
    
    if not progress or not is_content_completed:
        messages.error(request, 'You must complete all slides before taking the quiz.')
        return redirect('content:play_interactive', 
                       course_id=interactive_course.course.id, 
                       interactive_id=interactive_course.id)
    
    # Get all questions for this interactive course
    questions = list(Question.objects.filter(interactive_course=interactive_course))
    
    if not questions:
        messages.error(request, 'No questions available for this course yet.')
        return redirect('content:play_interactive', 
                       course_id=interactive_course.course.id, 
                       interactive_id=interactive_course.id)
    
    # Randomly select questions (max 20)
    if len(questions) > 20:
        selected_questions = random.sample(questions, 20)
    else:
        selected_questions = questions
    
    # Create quiz attempt
    # Create quiz attempt with question IDs stored in database (not session)
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        interactive_course=interactive_course,
        total_questions=len(selected_questions),
        question_ids=[q.id for q in selected_questions]  # Store in DB for persistence
    )
    
    return redirect('quizzes:take', attempt_id=quiz_attempt.id)


@login_required
def manage_interactive_questions(request, interactive_id):
    """View and manage questions for an interactive course (admin only)"""
    interactive_course = get_object_or_404(InteractiveCourse, id=interactive_id)
    
    # Check if user has permission
    if not request.user.can_upload_content():
        messages.error(request, "You don't have permission to manage questions.")
        return redirect('courses:dashboard')
    
    questions = Question.objects.filter(interactive_course=interactive_course).prefetch_related('options')
    
    # Group questions by topic
    questions_by_topic = {}
    for q in questions:
        topic = q.topic or 'General'
        if topic not in questions_by_topic:
            questions_by_topic[topic] = []
        questions_by_topic[topic].append(q)
    
    context = {
        'interactive_course': interactive_course,
        'course': interactive_course.course,
        'questions': questions,
        'questions_by_topic': questions_by_topic,
        'total_questions': questions.count(),
    }
    
    return render(request, 'quizzes/manage_interactive_questions.html', context)


@login_required
def add_interactive_question(request, interactive_id):
    """Add a new question to an interactive course"""
    interactive_course = get_object_or_404(InteractiveCourse, id=interactive_id)
    
    if not request.user.can_upload_content():
        messages.error(request, "You don't have permission to add questions.")
        return redirect('courses:dashboard')
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        question_type = request.POST.get('question_type', 'multiple_choice')
        topic = request.POST.get('topic', '')
        difficulty = request.POST.get('difficulty', 'medium')
        points = int(request.POST.get('points', 1))
        
        # Create question
        question = Question.objects.create(
            interactive_course=interactive_course,
            question_text=question_text,
            question_type=question_type,
            topic=topic,
            difficulty=difficulty,
            points=points
        )
        
        # Add options
        option_count = int(request.POST.get('option_count', 4))
        for i in range(1, option_count + 1):
            option_text = request.POST.get(f'option_{i}')
            is_correct = request.POST.get(f'correct_{i}') == 'on'
            
            if option_text:
                QuestionOption.objects.create(
                    question=question,
                    option_text=option_text,
                    is_correct=is_correct,
                    order_index=i
                )
        
        messages.success(request, 'Question added successfully!')
        return redirect('quizzes:manage_interactive_questions', interactive_id=interactive_id)
    
    context = {
        'interactive_course': interactive_course,
        'course': interactive_course.course,
        'question_types': Question.QUESTION_TYPES,
        'difficulty_levels': Question.DIFFICULTY_LEVELS,
    }
    
    return render(request, 'quizzes/add_interactive_question.html', context)


@login_required
def edit_interactive_question(request, question_id):
    """Edit an existing question"""
    question = get_object_or_404(Question, id=question_id)
    
    if not request.user.can_upload_content():
        messages.error(request, "You don't have permission to edit questions.")
        return redirect('courses:dashboard')
    
    if request.method == 'POST':
        question.question_text = request.POST.get('question_text')
        question.question_type = request.POST.get('question_type', 'multiple_choice')
        question.topic = request.POST.get('topic', '')
        question.difficulty = request.POST.get('difficulty', 'medium')
        question.points = int(request.POST.get('points', 1))
        question.save()
        
        # Delete existing options and recreate
        question.options.all().delete()
        
        option_count = int(request.POST.get('option_count', 4))
        for i in range(1, option_count + 1):
            option_text = request.POST.get(f'option_{i}')
            is_correct = request.POST.get(f'correct_{i}') == 'on'
            
            if option_text:
                QuestionOption.objects.create(
                    question=question,
                    option_text=option_text,
                    is_correct=is_correct,
                    order_index=i
                )
        
        messages.success(request, 'Question updated successfully!')
        
        if question.interactive_course:
            return redirect('quizzes:manage_interactive_questions', 
                          interactive_id=question.interactive_course.id)
        else:
            return redirect('courses:dashboard')
    
    context = {
        'question': question,
        'interactive_course': question.interactive_course,
        'course': question.interactive_course.course if question.interactive_course else question.course,
        'question_types': Question.QUESTION_TYPES,
        'difficulty_levels': Question.DIFFICULTY_LEVELS,
    }
    
    return render(request, 'quizzes/edit_interactive_question.html', context)


@login_required
def delete_interactive_question(request, question_id):
    """Delete a question"""
    question = get_object_or_404(Question, id=question_id)
    
    if not request.user.can_upload_content():
        messages.error(request, "You don't have permission to delete questions.")
        return redirect('courses:dashboard')
    
    interactive_id = question.interactive_course.id if question.interactive_course else None
    question.delete()
    
    messages.success(request, 'Question deleted successfully!')
    
    if interactive_id:
        return redirect('quizzes:manage_interactive_questions', interactive_id=interactive_id)
    return redirect('courses:dashboard')
