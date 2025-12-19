# Risk Department Learning Management System - Django Edition

A comprehensive Learning Management System (LMS) built with **Django** for risk department training, featuring video tutorials with translations, mandatory viewing enforcement, randomized quizzes, and automated certificate generation with QR code verification.

## ✨ Key Features

### 🎥 Video Management
- Upload video tutorials with automatic FFmpeg processing
- Multi-language subtitle support (SRT, VTT formats)
- **Mandatory viewing enforcement** - 95% completion required, no skipping allowed
- Real-time progress tracking (updates every 5 seconds via AJAX)
- Support for various video formats (MP4, AVI, MKV, WebM)
- Video duration auto-detection

### 📝 Assessment System  
- **Random question selection** from topic-based pools
- Multiple question types: multiple choice, true/false, multiple answer
- **Unique quiz experience** for each attempt - no two quizzes are the same
- **80% passing benchmark** required across all courses
- Automatic grading with instant results
- Unlimited quiz retakes until passing

### 🎓 Certificate Generation
- **Automatic certificate generation** upon 80% average achievement
- **QR code** embedded in certificates for instant verification
- **Professional PDF certificates** with ReportLab
- Unique certificate numbers (RISK-XXXXXXXX format)
- **Public verification portal** for employers and auditors
- Certificate revocation capability for admins

### 👥 User Roles & Permissions
- **Admin**: Full system access via Django admin interface
- **Risk Admin**: Create courses, upload videos, manage question banks, view all user progress
- **Banker**: Enroll in courses, watch videos (mandatory completion), take randomized quizzes, earn certificates

## 🛠️ Technology Stack

### Backend Framework
- **Django 4.2** - Full-featured web framework with ORM
- **Django REST Framework** - API endpoints for future mobile apps
- **PostgreSQL** - Production-grade relational database
- **Celery + Redis** - Asynchronous task processing (video encoding)

### Frontend
- **SB Admin 2** - Bootstrap-based responsive admin template
- **Django Templates** - Server-side rendering with Jinja2 syntax
- **Bootstrap 4** - Mobile-first responsive design
- **jQuery** - AJAX interactions and video progress tracking

### Additional Libraries
- **moviepy + FFmpeg** - Video processing and format conversion
- **ReportLab** - Professional PDF certificate generation
- **qrcode + Pillow** - QR code generation and image processing
- **django-cors-headers** - CORS support for API endpoints
- **WhiteNoise** - Static file serving in production
- **python-decouple** - Environment variable management

## 📋 Prerequisites

