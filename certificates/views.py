from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Avg
from .models import Certificate
from courses.models import Course, Enrollment
from quizzes.models import QuizAttempt
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import uuid
from io import BytesIO

@login_required
def my_certificates_view(request):
    """Display user's certificates"""
    certificates = Certificate.objects.filter(user=request.user)
    
    context = {
        'certificates': certificates,
    }
    
    return render(request, 'certificates/my_certificates.html', context)

@login_required
def certificate_detail_view(request, certificate_id):
    """Display certificate details with download option"""
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    
    context = {
        'certificate': certificate,
    }
    
    return render(request, 'certificates/certificate_detail.html', context)

@login_required
def download_certificate_view(request, certificate_id):
    """Download certificate PDF"""
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    
    if not certificate.pdf_file:
        # Generate PDF if it doesn't exist
        generate_certificate_pdf(certificate)
        certificate.save()
    
    if certificate.pdf_file:
        response = HttpResponse(
            certificate.pdf_file.read(),
            content_type='application/pdf'
        )
        filename = f'Certificate_{certificate.certificate_number}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse('Certificate PDF not available', status=404)

def verify_certificate_view(request, certificate_number):
    """Public certificate verification"""
    try:
        certificate = Certificate.objects.get(certificate_number=certificate_number)
        
        context = {
            'certificate': certificate,
            'valid': certificate.is_valid,
        }
        
        return render(request, 'certificates/verify.html', context)
    except Certificate.DoesNotExist:
        context = {
            'valid': False,
            'message': 'Certificate not found'
        }
        return render(request, 'certificates/verify.html', context)

@login_required
def generate_certificate_view(request):
    """Generate certificate after completing all courses with 80% average"""
    user = request.user
    
    # Get all enrollments
    enrollments = Enrollment.objects.filter(user=user)
    
    if enrollments.count() == 0:
        return JsonResponse({'error': 'No courses enrolled'}, status=400)
    
    # Calculate average score across all courses
    total_score = 0
    completed_courses = 0
    
    for enrollment in enrollments:
        course = enrollment.course
        
        # Check if all videos are watched
        total_videos = course.videos.count()
        from videos.models import VideoProgress, InteractiveCourse, InteractiveCourseProgress
        completed_videos = VideoProgress.objects.filter(
            user=user,
            video__course=course,
            is_completed=True
        ).count()
        
        if completed_videos < total_videos:
            continue
        
        # Check if all interactive courses are completed
        total_interactive = InteractiveCourse.objects.filter(course=course).count()
        completed_interactive = InteractiveCourseProgress.objects.filter(
            user=user,
            interactive_course__course=course,
            is_completed=True
        ).count()
        
        if completed_interactive < total_interactive:
            continue
        
        # Get best quiz score for this course
        quiz_attempts = QuizAttempt.objects.filter(
            user=user,
            course=course,
            completed_at__isnull=False,
            passed=True
        )
        
        if quiz_attempts.count() == 0:
            continue
        
        best_score = quiz_attempts.aggregate(Avg('score'))['score__avg']
        total_score += best_score
        completed_courses += 1
    
    if completed_courses == 0:
        return JsonResponse({'error': 'No courses completed. You must complete all videos, interactive modules, and pass the quiz.'}, status=400)
    
    average_score = total_score / completed_courses
    
    # Check if average is at least 80%
    if average_score < 80:
        return JsonResponse({
            'error': f'Average score is {average_score:.2f}%. Minimum 80% required.',
            'average_score': average_score
        }, status=400)
    
    # Generate unique certificate number
    certificate_number = f'RISK-{uuid.uuid4().hex[:8].upper()}'
    
    # Create verification URL
    verification_url = request.build_absolute_uri(f'/certificates/verify/{certificate_number}/')
    
    # Create certificate
    certificate = Certificate.objects.create(
        user=user,
        certificate_number=certificate_number,
        overall_score=average_score,
        verification_url=verification_url
    )
    
    # Generate QR code
    certificate.generate_qr_code()
    
    # Generate PDF
    generate_certificate_pdf(certificate)
    
    certificate.save()
    
    return JsonResponse({
        'success': True,
        'certificate_id': certificate.id,
        'certificate_number': certificate_number,
        'average_score': average_score
    })

