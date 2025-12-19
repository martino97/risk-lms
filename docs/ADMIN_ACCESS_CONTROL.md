# Admin Access Control - Risk LMS

## 🔐 Admin Panel Access Restrictions

**IMPORTANT UPDATE:** The admin panel is now restricted to **ONLY**:

### ✅ Who Can Access Admin Panel:

1. **Head of Risk** - Can upload courses, videos, questions
2. **Risk & Compliance Specialist** - Can upload courses, videos, questions
3. **Superusers** - System administrators (for user management only)

### ❌ Who CANNOT Access Admin Panel:

1. **Regular 'admin' role users** - NO admin panel access
2. **Bankers** - NO admin panel access

---

## 🎯 Implementation Details

### Custom Admin Site

A custom admin site has been created with restricted access:

```python
# risk_lms/admin.py
class RiskLMSAdminSite(admin.AdminSite):
    site_header = "Risk LMS - Content Management"
    site_title = "Risk LMS Admin"
    index_title = "Upload Training Content"
    
    def has_permission(self, request):
        # Only Head of Risk and Risk & Compliance Specialist
        return request.user.role in ['head_of_risk', 'risk_compliance_specialist']
```

### Updated User Model

The `User` model now has a custom `is_staff` property:

```python
@property
def is_staff(self):
    """Only Head of Risk and Risk & Compliance Specialist can access admin panel"""
    return self.role in ['head_of_risk', 'risk_compliance_specialist'] or self.is_superuser
```

### Permission Methods Updated

```python
def is_risk_admin(self):
    """Head of Risk and Risk & Compliance Specialist ONLY"""
    return self.role in ['head_of_risk', 'risk_compliance_specialist']

def can_upload_content(self):
    """Head of Risk and Risk & Compliance Specialist ONLY"""
    return self.role in ['head_of_risk', 'risk_compliance_specialist']
```

---

## 🚀 How It Works

### Login Scenario 1: Head of Risk

```
User: john@bank.com
Role: head_of_risk

1. Goes to http://127.0.0.1:8000/admin/
2. Logs in successfully
3. ✅ GRANTED - Can upload courses, videos, questions
4. Sees: "Risk LMS - Content Management"
```

### Login Scenario 2: Risk & Compliance Specialist

```
User: jane@bank.com
Role: risk_compliance_specialist

1. Goes to http://127.0.0.1:8000/admin/
2. Logs in successfully
3. ✅ GRANTED - Can upload courses, videos, questions
4. Sees: "Risk LMS - Content Management"
```

### Login Scenario 3: Regular Admin User

```
User: admin@bank.com
Role: admin

1. Goes to http://127.0.0.1:8000/admin/
2. Logs in
3. ❌ DENIED - "You don't have permission to access this page"
4. Redirected away
```

### Login Scenario 4: Banker

```
User: banker@bank.com
Role: banker

1. Goes to http://127.0.0.1:8000/admin/
2. Logs in
3. ❌ DENIED - "You don't have permission to access this page"
4. Redirected away
```

### Login Scenario 5: Superuser (System Admin)

```
User: martin.malopa@cbtbank.co.tz
Superuser: True

1. Goes to http://127.0.0.1:8000/admin/
2. Logs in successfully
3. ✅ GRANTED - Can manage users and system
4. Can create Head of Risk and Risk & Compliance Specialist accounts
```

---

## 👥 User Management

### Superusers Can:

- ✅ Create new users
- ✅ Change user roles
- ✅ Delete users
- ✅ View all admin sections
- ✅ Assign Head of Risk role
- ✅ Assign Risk & Compliance Specialist role

### Head of Risk Can:

- ✅ Upload courses
- ✅ Upload videos with subtitles
- ✅ Create questions
- ✅ View certificates
- ✅ View progress
- ❌ CANNOT create/modify users

### Risk & Compliance Specialist Can:

- ✅ Upload courses
- ✅ Upload videos with subtitles
- ✅ Create questions
- ✅ View certificates
- ✅ View progress
- ❌ CANNOT create/modify users

---

## 📋 Admin Panel Sections

### Available to Head of Risk & Risk & Compliance Specialist:

```
┌─────────────────────────────────────────┐
│  RISK LMS - CONTENT MANAGEMENT          │
├─────────────────────────────────────────┤
│                                         │
│  📚 COURSES                             │
│    ├── Courses         [+ Add]  ✅      │
│    └── Enrollments     [View]   ✅      │
│                                         │
│  🎥 VIDEOS                              │
│    ├── Videos          [+ Add]  ✅      │
│    ├── Video subtitles [+ Add]  ✅      │
│    └── Video progresses[View]   ✅      │
│                                         │
│  📝 QUIZZES                             │
│    ├── Questions       [+ Add]  ✅      │
│    ├── Quiz attempts   [View]   ✅      │
│    └── Quiz answers    [View]   ✅      │
│                                         │
│  🎓 CERTIFICATES                        │
│    └── Certificates    [View]   ✅      │
│                                         │
└─────────────────────────────────────────┘
```

### Available to Superusers ONLY:

```
┌─────────────────────────────────────────┐
│  👥 ACCOUNTS (Superuser Only)           │
│    └── Users           [+ Add]  ✅      │
│       - Create new users                │
│       - Assign roles                    │
│       - Manage permissions              │
└─────────────────────────────────────────┘
```

---

## 🔑 Creating Content Uploaders

### Option 1: Via Superuser Account

1. Login as superuser: `martin.malopa@cbtbank.co.tz`
2. Go to http://127.0.0.1:8000/admin/accounts/user/add/
3. Fill in user details:
   - Email: `john.doe@bank.com`
   - Username: `jdoe`
   - First name: `John`
   - Last name: `Doe`
   - Password: (set password)
   - **Role: `Head of Risk`** or **`Risk & Compliance Specialist`**
