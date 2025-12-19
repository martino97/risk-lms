from django.db import models
from django.conf import settings
from courses.models import Course
from videos.models import InteractiveCourse
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
import os

class Certificate(models.Model):
    """Certificate model for course completion"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates', null=True, blank=True)
    interactive_course = models.ForeignKey(InteractiveCourse, on_delete=models.CASCADE, related_name='certificates', null=True, blank=True)
    certificate_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateTimeField(default=timezone.now)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    qr_code = models.ImageField(upload_to='certificates/qr_codes/', blank=True)
    pdf_file = models.FileField(upload_to='certificates/pdfs/', blank=True)
    verification_url = models.URLField(max_length=500)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'certificates'
        ordering = ['-issue_date']
    
    def __str__(self):
        course_title = self.course.title if self.course else (self.interactive_course.title if self.interactive_course else 'Unknown')
        return f"{self.user.get_full_name()} - {course_title} - {self.certificate_number}"
    
    def get_course_title(self):
        """Get the title of the course or interactive course"""
        if self.course:
            return self.course.title
        elif self.interactive_course:
            return self.interactive_course.title
        return 'Risk Management Program'
    
    def generate_qr_code(self):
        """Generate QR code for certificate verification with comprehensive user details"""
        import json
        from django.utils import timezone
        
        course_title = self.get_course_title()
        
        # Create comprehensive, immediately readable QR data - no web lookup needed
        qr_text = f"""🏆 CERTIFICATE OF COMPLETION 🏆

📜 Certificate #: {self.certificate_number}
👤 Full Name: {self.user.get_full_name()}
📧 Email: {self.user.email}
🆔 Username: {self.user.username}
📚 Course: {course_title}
📊 Final Score: {self.overall_score:.1f}%
📅 Completed: {self.issue_date.strftime('%B %d, %Y')}
🏦 Issuing Bank: Co-operative Bank of Tanzania PLC
🏢 Department: Risk Management & Compliance
🌐 Website: www.coopbank.co.tz
✅ Status: VALID & AUTHENTIC

This certificate confirms successful completion of the Risk Management training program with a score of {self.overall_score:.1f}%. 

Verification: {self.verification_url}
Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} EAT"""
        
        qr = qrcode.QRCode(
            version=4,  # Larger version for more detailed data
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium error correction for larger data
            box_size=12,  # Good balance of size and scannability
            border=2,  # Minimal border
        )
        qr.add_data(qr_text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        filename = f'{self.certificate_number}_qr.png'
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()
