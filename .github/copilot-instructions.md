# Risk Department Learning Management System - Django Project

## Project Overview
Comprehensive LMS for risk department training with:
- Video uploads with subtitle/translation support
- Mandatory viewing tracking (no skip, 95% completion required)
- Random question pools by topic
- 80% benchmark grading system
- Certificate generation with QR codes
- Role-based access (Admin, Risk Admin & Bankers)

## Setup Progress

- [x] Verify copilot-instructions.md created
- [x] Scaffold Django Project - All apps complete
- [x] Customize the Project - All features implemented
- [x] Create all Django models (User, Course, Video, Question, Certificate)
- [x] Create all views and URL routing
- [x] Create admin interfaces
- [ ] Install Python 3.9+ (REQUIRED FIRST)
- [ ] Create virtual environment
- [ ] Install Python dependencies (pip install -r requirements.txt)
- [ ] Install PostgreSQL database
- [ ] Install FFmpeg for video processing
- [ ] Configure environment variables (.env file)
- [ ] Run database migrations
- [ ] Create superuser account
- [ ] Copy SB Admin 2 template files
- [ ] Create Django templates
- [ ] Launch the Project (python manage.py runserver)

## Technology Stack
- Backend: Django 4.2, Django REST Framework, PostgreSQL
- Frontend: SB Admin 2 (Bootstrap), Django Templates
- Video: FFmpeg processing with moviepy
- Features: QR codes (qrcode), PDF certificates (reportlab), Progress tracking
- Async: Celery + Redis for background tasks

## Next Steps

See **DJANGO_SETUP.md** for detailed installation instructions.

### Quick Start:

1. **Install Python 3.9+**
   - Download from: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation
   - Verify: `python --version`

2. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/windows/
   - Create database: `CREATE DATABASE risk_lms;`

3. **Install FFmpeg**
   - Download from: https://ffmpeg.org/download.html
   - Add to PATH

4. **Set Up Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

5. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

6. **Configure Environment**
   - Create `.env` file in project root
   - Add database credentials and settings

7. **Run Migrations**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

8. **Copy SB Admin 2 Template**
   ```powershell
   # From: C:\Users\Paul\Desktop\startbootstrap-sb-admin-2-gh-pages
   # Copy css/, js/, vendor/ to static/ folder
   ```

9. **Start Development Server**
   ```powershell
   python manage.py runserver
   ```

10. **Access the Application**
    - Main site: http://localhost:8000/
    - Admin panel: http://localhost:8000/admin/
    - Login with superuser credentials