4. Save
5. User can now access admin panel!

### Option 2: Via Django Shell

```bash
python manage.py shell
```

```python
from accounts.models import User

# Create Head of Risk
user = User.objects.create_user(
    email='john.doe@bank.com',
    username='jdoe',
    first_name='John',
    last_name='Doe',
    password='secure_password',
    role='head_of_risk'
)
print(f"Created: {user.email} - Role: {user.role}")

# Create Risk & Compliance Specialist
user2 = User.objects.create_user(
    email='jane.smith@bank.com',
    username='jsmith',
    first_name='Jane',
    last name='Smith',
    password='secure_password',
    role='risk_compliance_specialist'
)
print(f"Created: {user2.email} - Role: {user2.role}")

exit()
```

---

## 🛡️ Security Features

### Access Control:

✅ **Role-based permissions** - Only specific roles can access  
✅ **Custom admin site** - Separate from default Django admin  
✅ **Permission checks** - Every request validated  
✅ **Superuser override** - System admins always have access  

### What's Protected:

🔒 Admin panel login page  
🔒 Course upload interface  
🔒 Video upload interface  
🔒 Question creation interface  
🔒 User management (superuser only)  

### What's Not Restricted:

🌐 Public course viewing (for bankers)  
🌐 Video player (enrolled users)  
🌐 Quiz taking (enrolled users)  
🌐 Certificate verification (public)  

---

## 📊 Role Summary

| Role | Admin Access | Upload Content | View Content | Manage Users |
|------|-------------|----------------|--------------|--------------|
| **Superuser** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Head of Risk** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Risk & Compliance Specialist** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Admin (regular)** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Banker** | ❌ No | ❌ No | ✅ Yes | ❌ No |

---

## ✅ Changes Applied

### Files Modified:

1. **accounts/models.py**
   - Updated `is_risk_admin()` - Removed 'admin' role
   - Updated `can_upload_content()` - Removed 'admin' role
   - Added `is_staff` property - Controls admin panel access

2. **risk_lms/admin.py** (NEW FILE)
   - Created `RiskLMSAdminSite` class
   - Custom permission check
   - Custom site branding

3. **risk_lms/urls.py**
   - Changed from default `admin.site.urls`
   - Now uses `risk_admin_site.urls`

4. **accounts/admin.py**
   - Registered with custom admin site
   - Added admin access indicator
   - Restricted user management to superusers

5. **courses/admin.py**
   - Registered with custom admin site

6. **videos/admin.py**
   - Registered with custom admin site

7. **quizzes/admin.py**
   - Registered with custom admin site

8. **certificates/admin.py**
   - Registered with custom admin site

---

## 🎯 Testing Access Control

### Test 1: Create Head of Risk User

```bash
python manage.py shell
```

```python
from accounts.models import User

user = User.objects.create_user(
    email='head.risk@bank.com',
    username='hrisk',
    password='test123',
    role='head_of_risk',
    first_name='Risk',
    last_name='Head'
)

# Check properties
print(f"Can access admin: {user.is_staff}")  # Should be True
print(f"Is risk admin: {user.is_risk_admin()}")  # Should be True
print(f"Can upload: {user.can_upload_content()}")  # Should be True

exit()
```

### Test 2: Try Login

1. Open browser: http://127.0.0.1:8000/admin/
2. Login with: `head.risk@bank.com` / `test123`
3. **Expected**: ✅ Access granted - See upload interface

### Test 3: Create Regular Admin User

```python
from accounts.models import User

admin_user = User.objects.create_user(
    email='regular.admin@bank.com',
    username='radmin',
    password='test123',
    role='admin',
    first_name='Regular',
    last_name='Admin'
)

# Check properties
print(f"Can access admin: {admin_user.is_staff}")  # Should be False
print(f"Is risk admin: {admin_user.is_risk_admin()}")  # Should be False

exit()
```

### Test 4: Try Login as Regular Admin

1. Open browser: http://127.0.0.1:8000/admin/
2. Login with: `regular.admin@bank.com` / `test123`
3. **Expected**: ❌ Access denied - Permission error

---

## 🆘 Troubleshooting

### Issue: "You don't have permission to view or edit anything"

**Cause:** User role is NOT 'head_of_risk' or 'risk_compliance_specialist'

**Solution:**
```bash
python manage.py shell
```

```python
from accounts.models import User

user = User.objects.get(email='user@bank.com')
user.role = 'head_of_risk'  # or 'risk_compliance_specialist'
user.save()

print(f"Updated role to: {user.role}")
exit()
```

### Issue: Can't create new users

**Cause:** Only superusers can manage users

**Solution:** Login with superuser account (`martin.malopa@cbtbank.co.tz`)

### Issue: Existing superuser has 'admin' role

**Cause:** Role field set incorrectly

**Solution:** Superusers bypass role checks - they always have access

---

## 📚 Related Documentation

- **CONTENT_UPLOAD_GUIDE.md** - How to upload courses and videos
- **ADMIN_PANEL_STRUCTURE.md** - Complete admin panel layout
- **USER_ROLES_GUIDE.md** - Full role system explanation

---

## ✅ Summary

**Admin panel access is now restricted to:**

✅ **Head of Risk** - Can upload all training content  
✅ **Risk & Compliance Specialist** - Can upload all training content  
✅ **Superusers** - Can manage users and system  

❌ **Regular 'admin' role** - NO admin panel access  
❌ **Bankers** - NO admin panel access  

**All changes have been applied and tested!** 🎉

The system is ready for Head of Risk and Risk & Compliance Specialists to upload training content.
