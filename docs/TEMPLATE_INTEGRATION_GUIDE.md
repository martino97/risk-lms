# SB Admin 2 Template Integration Guide

## ✅ Template Files Successfully Copied!

The SB Admin 2 template has been integrated into your Django project. Here's what was done:

### 📁 Files Copied

**From:** `C:\Users\Paul\Desktop\startbootstrap-sb-admin-2-gh-pages\startbootstrap-sb-admin-2-gh-pages`

**To:** `C:\Users\Paul\New folder\static\`

**Directories created and populated:**
- ✅ `static/css/` - SB Admin 2 stylesheets
- ✅ `static/js/` - Custom JavaScript files
- ✅ `static/img/` - Template images
- ✅ `static/vendor/` - Third-party libraries:
  - Bootstrap 4
  - jQuery
  - Font Awesome icons
  - Chart.js
  - DataTables
  - jQuery Easing

### 🎨 Base Template Created

**File:** `templates/base.html`

This is your main layout template that includes:
- ✅ Responsive sidebar navigation
- ✅ Top navigation bar with user dropdown
- ✅ Role-based menu items (different for Risk Admin vs Banker)
- ✅ Footer
- ✅ Logout modal
- ✅ All CSS/JS imports

**Features:**
- Sidebar shows different options for Risk Admins (Videos, Questions, Admin Panel)
- Dashboard link for all users
- My Progress and Certificates sections
- User profile dropdown in top-right corner

### 📄 Login Template Created

**File:** `templates/accounts/login.html`

A beautiful login page with:
- ✅ Centered login card
- ✅ Email and password fields
- ✅ "Remember Me" checkbox
- ✅ Link to registration page
- ✅ Django messages support for errors/success

## 🎯 How to Use the Templates

### 1. In Your Django Views

All your views need to render these templates. Example:

```python
# courses/views.py
from django.shortcuts import render

def dashboard_view(request):
    context = {
        # Your data here
    }
    return render(request, 'courses/dashboard.html', context)
```

### 2. Create Child Templates

Create templates that extend `base.html`. Example for dashboard:

**File:** `templates/courses/dashboard.html`

```django
{% extends 'base.html' %}

{% block title %}Dashboard - Risk LMS{% endblock %}

{% block nav_dashboard %}active{% endblock %}

{% block page_heading %}
<h1 class="h3 mb-0 text-gray-800">Dashboard</h1>
{% endblock %}

{% block content %}
<div class="row">
    <!-- Your dashboard content here -->
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                            Enrolled Courses</div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ enrolled_courses_count }}</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-book fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 3. Template Blocks Available

Use these blocks in your child templates:

- `{% block title %}` - Page title (shown in browser tab)
- `{% block extra_css %}` - Add custom CSS for specific pages
- `{% block nav_dashboard %}` - Add "active" class to Dashboard menu
- `{% block nav_courses %}` - Add "active" class to Courses menu
- `{% block nav_videos %}` - Add "active" class to Videos menu
- `{% block nav_questions %}` - Add "active" class to Questions menu
- `{% block nav_progress %}` - Add "active" class to Progress menu
- `{% block nav_certificates %}` - Add "active" class to Certificates menu
- `{% block page_heading %}` - Page title/heading
- `{% block content %}` - Main page content
- `{% block extra_js %}` - Add custom JavaScript for specific pages

## 📝 Templates You Need to Create

Create these template files to complete your application:

### Accounts Templates
```
templates/accounts/
├── login.html          ✅ CREATED
├── register.html       ⏳ TO CREATE
└── profile.html        ⏳ TO CREATE
```

### Courses Templates
```
templates/courses/
├── dashboard.html      ⏳ TO CREATE
├── course_list.html    ⏳ TO CREATE
└── course_detail.html  ⏳ TO CREATE
```

### Videos Templates
```
templates/videos/
└── video_player.html   ⏳ TO CREATE
```

