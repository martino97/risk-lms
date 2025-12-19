# User Roles Guide - Risk LMS

## Updated Role System

The Risk LMS now supports **4 user roles** with different permissions:

### 1. **Admin** (Full System Access)
- Complete access to Django admin panel
- Can manage all users and their roles
- Can upload courses, videos, and create questions
- Can view all progress reports
- Can generate and revoke certificates

### 2. **Head of Risk** (Content Manager)
- Can upload and manage courses
- Can upload videos with translations/subtitles
- Can create and manage question banks
- Can view all user progress
- Can access risk reports and analytics
- **Perfect for**: Risk department heads who oversee training programs

### 3. **Risk & Compliance Specialist** (Content Creator)
- Can upload and manage courses
- Can upload videos with translations/subtitles  
- Can create and manage question banks
- Can view progress for their courses
- **Perfect for**: Team members who create training content

### 4. **Banker** (Learner)
- Can enroll in courses
- Must watch videos completely (95% completion required)
- Can take quizzes (80% passing required)
- Can earn certificates
- Can view personal progress
- **Perfect for**: All bank staff receiving training

---

## How to Assign Roles

### Via Django Admin Panel

1. **Login to Admin Panel**: http://127.0.0.1:8000/admin/
2. Go to **Users** section
3. Click on the user you want to update
4. Change the **Role** dropdown to:
   - `Admin` - Full access
   - `Head of Risk` - Can upload courses/videos
   - `Risk & Compliance Specialist` - Can upload courses/videos
   - `Banker` - Regular learners
5. Click **Save**

### Via Django Shell

```python
python manage.py shell
```

Then:

```python
from accounts.models import User

# Promote user to Head of Risk
user = User.objects.get(email='john@bank.com')
user.role = 'head_of_risk'
user.save()

# Promote user to Risk & Compliance Specialist
user = User.objects.get(email='jane@bank.com')
user.role = 'risk_compliance_specialist'
user.save()

# Set as Banker (default role)
user = User.objects.get(email='banker@bank.com')
user.role = 'banker'
user.save()

exit()
```

---

## Content Upload Permissions

### Who Can Upload Courses?
✅ Admin  
✅ Head of Risk  
✅ Risk & Compliance Specialist  
❌ Banker

### Who Can Upload Videos with Translations?
✅ Admin  
✅ Head of Risk  
✅ Risk & Compliance Specialist  
❌ Banker

### Who Can Create Questions?
✅ Admin  
✅ Head of Risk  
✅ Risk & Compliance Specialist  
❌ Banker

---

## Uploading Courses with Videos & Translations

### Step 1: Create a Course

1. Login with Admin, Head of Risk, or Risk & Compliance Specialist account
2. Go to Admin Panel: http://127.0.0.1:8000/admin/
3. Click on **Courses** > **Add Course**
4. Fill in:
   - **Title**: e.g., "Anti-Money Laundering Training"
   - **Description**: Course overview
   - **Passing Score**: e.g., 80 (default)
5. Click **Save**

### Step 2: Upload Videos

1. In Admin Panel, go to **Videos** > **Add Video**
2. Fill in:
   - **Course**: Select the course you created
   - **Title**: e.g., "Introduction to AML"
   - **Description**: Video description
   - **Video file**: Upload your video (MP4, AVI, MKV supported, max 2GB)
   - **Duration**: Enter video duration in seconds
   - **Order index**: Set video order (0, 1, 2...)
3. Click **Save**

### Step 3: Add Translations/Subtitles

1. In Admin Panel, go to **Video subtitles** > **Add video subtitle**
2. Fill in:
   - **Video**: Select the video
   - **Language code**: e.g., `en` (English), `sw` (Swahili), `fr` (French)
   - **Language name**: e.g., "English", "Swahili", "French"
   - **Subtitle file**: Upload SRT or VTT subtitle file
3. Click **Save**
4. Repeat for each language

**Supported Languages:**
- English (en)
- Swahili (sw)
- French (fr)
- Spanish (es)
- Arabic (ar)
- Portuguese (pt)
- Add more as needed

### Step 4: Create Question Bank

1. In Admin Panel, go to **Questions** > **Add Question**
2. Fill in:
   - **Course**: Select your course
   - **Question text**: Enter the question
   - **Question type**: Multiple choice, True/False, or Multiple answer
   - **Topic**: e.g., "AML Basics", "Regulations", etc.
   - **Difficulty**: Easy, Medium, or Hard
   - **Points**: Default 1
3. **Add Options** (inline form below):
   - Enter each option text
   - Check **Is correct** for the right answer(s)
   - Set order index (0, 1, 2, 3...)
4. Click **Save**

---

## Course Visibility

### Who Can See Courses?

**All courses are visible to ALL users:**
- ✅ Admins can see all courses
- ✅ Head of Risk can see all courses
- ✅ Risk & Compliance Specialists can see all courses
- ✅ **Bankers can see ALL courses** and enroll in them

This ensures that training content uploaded by Head of Risk or Risk & Compliance Specialists is immediately available to all bankers for learning.

---

## Video Player Features

### For Bankers (Learners):

1. **Mandatory Viewing**: Must watch 95% of video to mark as complete
2. **No Skipping**: Progress tracked every 5 seconds
3. **Translation Support**: Can switch between available subtitle languages
4. **Progress Saved**: Can resume where you left off
5. **Skip Detection**: System tracks if you try to skip ahead

### For Content Uploaders:

- Videos automatically processed by FFmpeg
- Thumbnail auto-generated
- Duration detected automatically
- Multiple subtitle tracks supported
- Progress analytics available

---

## Quiz System

### Random Question Selection

- Questions randomly selected from **topic-based pools**
- Each banker gets **different questions** every attempt
- Prevents memorization and cheating
- Fair assessment across all users

### Grading

- **80% passing score** (configurable per course)
- Unlimited retakes allowed
- Only best score counts
- Automatic grading with instant results

---

## Certificate Generation

### Requirements

Bankers must:
1. ✅ Complete ALL videos in ALL enrolled courses (95% each)
2. ✅ Pass ALL quizzes with 80% average
3. ✅ Have active enrollment in courses

### Certificate Features

- **QR Code**: For instant verification
- **PDF Download**: Professional certificate design
- **Unique Number**: Format: RISK-XXXXXXXX
- **Public Verification**: Anyone can verify at /certificates/verify/

---

## Example Workflow

### For Head of Risk / Risk & Compliance Specialist:

1. **Login** to system
2. **Create Course** in admin panel
3. **Upload Videos** with subtitles in multiple languages
4. **Create Questions** for quiz pool
5. **Monitor Progress** - View banker completion rates
6. **Analyze Results** - See quiz performance

### For Bankers:

1. **Login** to system
2. **Browse Courses** - See all available courses
3. **Enroll** in desired courses
4. **Watch Videos** - With translated subtitles
5. **Take Quiz** - Random questions from pool
6. **Earn Certificate** - After 80% average across all courses

---

## Support & Updates

### Current Status
- ✅ 4 user roles implemented
- ✅ Content upload permissions configured
- ✅ Video translations supported
- ✅ All courses visible to bankers
- ✅ Random quiz system active
- ✅ Certificate generation working

### Future Enhancements
- Video streaming optimization
- Mobile app support
- Advanced analytics dashboard
- Bulk user import
- Email notifications
- Course categories

---

**For technical setup, see DJANGO_SETUP.md**  
**For Django commands, see DJANGO_COMMANDS.md**