def generate_certificate_pdf(certificate):
    """Generate professional A4 PDF certificate with Co-operative Bank Tanzania PLC branding"""
    buffer = BytesIO()
    
    # Create PDF - A4 Portrait format
    from reportlab.lib.pagesizes import A4
    pagesize = A4
    p = canvas.Canvas(buffer, pagesize=pagesize)
    width, height = pagesize
    
    # Co-operative Bank Tanzania PLC Colors
    from reportlab.lib.colors import HexColor, white, black
    coop_blue = HexColor('#0052CC')       # Co-op Bank blue
    coop_dark_blue = HexColor('#002B5C')  # Navy blue
    coop_green = HexColor('#00A651')      # Co-op Bank green
    coop_light_blue = HexColor('#E6F0FF') # Light blue tint
    dark_gray = HexColor('#333333')
    
    # Margin settings
    margin = 0.4*inch
    inner_margin = 0.6*inch
    
    # === WHITE BACKGROUND ===
    p.setFillColor(white)
    p.rect(0, 0, width, height, fill=True, stroke=False)
    
    # === WATERMARK LOGO IN CENTER BACKGROUND ===
    try:
        import os
        from django.conf import settings
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'CoopLogo.png')
        
        if os.path.exists(logo_path):
            p.saveState()
            watermark_size = 4.5*inch
            watermark_x = (width - watermark_size) / 2
            watermark_y = (height - watermark_size) / 2
            p.setFillAlpha(0.06)
            p.setStrokeAlpha(0.06)
            logo_img = ImageReader(logo_path)
            p.drawImage(logo_img, watermark_x, watermark_y, width=watermark_size, height=watermark_size, mask='auto')
            p.restoreState()
    except Exception as e:
        print(f"Watermark error: {e}")
    
    # === ELEGANT TOP BANNER - Smooth Blue to Green Gradient ===
    banner_height = 1.0*inch
    num_strips = 60
    strip_height = banner_height / num_strips
    
    for i in range(num_strips):
        # Smooth gradient from Navy Blue (#002B5C) -> Blue (#0052CC) -> Green (#00A651)
        if i < num_strips / 2:
            # Navy to Blue
            progress = i / (num_strips / 2)
            r = 0
            g = int(43 + (82 - 43) * progress)
            b = int(92 + (204 - 92) * progress)
        else:
            # Blue to Green
            progress = (i - num_strips / 2) / (num_strips / 2)
            r = 0
            g = int(82 + (166 - 82) * progress)
            b = int(204 + (81 - 204) * progress)
        
        p.setFillColor(HexColor(f'#{r:02x}{g:02x}{b:02x}'))
        p.rect(0, height - (i + 1) * strip_height, width, strip_height + 1, fill=True, stroke=False)
    
    # === ELEGANT BOTTOM BANNER - Smooth Green to Blue Gradient ===
    for i in range(num_strips):
        # Smooth gradient from Green (#00A651) -> Blue (#0052CC) -> Navy Blue (#002B5C)
        if i < num_strips / 2:
            # Green to Blue
            progress = i / (num_strips / 2)
            r = 0
            g = int(166 + (82 - 166) * progress)
            b = int(81 + (204 - 81) * progress)
        else:
            # Blue to Navy
            progress = (i - num_strips / 2) / (num_strips / 2)
            r = 0
            g = int(82 + (43 - 82) * progress)
            b = int(204 + (92 - 204) * progress)
        
        p.setFillColor(HexColor(f'#{r:02x}{g:02x}{b:02x}'))
        p.rect(0, (num_strips - i - 1) * strip_height, width, strip_height + 1, fill=True, stroke=False)
    
    # === GRADIENT BORDER (Blue to Green) ===
    # Outer border - Navy Blue
    p.setStrokeColor(coop_dark_blue)
    p.setLineWidth(4)
    p.rect(margin, margin + 0.65*inch, width - 2*margin, height - 2*margin - 0.65*inch)
    
    # Inner border - Green
    p.setStrokeColor(coop_green)
    p.setLineWidth(2)
    p.rect(margin + 10, margin + 0.65*inch + 10, width - 2*margin - 20, height - 2*margin - 0.65*inch - 20)
    
    content_top = height - banner_height - 0.4*inch
    
    # === LOGO SECTION (Top) ===
    try:
        import os
        from django.conf import settings
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'CoopLogo.png')
        
        if os.path.exists(logo_path):
            logo_img = ImageReader(logo_path)
            logo_size = 1.1*inch
            logo_x = (width - logo_size) / 2
            p.drawImage(logo_img, logo_x, content_top - logo_size + 0.2*inch, width=logo_size, height=logo_size, mask='auto')
            content_top -= logo_size + 0.15*inch
    except Exception as e:
        print(f"Logo error: {e}")
        content_top -= 0.3*inch
    
    # === BANK NAME ===
    p.setFillColor(coop_dark_blue)
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width / 2, content_top, "CO-OPERATIVE BANK TANZANIA PLC")
    content_top -= 0.7*inch
    
    # === CERTIFICATE TITLE ===
    # Decorative line - Blue gradient effect
    line_width = 3*inch
    p.setStrokeColor(coop_blue)
    p.setLineWidth(2)
    p.line((width - line_width)/2, content_top + 0.15*inch, (width + line_width)/2, content_top + 0.15*inch)
    
    p.setFillColor(coop_dark_blue)
    p.setFont("Helvetica-Bold", 42)
    p.drawCentredString(width / 2, content_top - 0.5*inch, "CERTIFICATE")
    content_top -= 0.85*inch
    
    p.setFillColor(coop_green)
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width / 2, content_top - 0.1*inch, "OF COMPLETION")
    content_top -= 0.55*inch
    
    # Bottom decorative line - Green
    p.setStrokeColor(coop_green)
    p.setLineWidth(2)
    p.line((width - line_width)/2, content_top, (width + line_width)/2, content_top)
    content_top -= 0.65*inch
    
    # === RECIPIENT SECTION ===
    p.setFillColor(dark_gray)
    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2, content_top, "This is to certify that")
    content_top -= 0.6*inch
    
    participant_name = certificate.user.get_full_name().upper()
    if not participant_name.strip():
        participant_name = certificate.user.username.upper()
    
    p.setFillColor(coop_dark_blue)
    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(width / 2, content_top, participant_name)
    content_top -= 0.25*inch
    
    # Name underline - gradient effect (draw two lines)
    name_width = p.stringWidth(participant_name, "Helvetica-Bold", 30)
    p.setStrokeColor(coop_blue)
    p.setLineWidth(2)
    p.line((width - name_width)/2 - 40, content_top, width/2, content_top)
    p.setStrokeColor(coop_green)
    p.line(width/2, content_top, (width + name_width)/2 + 40, content_top)
    content_top -= 0.65*inch
    
    # === COURSE SECTION ===
    p.setFillColor(dark_gray)
    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2, content_top, "has successfully completed the training course")
    content_top -= 0.55*inch
    
    course_title = certificate.get_course_title()
    p.setFillColor(coop_blue)
    p.setFont("Helvetica-Bold", 17)
    
    if len(course_title) > 45:
        words = course_title.split()
        mid = len(words) // 2
        line1 = ' '.join(words[:mid])
        line2 = ' '.join(words[mid:])
        p.drawCentredString(width / 2, content_top, line1.upper())
        content_top -= 0.3*inch
        p.drawCentredString(width / 2, content_top, line2.upper())
    else:
        p.drawCentredString(width / 2, content_top, course_title.upper())
    content_top -= 0.55*inch
    
    # === OFFERED BY ===
    p.setFillColor(coop_green)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, content_top, "Offered by Co-operative Bank Tanzania PLC")
    content_top -= 0.7*inch
    
    # === BOTTOM SECTION - 3 Columns ===
    bottom_section_y = 1.8*inch
    col_width = (width - 2*inner_margin) / 3
    
    # --- Left Column: Date & Certificate Number ---
    left_x = inner_margin + col_width/2
    
    p.setFillColor(coop_dark_blue)
    p.setFont("Helvetica", 9)
    p.drawCentredString(left_x, bottom_section_y + 0.55*inch, "DATE OF ISSUE")
    p.setFont("Helvetica-Bold", 11)
    p.setFillColor(dark_gray)
    p.drawCentredString(left_x, bottom_section_y + 0.32*inch, certificate.issue_date.strftime('%B %d, %Y'))
    
    p.setFillColor(coop_dark_blue)
    p.setFont("Helvetica", 9)
    p.drawCentredString(left_x, bottom_section_y + 0.05*inch, "CERTIFICATE NO.")
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(dark_gray)
    p.drawCentredString(left_x, bottom_section_y - 0.15*inch, certificate.certificate_number)
    
    # --- Center Column: QR Code ---
    center_x = width / 2
    
    if certificate.qr_code:
        try:
            qr_img = ImageReader(certificate.qr_code.path)
            qr_size = 1.2*inch
            qr_x = center_x - qr_size/2
            qr_y = bottom_section_y - 0.3*inch
            
            p.setFillColor(white)
            p.setStrokeColor(coop_green)
            p.setLineWidth(2)
            p.roundRect(qr_x - 5, qr_y - 5, qr_size + 10, qr_size + 10, 4, fill=True, stroke=True)
            
            p.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size)
            
            p.setFillColor(coop_dark_blue)
            p.setFont("Helvetica-Bold", 7)
            p.drawCentredString(center_x, qr_y - 12, "SCAN TO VERIFY")
        except Exception as e:
            print(f"QR error: {e}")
    
    # --- Right Column: HEAD OF RISK SIGNATURE ---
    right_x = width - inner_margin - col_width/2
    
    p.setStrokeColor(coop_dark_blue)
    p.setLineWidth(1.5)
    sig_line_width = 1.6*inch
    p.line(right_x - sig_line_width/2, bottom_section_y + 0.35*inch, right_x + sig_line_width/2, bottom_section_y + 0.35*inch)
    
    p.setFillColor(coop_dark_blue)
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(right_x, bottom_section_y + 0.12*inch, "HEAD OF RISK")
    
    p.setFillColor(dark_gray)
    p.setFont("Helvetica", 9)
    p.drawCentredString(right_x, bottom_section_y - 0.08*inch, "Risk Department")
    
    p.setFillColor(coop_green)
    p.setFont("Helvetica-Bold", 8)
    p.drawCentredString(right_x, bottom_section_y - 0.26*inch, "Co-operative Bank Tanzania PLC")
    
    # === FOOTER ===
    footer_y = 0.6*inch
    p.setFillColor(white)
    p.setFont("Helvetica", 8)
    p.drawCentredString(width / 2, footer_y + 0.15*inch, "This certificate is electronically generated and can be verified by scanning the QR code")
    p.setFont("Helvetica-Bold", 9)
    p.drawCentredString(width / 2, footer_y - 0.05*inch, "Copyright © 2025 Co-operative Bank Tanzania PLC")
    
    # Finish PDF
    p.showPage()
    p.save()
    
    # Save to file field
    buffer.seek(0)
    filename = f'{certificate.certificate_number}.pdf'
    from django.core.files import File
    certificate.pdf_file.save(filename, File(buffer), save=False)
    buffer.close()