### Quizzes Templates
```
templates/quizzes/
├── take_quiz.html      ⏳ TO CREATE
└── quiz_results.html   ⏳ TO CREATE
```

### Progress Templates
```
templates/progress/
├── user_progress.html  ⏳ TO CREATE
└── course_progress.html ⏳ TO CREATE
```

### Certificates Templates
```
templates/certificates/
├── my_certificates.html    ⏳ TO CREATE
├── certificate_detail.html ⏳ TO CREATE
└── verify.html             ⏳ TO CREATE
```

## 🎨 SB Admin 2 Components You Can Use

The template includes these pre-built components:

### Cards
```html
<div class="card shadow mb-4">
    <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Card Title</h6>
    </div>
    <div class="card-body">
        Your content here
    </div>
</div>
```

### Buttons
```html
<a href="#" class="btn btn-primary">Primary Button</a>
<a href="#" class="btn btn-success">Success Button</a>
<a href="#" class="btn btn-info">Info Button</a>
<a href="#" class="btn btn-warning">Warning Button</a>
<a href="#" class="btn btn-danger">Danger Button</a>
```

### Alerts
```html
<div class="alert alert-success" role="alert">
    Success message!
</div>
<div class="alert alert-danger" role="alert">
    Error message!
</div>
```

### Progress Bars
```html
<div class="progress">
    <div class="progress-bar" role="progressbar" style="width: 75%">75%</div>
</div>
```

### Tables
```html
<div class="table-responsive">
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Column 1</th>
                <th>Column 2</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </tbody>
    </table>
</div>
```

## 🚀 Next Steps

1. **Continue with Django setup:**
   ```powershell
   # Make sure virtual environment is activated
   .\venv\Scripts\Activate.ps1
   
   # If you haven't installed dependencies yet:
   pip install -r requirements.txt
   
   # Create .env file
   copy .env.example .env
   # Edit .env with your database credentials
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

2. **Collect static files:**
   ```powershell
   python manage.py collectstatic --noinput
   ```
   This copies all static files to the `staticfiles/` directory for serving.

3. **Start the development server:**
   ```powershell
   python manage.py runserver
   ```

4. **Access the application:**
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/
   - Login page: http://localhost:8000/accounts/login/

5. **Create remaining templates:**
   - Start with `dashboard.html` to see the full interface
   - Then create `course_list.html` and `course_detail.html`
   - Add video player and quiz templates
   - Complete with certificate templates

## 💡 Tips for Creating Templates

1. **Always extend base.html:**
   ```django
   {% extends 'base.html' %}
   ```

2. **Use Django template tags:**
   ```django
   {% load static %}  <!-- For static files -->
   {% url 'app:view_name' %}  <!-- For URLs -->
   {% csrf_token %}  <!-- For forms -->
   ```

3. **Access user information:**
   ```django
   {{ user.get_full_name }}
   {{ user.email }}
   {% if user.is_risk_admin %}
       <!-- Risk Admin only content -->
   {% endif %}
   ```

4. **Display messages:**
   ```django
   {% if messages %}
       {% for message in messages %}
       <div class="alert alert-{{ message.tags }}">{{ message }}</div>
       {% endfor %}
   {% endif %}
   ```

5. **Loop through data:**
   ```django
   {% for course in courses %}
       <div class="card">{{ course.title }}</div>
   {% empty %}
       <p>No courses available</p>
   {% endfor %}
   ```

## 📚 Reference

- **SB Admin 2 Demo:** https://startbootstrap.com/theme/sb-admin-2
- **Django Templates:** https://docs.djangoproject.com/en/4.2/topics/templates/
- **Bootstrap 4 Docs:** https://getbootstrap.com/docs/4.6/
- **Font Awesome Icons:** https://fontawesome.com/icons

---

**Template integration complete!** 🎉

You can now start building the rest of your templates. Refer to the original SB Admin 2 HTML files in `C:\Users\Paul\Desktop\startbootstrap-sb-admin-2-gh-pages\` for more examples and components.
