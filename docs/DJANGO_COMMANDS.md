# Django Command Reference - Risk LMS

Quick reference for common Django management commands.

## 🚀 Initial Setup

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Then edit .env with your settings

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

## 📊 Database Commands

```powershell
# Create new migrations after model changes
python manage.py makemigrations

# Show migration SQL (without applying)
python manage.py sqlmigrate accounts 0001

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback to specific migration
python manage.py migrate accounts 0001

# Reset database (DANGEROUS - deletes all data)
python manage.py flush
```

## 👤 User Management

```powershell
# Create superuser (Admin)
python manage.py createsuperuser

# Change user password via shell
python manage.py shell
```

Then in Python shell:
```python
from accounts.models import User
user = User.objects.get(email='user@example.com')
user.set_password('new_password')
user.save()
exit()
```

To promote user to Risk Admin:
```python
from accounts.models import User
user = User.objects.get(email='user@example.com')
user.role = 'risk_admin'
user.save()
exit()
```

## 🖥️ Django Shell Commands

```powershell
# Open Django shell
python manage.py shell
```

Useful shell commands:
```python
# Import models
from accounts.models import User
from courses.models import Course, Enrollment
from videos.models import Video, VideoProgress
from quizzes.models import Question, QuizAttempt
from certificates.models import Certificate

# List all users
User.objects.all()

# Get specific user
user = User.objects.get(email='user@example.com')

# Create course
course = Course.objects.create(
    title='Risk Management 101',
    description='Introduction to risk management',
    passing_score=80
)

# Enroll user in course
enrollment = Enrollment.objects.create(user=user, course=course)

# Get user's enrollments
Enrollment.objects.filter(user=user)

# Get course enrollments
Enrollment.objects.filter(course=course)

# Count objects
User.objects.count()
Course.objects.count()
Video.objects.count()

# Filter by role
User.objects.filter(role='banker')
User.objects.filter(role='risk_admin')

# Get quiz attempts
QuizAttempt.objects.filter(user=user, passed=True)

# Get certificates
Certificate.objects.filter(user=user, is_valid=True)

# Exit shell
exit()
```

## 🧪 Testing Commands

```powershell
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test courses

# Run specific test class
python manage.py test accounts.tests.UserModelTests

# Run with verbosity
python manage.py test --verbosity=2

# Keep database after tests
python manage.py test --keepdb
```

## 📁 Static Files

```powershell
# Collect static files (for production)
python manage.py collectstatic

# Collect without prompts
python manage.py collectstatic --noinput

# Clear existing files first
python manage.py collectstatic --clear --noinput
```

## 🔍 Debugging Commands

```powershell
# Check for errors in project
python manage.py check

# Show detailed system check
python manage.py check --deploy

# Show installed apps
python manage.py showmigrations

# Validate models
python manage.py validate

# Show Django version
python -m django --version

# Show database router
python manage.py dbshell
```

## 📦 App Management

```powershell
# Create new app
python manage.py startapp app_name

# Then add to INSTALLED_APPS in settings.py
```

## 💾 Backup & Restore

```powershell
# Dump data to JSON (backup)
python manage.py dumpdata > backup.json

# Dump specific app
python manage.py dumpdata accounts > accounts_backup.json

# Load data from JSON (restore)
python manage.py loaddata backup.json

# Dump with indentation (readable)
python manage.py dumpdata --indent 2 > backup.json
```

## 🌐 Development Server

```powershell
# Start server (default: http://localhost:8000)
python manage.py runserver

# Start on different port
python manage.py runserver 8080

# Start on all interfaces
python manage.py runserver 0.0.0.0:8000

# Disable auto-reload
python manage.py runserver --noreload
```

## 🔐 Security Commands

```powershell
# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Check for security issues
python manage.py check --deploy
```

## 📧 Email Testing

```powershell
# Start email server (prints emails to console)
python -m smtpd -n -c DebuggingServer localhost:1025

# In another terminal, run Django with this setting in .env:
# EMAIL_HOST=localhost
# EMAIL_PORT=1025
```

## 🧹 Cleanup Commands

```powershell
# Clear sessions
python manage.py clearsessions

# Delete expired sessions
python manage.py clearsessions

# Clear cache
python manage.py clear_cache  # (if cache framework configured)
```

## 📊 Database Queries (via shell)

```powershell
python manage.py shell
```

```python
# Count users by role
from accounts.models import User
User.objects.filter(role='admin').count()
User.objects.filter(role='risk_admin').count()
User.objects.filter(role='banker').count()

# Get courses with enrollment count
from courses.models import Course
from django.db.models import Count
Course.objects.annotate(enrollment_count=Count('enrollments'))

# Get users who passed all quizzes
from quizzes.models import QuizAttempt
from accounts.models import User
users = User.objects.filter(
    quiz_attempts__passed=True
).distinct()

# Get average quiz score
from quizzes.models import QuizAttempt
QuizAttempt.objects.aggregate(Avg('score'))

# Get users eligible for certificates (80%+ average)
from django.db.models import Avg
QuizAttempt.objects.values('user').annotate(
    avg_score=Avg('score')
).filter(avg_score__gte=80)

# Delete all quiz attempts for a user
from quizzes.models import QuizAttempt
QuizAttempt.objects.filter(user=user).delete()
```

## 🎯 Custom Management Commands

Create in `app_name/management/commands/command_name.py`:

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of command'
    
    def handle(self, *args, **options):
        self.stdout.write('Command executed!')
```

Run with:
```powershell
python manage.py command_name
```

## 🔄 Celery Commands (Background Tasks)

```powershell
# Start Celery worker
celery -A risk_lms worker -l info

# Start Celery beat (scheduled tasks)
celery -A risk_lms beat -l info

# Start both worker and beat
celery -A risk_lms worker --beat -l info

# Purge all tasks
celery -A risk_lms purge

# Inspect active tasks
celery -A risk_lms inspect active

# Show registered tasks
celery -A risk_lms inspect registered
```

## 🐛 Common Troubleshooting

### Virtual environment not activating
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module not found error
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Database connection error
```powershell
# Check PostgreSQL is running
Get-Service -Name postgresql*

# Test connection
psql -U risk_admin -d risk_lms
```

### Migrations not applying
```powershell
# Show what's pending
python manage.py showmigrations

# Delete migration files and start fresh (CAREFUL!)
python manage.py migrate --fake accounts zero
# Then delete migration files manually
python manage.py makemigrations
python manage.py migrate
```

### Static files not loading
```powershell
python manage.py collectstatic --clear --noinput
# Check STATIC_URL and STATIC_ROOT in settings.py
```

## 📚 Quick References

### Access Points
- **Main site**: http://localhost:8000/
- **Admin panel**: http://localhost:8000/admin/
- **API root**: http://localhost:8000/api/

### Important Files
- **Settings**: `risk_lms/settings.py`
- **URLs**: `risk_lms/urls.py`
- **Environment**: `.env`
- **Dependencies**: `requirements.txt`

### Logs Location
- Console output (development)
- `logs/` folder (if configured)
- PostgreSQL logs: `C:\Program Files\PostgreSQL\<version>\data\log\`

---

## 💡 Pro Tips

1. **Always activate virtual environment first**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **After model changes, always run:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Check for errors before running:**
   ```powershell
   python manage.py check
   ```

4. **Use shell for quick testing:**
   ```powershell
   python manage.py shell
   ```

5. **Keep .env file secret** - Never commit to Git

6. **Backup before major changes:**
   ```powershell
   python manage.py dumpdata > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").json
   ```

---

**For detailed setup, see DJANGO_SETUP.md**