Before installation, ensure you have:
- **Python 3.9+** (Download: https://www.python.org/downloads/)
- **PostgreSQL 13+** (Download: https://www.postgresql.org/download/windows/)
- **FFmpeg** (Download: https://ffmpeg.org/download.html)
- **Git** (optional, for version control)

## 🚀 Quick Start Installation

### 1. Create Virtual Environment
```powershell
# Navigate to project directory
cd "c:\Users\Paul\New folder"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database
```sql
-- Open PostgreSQL command line (psql)
CREATE DATABASE risk_lms;
CREATE USER risk_admin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE risk_lms TO risk_admin;
```

### 4. Configure Environment Variables
```powershell
# Copy example environment file
copy .env.example .env

# Edit .env with your settings (use Notepad or VS Code)
notepad .env
```

Required settings in `.env`:
```env
SECRET_KEY=your-long-random-secret-key-here
DEBUG=True
DB_NAME=risk_lms
DB_USER=risk_admin
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```powershell
python manage.py createsuperuser
# Enter email, name, and password when prompted
```

### 7. Copy SB Admin 2 Template Files
```powershell
# Create static directories
New-Item -ItemType Directory -Force -Path "static/css", "static/js", "static/vendor"

# Copy from your desktop template
$template = "C:\Users\Paul\Desktop\startbootstrap-sb-admin-2-gh-pages"
Copy-Item "$template\css\*" -Destination "static\css\" -Recurse -Force
Copy-Item "$template\js\*" -Destination "static\js\" -Recurse -Force
Copy-Item "$template\vendor\*" -Destination "static\vendor\" -Recurse -Force

# Collect static files
python manage.py collectstatic --noinput
```

### 8. Start Development Server
```powershell
python manage.py runserver
```

**Application URLs:**
- Main Application: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- Login with your superuser credentials

## 📖 Complete Setup Guide

For detailed installation instructions, troubleshooting, and production deployment, see **[DJANGO_SETUP.md](DJANGO_SETUP.md)**

## 🎯 Usage Guide

### For Risk Admins

#### 1. Access Admin Panel
Navigate to http://localhost:8000/admin/ and login with admin credentials.

#### 2. Create Courses
- Go to **Courses** > **Add Course**
- Enter course title, description, passing score (default 80%)
- Save course

#### 3. Upload Videos
- Go to **Videos** > **Add Video**
- Select course from dropdown
- Upload video file (max 2GB)
- Add optional subtitles (SRT or VTT format)
- Video automatically processes via FFmpeg

#### 4. Build Question Banks
- Go to **Questions** > **Add Question**
- Select course and enter topic name
- Write question text and select type
- Add options (mark correct answers with checkbox)
- Set difficulty level (easy, medium, hard)

#### 5. Monitor User Progress
- View **Enrollments** to see who's enrolled
- Check **Quiz Attempts** for completion rates
- Review **Video Progress** for watch statistics

### For Bankers (Learners)

#### 1. Register & Login
- Visit http://localhost:8000/
- Click **Register** and create account
- Role automatically set to "Banker"

#### 2. Browse & Enroll in Courses
- View available courses from dashboard
- Click **Enroll** button on desired course
- Access course materials immediately

#### 3. Watch Videos (Mandatory Viewing)
- Click on video to open player
- Videos **must be watched to 95% completion**
- Progress tracked every 5 seconds via AJAX
- **Cannot skip ahead** - enforced by backend validation
- Must complete all videos before accessing quiz

#### 4. Take Randomized Quiz
- Quiz becomes available after all videos completed
- Questions randomly selected from topic pools
- **Each attempt has different questions**
- Submit answers when complete
- View instant results with score breakdown

#### 5. Earn Certificate
- Complete all enrolled courses
- Maintain **80% average score** across all quizzes
- Certificate auto-generates with unique QR code
- Download professional PDF certificate
- Share verification link with employers

## 🌐 URL Routes

| Route | Description | Access |
|-------|-------------|--------|
| `/accounts/login/` | User login page | Public |
| `/accounts/register/` | User registration | Public |
| `/accounts/logout/` | Logout user | Authenticated |
| `/accounts/profile/` | User profile page | Authenticated |
| `/courses/` | List all courses | Authenticated |
| `/courses/<id>/` | Course details | Authenticated |
| `/courses/<id>/enroll/` | Enroll in course | Banker |
| `/videos/<id>/player/` | Video player with tracking | Enrolled |
| `/videos/<id>/update-progress/` | AJAX progress endpoint | Enrolled |
| `/quizzes/<course_id>/start/` | Start new quiz attempt | Enrolled |
| `/quizzes/attempt/<id>/` | Take quiz | Enrolled |
| `/quizzes/attempt/<id>/submit/` | Submit quiz answers | Enrolled |
| `/quizzes/attempt/<id>/results/` | View quiz results | Enrolled |
| `/progress/user/<id>/` | User progress overview | Authenticated |
| `/progress/course/<id>/` | Course progress report | Risk Admin |
| `/certificates/` | My certificates list | Authenticated |
| `/certificates/<id>/` | Certificate detail & download | Owner |
| `/certificates/verify/<number>/` | Public verification | Public |
| `/certificates/generate/` | Generate new certificate | Authenticated |
| `/admin/` | Django admin panel | Admin/Risk Admin |

## 📁 Project Structure

```
risk_lms/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create from .env.example)
├── .env.example                 # Example environment configuration
├── DJANGO_SETUP.md              # Detailed setup instructions
├── README.md                    # This file
│
├── risk_lms/                    # Main project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py                  # WSGI application
│
├── accounts/                    # User authentication & profiles
│   ├── models.py                # Custom User model with roles
│   ├── views.py                 # Login, register, profile views
│   ├── forms.py                 # User forms
│   ├── admin.py                 # User admin interface
│   └── urls.py                  # Account URLs
│
├── courses/                     # Course management
│   ├── models.py                # Course & Enrollment models
│   ├── views.py                 # Course list, detail, enrollment
│   ├── admin.py                 # Course admin interface
│   └── urls.py                  # Course URLs
│
├── videos/                      # Video upload & playback
│   ├── models.py                # Video, VideoSubtitle, VideoProgress models
│   ├── views.py                 # Video player, progress tracking
│   ├── admin.py                 # Video admin interface
│   └── urls.py                  # Video URLs
│
├── quizzes/                     # Quiz system
│   ├── models.py                # Question, QuizAttempt, QuizAnswer models
│   ├── views.py                 # Quiz generation, submission, results
│   ├── admin.py                 # Question bank admin
│   └── urls.py                  # Quiz URLs
│
├── progress/                    # Progress tracking
│   ├── views.py                 # User & course progress reports
│   └── urls.py                  # Progress URLs
│
├── certificates/                # Certificate generation
│   ├── models.py                # Certificate model with QR codes
│   ├── views.py                 # Certificate generation, verification
│   ├── admin.py                 # Certificate admin interface
│   └── urls.py                  # Certificate URLs
│
├── static/                      # Static files (CSS, JS, images)
│   ├── css/                     # SB Admin 2 CSS
│   ├── js/                      # SB Admin 2 JavaScript
│   └── vendor/                  # Third-party libraries (Bootstrap, jQuery)
│
├── media/                       # Uploaded files (created automatically)
│   ├── videos/                  # Video files
│   ├── subtitles/               # Subtitle files
│   └── certificates/            # Certificate PDFs & QR codes
│
└── templates/                   # HTML templates (to be created)
    ├── base.html                # Base template with SB Admin 2
    ├── accounts/
    ├── courses/
    ├── videos/
    ├── quizzes/
    └── certificates/
```

## 🔧 Django Admin Features

Access at http://localhost:8000/admin/

### User Management
- View all users (Admins, Risk Admins, Bankers)
- Change user roles and permissions
- Reset passwords
- Activate/deactivate accounts

### Course Management
- Create, edit, delete courses
- Set passing scores per course
- Assign videos to courses
- View enrollment statistics

### Video Management
- Upload videos with drag-and-drop
- Add multiple subtitle files per video
- View video processing status
- Monitor storage usage

### Question Bank
- Create questions with inline options
- Organize questions by topic
- Set difficulty levels and point values
- Preview question display

### Quiz Monitoring
- View all quiz attempts
- See detailed answer breakdowns
- Identify struggling students
- Track completion rates

### Certificate Administration
- View issued certificates
- Revoke certificates if needed
- Verify certificate authenticity
- Download certificate reports

## 🔐 Security Features

- **CSRF Protection** - All forms protected against cross-site attacks
- **SQL Injection Prevention** - Django ORM prevents SQL injection
- **Password Hashing** - Bcrypt password hashing with salt
- **JWT Authentication** - Secure API token authentication
- **Role-Based Access** - Permissions enforced at view and model level
- **File Upload Validation** - File type and size restrictions
- **XSS Protection** - Template auto-escaping prevents XSS attacks

## 🚀 Production Deployment

For production deployment:

1. **Set Environment Variables**
   ```env
   DEBUG=False
   SECRET_KEY=<generate-new-long-random-key>
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Use Production Database**
   - Use managed PostgreSQL (AWS RDS, Azure Database, etc.)
   - Enable SSL connections

3. **Set Up File Storage**
   - Use AWS S3 or Azure Blob Storage for media files
   - Install django-storages: `pip install django-storages boto3`

4. **Configure Web Server**
   - Use Gunicorn + Nginx
   - Enable HTTPS with Let's Encrypt
   - Set up static file caching

5. **Enable Background Tasks**
   ```powershell
   # Start Redis
   redis-server
   
   # Start Celery worker
   celery -A risk_lms worker -l info
   ```

6. **Set Up Monitoring**
   - Use Sentry for error tracking
   - Enable Django logging
   - Monitor database performance

See **[DJANGO_SETUP.md](DJANGO_SETUP.md)** for detailed production deployment guide.

## 🐛 Troubleshooting

### Database Connection Error
```powershell
# Check if PostgreSQL is running
Get-Service -Name postgresql*

# Test connection
psql -U risk_admin -d risk_lms -h localhost
```

### FFmpeg Not Found
```powershell
# Check FFmpeg installation
ffmpeg -version

# Add to PATH if needed (System Properties > Environment Variables)
```

### Static Files Not Loading
```powershell
# Recollect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT in settings.py
```

### Video Upload Fails
```powershell
# Check media folder permissions
# Verify VIDEO_MAX_SIZE in .env
# Check FFmpeg is in PATH
```

## 📚 Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **SB Admin 2 Template**: https://startbootstrap.com/theme/sb-admin-2
- **FFmpeg Documentation**: https://ffmpeg.org/documentation.html
- **ReportLab Guide**: https://www.reportlab.com/docs/reportlab-userguide.pdf

## 📞 Support

For issues or questions:
1. Check **[DJANGO_SETUP.md](DJANGO_SETUP.md)** for detailed instructions
2. Review troubleshooting section above
3. Check Django error logs in console
4. Review PostgreSQL logs

## 📝 License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

**Built with Django 4.2 | PostgreSQL | SB Admin 2 Template**
