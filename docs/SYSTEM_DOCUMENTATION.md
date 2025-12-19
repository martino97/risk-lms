# Risk Department Learning Management System (LMS)

## Co-operative Bank of Tanzania PLC
### Risk Management & Compliance Training Platform

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Overview](#2-system-overview)
3. [Technology Stack](#3-technology-stack)
4. [User Roles & Permissions](#4-user-roles--permissions)
5. [System Architecture](#5-system-architecture)
6. [Core Modules](#6-core-modules)
7. [Authentication System](#7-authentication-system)
8. [Course Management](#8-course-management)
9. [Video & Interactive Content](#9-video--interactive-content)
10. [Quiz & Assessment System](#10-quiz--assessment-system)
11. [Certificate Generation](#11-certificate-generation)
12. [Database Schema](#12-database-schema)
13. [API Reference](#13-api-reference)
14. [Installation & Deployment](#14-installation--deployment)
15. [Administration Guide](#15-administration-guide)
16. [User Guide](#16-user-guide)
17. [Security Considerations](#17-security-considerations)
18. [Troubleshooting](#18-troubleshooting)
19. [Appendices](#19-appendices)

---

## 1. Executive Summary

### 1.1 Purpose
The Risk Department Learning Management System (Risk LMS) is a comprehensive web-based training platform designed specifically for Co-operative Bank of Tanzania PLC. The system enables the Risk Management & Compliance department to deliver mandatory training courses to all bank staff (bankers), track their progress, assess their knowledge through quizzes, and issue verifiable certificates upon successful completion.

### 1.2 Key Objectives
- **Centralized Training Management**: Single platform for all risk and compliance training materials
- **Mandatory Viewing Enforcement**: Ensures staff watch 95% of video content without skipping
- **Knowledge Assessment**: Random question pools with 80% pass benchmark
- **Compliance Tracking**: Real-time monitoring of training completion rates
- **Verifiable Certification**: QR-coded certificates for authenticity verification
- **Active Directory Integration**: Seamless authentication with bank's domain credentials

### 1.3 Target Users
- **Head of Risk**: Full administrative access to manage courses, users, and view analytics
- **Risk & Compliance Specialist**: Course creation, content management, and user monitoring
- **Bankers**: Training participants who complete courses and earn certificates

---

## 2. System Overview

### 2.1 System Description
The Risk LMS is built on Django 4.2+, a robust Python web framework, with Microsoft SQL Server as the production database. The system features a modern, responsive interface based on SB Admin 2 Bootstrap template.

### 2.2 Key Features

| Feature | Description |
|---------|-------------|
| **Multi-format Content** | Support for video courses, interactive SCORM/Captivate packages, and HTML5 content |
| **Progress Tracking** | Real-time tracking of user progress with mandatory viewing requirements |
| **Random Quiz Generation** | Questions randomly selected from topic-based question pools |
| **Certificate Generation** | Automated PDF certificates with QR codes for verification |
| **Active Directory Auth** | Single Sign-On with bank's KCBLTZ domain |
| **Role-Based Access** | Four-tier permission system for different user types |
| **Analytics Dashboard** | Comprehensive reporting on training compliance |
| **Deadline Management** | Configurable course completion time limits |

### 2.3 System Requirements

#### Server Requirements
- Python 3.9 or higher
- Microsoft SQL Server 2016+ (Express, Standard, or Enterprise)
- ODBC Driver 17 for SQL Server
- Windows Server 2016+ or Windows 10/11 (for development)

#### Client Requirements
- Modern web browser (Chrome, Firefox, Edge, Safari)
- JavaScript enabled
- Minimum screen resolution: 1280x720

---

## 3. Technology Stack

### 3.1 Backend Technologies

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Django | 4.2.x |
| Language | Python | 3.9+ |
| Database | Microsoft SQL Server | 2016+ |
| Database Driver | mssql-django, pyodbc | Latest |
| Task Queue | Celery | 5.3+ |
| Message Broker | Redis | 5.0+ |
| WSGI Server | Gunicorn/Waitress | Latest |

### 3.2 Frontend Technologies

| Component | Technology |
|-----------|------------|
| CSS Framework | Bootstrap 4 (SB Admin 2) |
| JavaScript | jQuery 3.x |
| Charts | Chart.js |
| Icons | Font Awesome 5 |
| DataTables | jQuery DataTables |

### 3.3 Additional Libraries

| Library | Purpose |
|---------|---------|
| `ldap3` | Active Directory authentication |
| `reportlab` | PDF certificate generation |
| `qrcode` | QR code generation for certificates |
| `Pillow` | Image processing |
| `moviepy` | Video duration calculation |
| `openpyxl` | Excel report generation |

---

## 4. User Roles & Permissions

### 4.1 Role Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                         ADMIN                                │
│  (Full System Access - Superuser)                           │
├─────────────────────────────────────────────────────────────┤
│                    HEAD OF RISK                              │
│  (Course Management, User Management, Analytics)            │
├─────────────────────────────────────────────────────────────┤
│            RISK & COMPLIANCE SPECIALIST                      │
│  (Course Management, Content Upload, User Monitoring)       │
├─────────────────────────────────────────────────────────────┤
│                        BANKER                                │
│  (View Courses, Take Quizzes, Earn Certificates)            │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Permission Matrix

| Permission | Admin | Head of Risk | R&C Specialist | Banker |
|------------|:-----:|:------------:|:--------------:|:------:|
| Access Admin Panel | ✅ | ✅ | ✅ | ❌ |
| Create Courses | ✅ | ✅ | ✅ | ❌ |
| Upload Videos | ✅ | ✅ | ✅ | ❌ |
| Add Questions | ✅ | ✅ | ✅ | ❌ |
| Delete Courses | ✅ | ✅ | ✅ | ❌ |
| Manage Users | ✅ | ✅ | ✅ | ❌ |
| View Analytics | ✅ | ✅ | ✅ | ❌ |
| Export Reports | ✅ | ✅ | ✅ | ❌ |
| Enroll in Courses | ✅ | ✅ | ✅ | ✅ |
| Take Quizzes | ✅ | ✅ | ✅ | ✅ |
| View Own Progress | ✅ | ✅ | ✅ | ✅ |
| Download Certificates | ✅ | ✅ | ✅ | ✅ |

### 4.3 Role Definitions

#### Admin
- Full superuser access to all system functions
- Can access Django admin panel
- Can modify system settings
- Can manage all user accounts

#### Head of Risk
- Primary administrator for training content
- Full access to course management
- Can view all user progress and analytics
- Can generate compliance reports
- Can manage banker accounts

#### Risk & Compliance Specialist
- Content creator and manager
- Can upload courses, videos, and questions
- Can monitor user progress
- Can generate reports
- Limited user management capabilities

#### Banker
- Training participant
- Can view and enroll in published courses
- Must complete all video content (95% minimum)
- Takes quizzes to earn certificates
- Can view own progress and certificates

---

## 5. System Architecture

### 5.1 Application Structure

```
risk_lms/
├── risk_lms/              # Main Django project
│   ├── settings.py        # Configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI entry point
│
├── accounts/              # User management module
│   ├── models.py          # User model with roles
│   ├── views.py           # Login, logout, profile
│   ├── ldap_backend.py    # AD authentication
│   └── forms.py           # User forms
│
├── courses/               # Course management
│   ├── models.py          # Course, Enrollment
│   ├── views.py           # Course views
│   └── urls.py            # Course URLs
│
├── videos/                # Video & interactive content
│   ├── models.py          # Video, InteractiveCourse
│   ├── views.py           # Video player, progress
│   └── urls.py            # Video URLs
│
├── quizzes/               # Assessment system
│   ├── models.py          # Question, QuizAttempt
│   ├── views.py           # Quiz logic
│   └── urls.py            # Quiz URLs
│
├── certificates/          # Certificate generation
│   ├── models.py          # Certificate model
│   ├── views.py           # PDF generation
│   └── urls.py            # Certificate URLs
│
├── content_management/    # Admin content tools
│   ├── views.py           # Upload, manage content
│   └── urls.py            # Content URLs
│
├── templates/             # HTML templates
├── static/                # CSS, JS, images
└── media/                 # Uploaded files
```

### 5.2 Database Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     users       │────<│   enrollments   │>────│    courses      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                                               │
        │                                               │
        ▼                                               ▼
┌─────────────────┐                            ┌─────────────────┐
│ quiz_attempts   │                            │     videos      │
└─────────────────┘                            └─────────────────┘
        │                                               │
        ▼                                               ▼
┌─────────────────┐                            ┌─────────────────┐
│  quiz_answers   │                            │ video_progress  │
└─────────────────┘                            └─────────────────┘
        │
        ▼
┌─────────────────┐     ┌─────────────────┐
│   questions     │────<│question_options │
└─────────────────┘     └─────────────────┘
        │
        ▼
┌─────────────────┐
│  certificates   │
└─────────────────┘
```

---

## 6. Core Modules

### 6.1 Accounts Module (`accounts/`)

**Purpose**: User authentication, authorization, and profile management.

**Key Components**:
- Custom User model with role-based permissions
- Active Directory/LDAP authentication backend
- Local password authentication fallback
- User profile management

**Model: User**
```python
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('head_of_risk', 'Head of Risk'),
        ('risk_compliance_specialist', 'Risk & Compliance Specialist'),
        ('banker', 'Banker'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
```

### 6.2 Courses Module (`courses/`)

**Purpose**: Course creation, management, and enrollment tracking.

**Key Components**:
- Course creation and editing
- Enrollment management
- Progress tracking
- Deadline management

**Model: Course**
```python
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, ...)
    is_published = models.BooleanField(default=False)
    passing_score = models.IntegerField(default=80)
    completion_time_enabled = models.BooleanField(default=False)
    completion_time_limit = models.IntegerField(default=0)  # days
```

### 6.3 Videos Module (`videos/`)

**Purpose**: Video content and interactive course management.

**Key Components**:
- Video upload and storage
- Interactive course (SCORM/Captivate) support
- Video progress tracking
- Mandatory viewing enforcement

**Model: InteractiveCourse**
```python
class InteractiveCourse(models.Model):
    CONTENT_TYPES = [
        ('captivate', 'Adobe Captivate'),
        ('scorm', 'SCORM Package'),
        ('html5', 'HTML5 Course'),
        ('articulate', 'Articulate Storyline'),
    ]
    
    course = models.ForeignKey(Course, ...)
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    package_file = models.FileField(upload_to='interactive_courses/packages/')
```

### 6.4 Quizzes Module (`quizzes/`)

**Purpose**: Question bank management and quiz assessment.

**Key Components**:
- Question bank with multiple types
- Random question selection
- Quiz attempt tracking
- Answer validation

**Question Types**:
- Multiple Choice (single answer)
- True/False
- Multiple Answer (multiple correct)

### 6.5 Certificates Module (`certificates/`)

**Purpose**: Certificate generation and verification.

**Key Components**:
- PDF certificate generation
- QR code generation
- Certificate verification
- Certificate history

---

## 7. Authentication System

### 7.1 Active Directory Integration

The system integrates with Co-operative Bank's Active Directory domain for Single Sign-On authentication.

**Domain Configuration**:
```python
LDAP_CONFIG = {
    'DOMAIN': 'KCBLTZ.CRDBBANKPLC.COM',
    'SERVERS': [
        '192.168.10.50',  # Primary DNS
        '192.168.10.10',  # Alternate DNS
    ],
    'BASE_DN': 'DC=KCBLTZ,DC=CRDBBANKPLC,DC=COM',
    'PORT': 389,
    'USE_SSL': False,
}
```

### 7.2 Authentication Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  User Login  │────>│ LDAP Backend │────>│Active Directory│
│   (Username) │     │  Authenticate│     │    Server     │
└──────────────┘     └──────────────┘     └──────────────┘
        │                   │
        │                   ▼
        │           ┌──────────────┐
        │           │ User Exists? │
        │           └──────────────┘
        │                   │
        │         ┌─────────┴─────────┐
        │         │                   │
        ▼         ▼                   ▼
┌──────────────┐  ┌──────────────┐   ┌──────────────┐
│ Local Auth   │  │ Update User  │   │ Create User  │
│  (Fallback)  │  │   Details    │   │   from AD    │
└──────────────┘  └──────────────┘   └──────────────┘
```

### 7.3 Dual Authentication Support

Users can authenticate using:
1. **Domain Credentials**: Primary method using AD username/password
2. **Local Credentials**: Fallback for testing or when AD is unavailable

**Example Login**:
- Username: `JMURO` (case-insensitive)
- Password: Domain password OR local password `Test123!`

---

## 8. Course Management

### 8.1 Creating a Course

**Step-by-step process**:
1. Navigate to Content Dashboard
2. Click "Create New Course"
3. Enter course details:
   - Title
   - Description
   - Passing Score (default: 80%)
   - Thumbnail image (optional)
4. Set completion time limit (optional)
5. Save and proceed to content upload

### 8.2 Course Structure

```
Course
├── Course Details (Title, Description, Thumbnail)
├── Settings (Passing Score, Time Limit)
├── Videos (Multiple, ordered)
├── Interactive Courses (SCORM/Captivate packages)
├── Questions (Random pool by topic)
└── Enrollments (User progress tracking)
```

### 8.3 Publishing Workflow

```
Draft ──> Add Content ──> Add Questions ──> Review ──> Publish
                              │
                              ▼
                    Minimum 5 questions required
```

---

## 9. Video & Interactive Content

### 9.1 Supported Video Formats
- MP4
- WebM
- AVI
- MOV

### 9.2 Interactive Course Packages

**Supported Types**:
| Type | Description |
|------|-------------|
| Adobe Captivate | `.cptx` packages exported as HTML5 |
| SCORM 1.2/2004 | Standard eLearning packages |
| Articulate Storyline | Published HTML5 output |
| HTML5 | Custom HTML5 courses |

### 9.3 Progress Tracking

**Video Progress**:
- Tracks watched duration
- Records last position for resume
- Requires 95% completion
- No skipping allowed

**Interactive Course Progress**:
- Slide-by-slide tracking
- SCORM data persistence
- Completion percentage calculation
- Resume capability

---

## 10. Quiz & Assessment System

### 10.1 Question Types

**Multiple Choice**
- Single correct answer
- 4 options typically
- Points awarded for correct answer

**True/False**
- Boolean answer
- Quick knowledge check

**Multiple Answer**
- Multiple correct options
- All correct must be selected

### 10.2 Quiz Generation

```python
# Questions randomly selected by topic
# Example: 10 questions from pool of 50
questions = Question.objects.filter(
    course=course
).order_by('?')[:num_questions]
```

### 10.3 Grading System

- **Pass Mark**: 80% (configurable per course)
- **Scoring**: Points-based (default 1 point per question)
- **Multiple Attempts**: Allowed, best score recorded
- **Time Limit**: None (optional feature)

### 10.4 Quiz Flow

```
Prerequisites Check ──> Generate Questions ──> Present Quiz
        │                                           │
        ▼                                           ▼
Must complete 95%                            Answer Questions
of video content                                    │
                                                    ▼
                                          Calculate Score ──> Pass/Fail
                                                    │
                                        ┌───────────┴───────────┐
                                        ▼                       ▼
                                    Generate                 Retry
                                   Certificate              Option
```

---

## 11. Certificate Generation

### 11.1 Certificate Components

**PDF Certificate Includes**:
- Bank logo and branding
- Recipient's full name
- Course title
- Completion date
- Final score
- Unique certificate number
- QR code for verification
- Authorized signatures

### 11.2 QR Code Data

The QR code contains comprehensive verification information:

```
🏆 CERTIFICATE OF COMPLETION 🏆

📜 Certificate #: CERT-2025-001234
👤 Full Name: Jackline Muro
📧 Email: jmuro@cbtbank.co.tz
📚 Course: Risk Management Fundamentals
📊 Final Score: 85.0%
📅 Completed: December 19, 2025
🏦 Issuing Bank: Co-operative Bank of Tanzania PLC
✅ Status: VALID & AUTHENTIC
```

### 11.3 Certificate Verification

**Verification Methods**:
1. **QR Code Scan**: Instant verification via mobile device
2. **Online Verification**: URL-based verification page
3. **Certificate Number**: Manual lookup in system

---

## 12. Database Schema

### 12.1 Core Tables

| Table | Description |
|-------|-------------|
| `users` | User accounts and profiles |
| `courses` | Course definitions |
| `enrollments` | User-course enrollment records |
| `videos` | Video content metadata |
| `video_progress` | User video watching progress |
| `interactive_courses` | SCORM/Captivate packages |
| `interactive_course_progress` | Interactive content progress |
| `questions` | Question bank |
| `question_options` | Answer options for questions |
| `quiz_attempts` | Quiz attempt records |
| `quiz_answers` | Individual question answers |
| `certificates` | Issued certificates |

### 12.2 Entity Relationship Diagram

```
users (1) ──────< (M) enrollments (M) >────── (1) courses
  │                                               │
  │                                               │
  └──< quiz_attempts >── questions ──< question_options
  │         │                │
  │         │                └──────────────────────┐
  │         └──< quiz_answers                       │
  │                                                 │
  └──< certificates >──────────────────────────────┘
```

---

## 13. API Reference

### 13.1 Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts/login/` | GET, POST | User login page |
| `/accounts/logout/` | GET | User logout |
| `/accounts/profile/` | GET | User profile |

### 13.2 Course Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/courses/` | GET | List all courses |
| `/courses/<id>/` | GET | Course detail |
| `/courses/<id>/enroll/` | POST | Enroll in course |
| `/courses/my-courses/` | GET | User's enrolled courses |

### 13.3 Quiz Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/quiz/<course_id>/start/` | POST | Start quiz |
| `/quiz/<attempt_id>/` | GET | Quiz questions |
| `/quiz/<attempt_id>/submit/` | POST | Submit answer |
| `/quiz/<attempt_id>/complete/` | POST | Complete quiz |

### 13.4 Content Management Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/content/` | GET | Content dashboard |
| `/content/course/create/` | POST | Create course |
| `/content/video/upload/` | POST | Upload video |
| `/content/questions/add/` | POST | Add questions |

---

## 14. Installation & Deployment

### 14.1 Prerequisites

```bash
# Required software
- Python 3.9+
- Microsoft SQL Server 2016+
- ODBC Driver 17 for SQL Server
- Git
```

### 14.2 Installation Steps

```powershell
# 1. Clone or extract project
cd "C:\path\to\project"

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
$env:DB_ENGINE = "mssql"
$env:DB_NAME = "risk_lms"
$env:DB_HOST = "ServerName\SQLEXPRESS"

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic

# 8. Run server
python manage.py runserver 0.0.0.0:8000
```

### 14.3 Production Deployment

**IIS Deployment**:
```powershell
# Install wfastcgi
pip install wfastcgi
wfastcgi-enable
```

**Environment Variables for Production**:
```
DEBUG=False
SECRET_KEY=<your-secure-secret-key>
ALLOWED_HOSTS=your-domain.com
DB_ENGINE=mssql
DB_HOST=production-server\instance
DB_NAME=risk_lms_prod
```

---

## 15. Administration Guide

### 15.1 User Management

**Creating Users**:
1. Users are auto-created on first AD login
2. Manual creation via Django Admin
3. Bulk import via management command

**Assigning Roles**:
```python
# Via Django shell
python manage.py shell
>>> from accounts.models import User
>>> user = User.objects.get(username='JMURO')
>>> user.role = 'head_of_risk'
>>> user.is_staff = True
>>> user.save()
```

### 15.2 Course Administration

**Course Lifecycle**:
1. Create course (Draft status)
2. Upload content (Videos, Interactive)
3. Add questions (Minimum 5)
4. Review and test
5. Publish course
6. Monitor enrollments
7. Archive when complete

### 15.3 Reporting

**Available Reports**:
- User Progress Report
- Course Completion Report
- Quiz Performance Report
- Certificate Issuance Report
- Compliance Summary Report

---

## 16. User Guide

### 16.1 For Bankers (Training Participants)

**Logging In**:
1. Navigate to http://localhost:8000/
2. Enter your domain username (e.g., `JMURO`)
3. Enter your domain password
4. Click "Sign In"

**Taking a Course**:
1. View available courses on dashboard
2. Click "Enroll" on desired course
3. Watch all videos (95% minimum)
4. Complete interactive content
5. Take the quiz (80% pass required)
6. Download your certificate

**Viewing Certificates**:
1. Go to "My Certificates"
2. Click "Download PDF"
3. Share certificate via QR code

### 16.2 For Administrators

**Creating Content**:
1. Login with admin credentials
2. Navigate to Content Dashboard
3. Create new course
4. Upload videos/interactive content
5. Add quiz questions
6. Publish course

**Monitoring Progress**:
1. View Analytics Dashboard
2. Check completion rates
3. Identify non-compliant users
4. Generate reports

---

## 17. Security Considerations

### 17.1 Authentication Security

- **LDAP/AD Integration**: Enterprise-grade authentication
- **Password Hashing**: Django's PBKDF2 algorithm
- **Session Security**: Secure session cookies
- **CSRF Protection**: Built-in CSRF tokens

### 17.2 Authorization Controls

- **Role-Based Access**: Four-tier permission system
- **View Decorators**: `@login_required` protection
- **Permission Checks**: `can_upload_content()` methods
- **Admin Panel**: Staff-only access

### 17.3 Data Protection

- **SQL Injection**: Django ORM parameterized queries
- **XSS Prevention**: Template auto-escaping
- **File Upload**: Validated file types
- **Sensitive Data**: Encrypted storage recommended

### 17.4 Production Recommendations

```python
# settings.py for production
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use env variable
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

---

## 18. Troubleshooting

### 18.1 Common Issues

**Issue: Cannot connect to database**
```
Solution: Verify SQL Server is running and environment variables are set
$env:DB_HOST = "ServerName\SQLEXPRESS"
```

**Issue: LDAP authentication fails**
```
Solution: 
1. Check network connectivity to AD servers
2. Verify domain credentials
3. Check LDAP port (389) is open
```

**Issue: Video won't play**
```
Solution:
1. Check file format (MP4/WebM supported)
2. Verify file uploaded completely
3. Check browser console for errors
```

**Issue: Certificate generation fails**
```
Solution:
1. Ensure reportlab and Pillow are installed
2. Check media/certificates/ directory permissions
3. Verify all required user fields are populated
```

### 18.2 Log Locations

```
Django Logs: Console output (DEBUG=True)
Application Logs: ./logs/risk_lms.log (if configured)
SQL Server Logs: SQL Server Management Studio
```

---

## 19. Appendices

### Appendix A: Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_ENGINE` | Database engine | `mssql` |
| `DB_NAME` | Database name | `risk_lms` |
| `DB_HOST` | Database server | `localhost\SQLEXPRESS` |
| `DB_USER` | Database user | (Windows Auth) |
| `DB_PASSWORD` | Database password | (Windows Auth) |
| `DEBUG` | Debug mode | `True` |
| `SECRET_KEY` | Django secret key | (Change in production) |

### Appendix B: Default Credentials

**Admin User (Example)**:
- Username: `MMalopa`
- Email: `martin.malopa@cbtbank.co.tz`
- Role: Admin

**Head of Risk (Example)**:
- Username: `JMURO`
- Email: `jmuro@cbtbank.co.tz`
- Password: `Test123!`
- Role: Head of Risk

### Appendix C: File Structure

```
C:\Users\Paul\New folder\
├── manage.py
├── requirements.txt
├── db.sqlite3 (development)
├── risk_lms/
├── accounts/
├── courses/
├── videos/
├── quizzes/
├── certificates/
├── content_management/
├── templates/
├── static/
└── media/
    ├── certificates/
    ├── course_thumbnails/
    ├── interactive_courses/
    └── videos/
```

### Appendix D: Quick Reference Commands

```powershell
# Start server
$env:DB_ENGINE = "mssql"
$env:DB_HOST = "Martin\SQLEXPRESS"
python manage.py runserver 0.0.0.0:8000

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Django shell
python manage.py shell
```

---

## Document Information

| Field | Value |
|-------|-------|
| **Document Title** | Risk LMS System Documentation |
| **Version** | 1.0 |
| **Last Updated** | December 19, 2025 |
| **Organization** | Co-operative Bank of Tanzania PLC |
| **Department** | Risk Management & Compliance |
| **Author** | System Development Team |
| **Classification** | Internal Use |

---

*© 2025 Co-operative Bank of Tanzania PLC. All rights reserved.*
