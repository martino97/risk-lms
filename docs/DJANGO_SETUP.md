# Risk Department Learning Management System - Django Setup Guide

## Prerequisites
Before you begin, ensure you have the following installed:

1. **Python 3.9 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify installation: `python --version`

2. **PostgreSQL 13 or higher**
   - Download from: https://www.postgresql.org/download/windows/
   - Remember the password you set during installation
   - Verify installation: `psql --version`

3. **FFmpeg** (for video processing)
   - Download from: https://ffmpeg.org/download.html#build-windows
   - Extract to a folder (e.g., C:\ffmpeg)
   - Add to PATH: System Properties > Environment Variables > System Variables > Path > New > C:\ffmpeg\bin

4. **Redis** (for Celery task queue - optional for initial setup)
   - Download from: https://github.com/microsoftarchive/redis/releases
   - Or use Windows Subsystem for Linux (WSL)

## Step 1: Create PostgreSQL Database

Open PostgreSQL command line (psql) or pgAdmin:

```sql
-- Create database
CREATE DATABASE risk_lms;

-- Create user (optional, can use postgres user)
CREATE USER risk_admin WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE risk_lms TO risk_admin;
```

## Step 2: Set Up Virtual Environment

Open PowerShell in your project directory:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 3: Install Dependencies

```powershell
# Install all required packages
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-long-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=risk_lms
DB_USER=risk_admin
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Media Files
MEDIA_ROOT=media/
MEDIA_URL=/media/

# FFmpeg Path (if not in PATH)
FFMPEG_PATH=C:/ffmpeg/bin/ffmpeg.exe

# Email Configuration (for notifications - optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Configuration (for Celery)
REDIS_URL=redis://localhost:6379/0

# Domain (for certificate verification URLs)
DOMAIN=http://localhost:8000
```

## Step 5: Run Database Migrations

```powershell
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Create Superuser

```powershell
# Create admin account
python manage.py createsuperuser

# Follow the prompts:
# - Email: admin@example.com
# - First Name: Admin
# - Last Name: User
# - Password: (enter secure password)
# - Role: admin
```

## Step 7: Integrate SB Admin 2 Template

Copy the SB Admin 2 template files to your project:

```powershell
# Create necessary directories
New-Item -ItemType Directory -Force -Path "static/css"
New-Item -ItemType Directory -Force -Path "static/js"
New-Item -ItemType Directory -Force -Path "static/vendor"
New-Item -ItemType Directory -Force -Path "templates"

# Copy files from your Desktop template
# From: C:\Users\Paul\Desktop\startbootstrap-sb-admin-2-gh-pages

# Copy CSS files
Copy-Item "C:\Users\Paul\Desktop\startbootstrap-sb-admin-2-gh-pages\css\*" -Destination "static/css/" -Recurse

# Copy JS files
Copy-Item "C:\Users\Paul\Desktop\startbootstrap-sb-admin-2-gh-pages\js\*" -Destination "static/js/" -Recurse

# Copy vendor files (Bootstrap, jQuery, etc.)
Copy-Item "C:\Users\Paul\Desktop\startbootstrap-sb-admin-2-gh-pages\vendor\*" -Destination "static/vendor/" -Recurse
```

## Step 8: Collect Static Files

```powershell
# Collect all static files
python manage.py collectstatic --noinput
```

## Step 9: Run Development Server

```powershell
# Start Django development server
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

## Step 10: Access the Application

### Admin Interface
- URL: http://localhost:8000/admin/
- Login with the superuser credentials you created

### Main Application
- URL: http://localhost:8000/
- Register a new user or use the superuser account

## Default User Roles

The system has three user roles:

1. **Admin** - Full system access
2. **Risk Admin** - Can create courses, upload videos, manage questions
3. **Banker** - Can enroll in courses, watch videos, take quizzes

### Promoting User to Risk Admin

After registration, you can promote a user to Risk Admin via:

**Option 1: Django Admin**
1. Go to http://localhost:8000/admin/accounts/user/
2. Click on the user
3. Change "Role" to "risk_admin"
4. Save

**Option 2: Django Shell**
```powershell
python manage.py shell
```
```python
from accounts.models import User
user = User.objects.get(email='user@example.com')
user.role = 'risk_admin'
user.save()
```

## Running Background Tasks (Optional)

For video processing and other async tasks:

### Terminal 1: Start Redis
```powershell
redis-server
```

### Terminal 2: Start Celery Worker
```powershell
celery -A risk_lms worker -l info
```

### Terminal 3: Django Server
```powershell
python manage.py runserver
```

## Common Issues & Solutions

### Issue 1: Database Connection Error
**Solution:** Check PostgreSQL is running and credentials in `.env` are correct
```powershell
# Check if PostgreSQL is running
Get-Service -Name postgresql*
```

### Issue 2: Static Files Not Loading
**Solution:** Run collectstatic and check STATIC_URL in settings
```powershell
python manage.py collectstatic --noinput
```

### Issue 3: Video Upload Fails
**Solution:** Check MEDIA_ROOT permissions and FFmpeg installation
```powershell
# Test FFmpeg
ffmpeg -version
```

### Issue 4: Module Not Found Error
**Solution:** Ensure virtual environment is activated
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Project Structure

```
risk_lms/
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── risk_lms/              # Main project settings
│   ├── settings.py        # Django settings
│   └── urls.py            # URL routing
├── accounts/              # User authentication
├── courses/               # Course management
├── videos/                # Video upload & playback
├── quizzes/               # Quiz & questions
├── progress/              # Progress tracking
├── certificates/          # Certificate generation
├── static/                # Static files (CSS, JS)
├── media/                 # Uploaded files
└── templates/             # HTML templates

```

## Next Steps After Installation

1. **Login to Admin Panel**
   - Create courses at http://localhost:8000/admin/courses/course/

2. **Upload Videos**
   - Add videos to courses with optional subtitles

3. **Create Questions**
   - Add questions to the question bank for each course

4. **Test User Flow**
   - Register as a banker
   - Enroll in a course
   - Watch videos (mandatory viewing)
   - Take quiz (random questions from pool)
   - Complete all courses
   - Generate certificate (80% average required)

## Support & Documentation

- Django Documentation: https://docs.djangoproject.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- SB Admin 2 Template: https://startbootstrap.com/theme/sb-admin-2

## Security Notes

🔒 **For Production Deployment:**
1. Change `DEBUG=False` in `.env`
2. Generate new `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your domain
4. Use HTTPS
5. Set up proper email backend
6. Use environment-specific database credentials
7. Enable CORS properly for API access
8. Set up proper file storage (AWS S3, etc.)
