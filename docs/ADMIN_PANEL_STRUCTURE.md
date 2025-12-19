# Django Admin Panel Structure - Risk LMS

## 🎯 Complete Content Management System

Your Risk LMS has a **fully functional admin panel** where Head of Risk and Risk & Compliance Specialists can upload all training content.

---

## 🔗 Access URLs

```
Main Admin Panel:    http://127.0.0.1:8000/admin/
Course Management:   http://127.0.0.1:8000/admin/courses/course/
Video Management:    http://127.0.0.1:8000/admin/videos/video/
Question Management: http://127.0.0.1:8000/admin/quizzes/question/
User Management:     http://127.0.0.1:8000/admin/accounts/user/
```

---

## 📋 Admin Panel Sections

### 1. COURSES Section

#### **Courses** (`/admin/courses/course/`)
- **List View Shows:**
  - Course title
  - Creator (who uploaded it)
  - Published status (can edit inline)
  - Passing score
  - Created date
  - **Video count** (NEW!)
  - **Question count** (NEW!)

- **Add/Edit Features:**
  - Title field (required)
  - Rich text description
  - Thumbnail upload
  - Passing score setting (default: 80%)
  - Publish toggle
  - Auto-set creator on save

- **Filters:**
  - Published/Unpublished
  - Created date
  - Creator (see only your courses or all)

- **Search:** Search by title or description

#### **Enrollments** (`/admin/courses/enrollment/`)
- See who enrolled in which courses
- Track completion status
- View enrollment dates
- Filter by completion status

---

### 2. VIDEOS Section

#### **Videos** (`/admin/videos/video/`)
- **List View Shows:**
  - Video title
  - Course name
  - Duration (formatted as minutes:seconds)
  - Order index (can edit inline)
  - **Subtitle count** (NEW!)
  - Created date

- **Add/Edit Features:**
  - Course dropdown (required)
  - Title and description
  - **Video file upload** (MP4, AVI, MKV - max 2GB)
  - Thumbnail upload (auto-generated if empty)
  - Duration in seconds
  - Order index for video sequence
  - **Inline subtitle forms** (NEW!) - Add multiple translations right here!
  - Thumbnail preview (NEW!)

- **Inline Subtitles:**
  - Add multiple subtitle tracks without leaving the page
  - Fields: Language code, Language name, Subtitle file
  - Can add English, Swahili, French, etc. all at once

- **Filters:**
  - By course
  - By creation date

- **Search:** Search by title, description, or course name

#### **Video Subtitles** (`/admin/videos/videosubtitle/`)
- **List View Shows:**
  - Video name
  - Language name
  - Language code
  - **Course name** (NEW!)

- **Add/Edit Features:**
  - Video dropdown
  - Language code (en, sw, fr, ar, pt, etc.)
  - Language name (English, Swahili, French, etc.)
  - Subtitle file upload (.srt or .vtt)

- **Filters:**
  - By language code
  - By course (NEW!)

- **Use Cases:**
  - Add translations after video upload
  - Update existing subtitles
  - Add new language translations

#### **Video Progresses** (View Only)
- See learner watch progress
- Track completion rates
- Monitor skip attempts
- View watch duration vs video duration

---

### 3. QUIZZES Section

#### **Questions** (`/admin/quizzes/question/`)
- **List View Shows:**
  - Question text (first 75 chars)
  - Course
  - Topic
  - Difficulty level
  - Question type
  - Points
  - **Options count** (NEW!)

- **Add/Edit Features:**
  - Course dropdown (required)
  - Question text (full question)
  - Question type (Multiple choice, True/False, Multiple answer)
  - Topic field (for grouping: "AML Basics", "Regulations", etc.)
  - Difficulty (Easy, Medium, Hard)
  - Points (default: 1)
  - Optional explanation (shown after answer)
  - **Inline options form** - Add 4+ answer choices right here!

- **Inline Options:**
  - Option text
  - Is correct checkbox
  - Order index
  - Add as many as needed (default: 4)

- **Filters:**
  - By course
  - By topic
  - By difficulty
  - By question type

- **Search:** Search by question text or course name

#### **Quiz Attempts** (View Only)
- See who took quizzes
- View scores and pass/fail status
- Track attempt dates
- Monitor completion times

#### **Quiz Answers** (View Only)
- See individual question answers
- Track correctness
- View answer timestamps

---

### 4. CERTIFICATES Section

#### **Certificates** (`/admin/certificates/certificate/`)
- View issued certificates
- See QR codes
- Verify certificate authenticity
- Track issue dates
- Download PDF certificates

---

### 5. ACCOUNTS Section

#### **Users** (`/admin/accounts/user/`)
- **List View Shows:**
  - Email address
  - Username
  - Full name
  - **Role** (admin, head_of_risk, risk_compliance_specialist, banker)
  - Active status
  - Last login

- **Add/Edit Features:**
  - Email (required, unique)
  - Username
  - First name, Last name
  - Password (hashed)
  - **Role selection** (NEW! 4 roles available)
  - Active status
  - Staff status
  - Superuser status

- **Filters:**
  - By role
  - By active status
  - By staff status

- **Search:** Search by email or username

---

## 🎨 Enhanced Features (Just Added!)

### Course Admin Enhancements
✅ Video count display  
✅ Question count display  
✅ Auto-set creator on save  
✅ Organized fieldsets  
✅ Filter by creator  

### Video Admin Enhancements
✅ Inline subtitle management  
✅ Duration formatted display (25m 30s)  
✅ Subtitle count per video  
✅ Thumbnail preview  
✅ Course filter in subtitle view  
✅ Order index inline editing  

### Question Admin Enhancements
✅ Inline option management (add 4+ at once)  
✅ Question text truncated for readability  
✅ Options count display  
✅ Organized fieldsets  
✅ Enhanced search (course name included)  

---

## 🚀 Upload Workflow

### Complete Course Creation

```
Step 1: Create Course
   ↓
http://127.0.0.1:8000/admin/courses/course/add/
- Fill in title, description
- Upload thumbnail (optional)
- Set passing score (default 80%)
- Check "Published" if ready
- Save

Step 2: Upload Videos
   ↓
http://127.0.0.1:8000/admin/videos/video/add/
- Select course
- Fill in title, description
- Upload video file (MP4 recommended)
- Set duration in seconds
- Set order (0, 1, 2, 3...)
- Add subtitles inline (English, Swahili, etc.)
- Save

Step 3: Create Questions
   ↓
http://127.0.0.1:8000/admin/quizzes/question/add/
- Select course
- Write question
- Set topic (for randomization)
- Set difficulty
- Add 4+ options inline
- Check correct answer(s)
- Save

Step 4: Repeat
   ↓
- Add more videos (change order index)
- Add more questions (different topics)
- Test as banker user

Step 5: Publish
   ↓
- Ensure course is "Published"
- Now visible to all bankers!
```

---

## 🎬 Video Upload Details

### Supported Video Formats
- MP4 (H.264 codec - RECOMMENDED)
- AVI
- MKV
- MOV
- WMV

### Video Processing
- Automatic thumbnail generation (FFmpeg)
- Duration auto-detection
- Progress tracking per user
- 95% completion requirement
- Skip attempt monitoring

### Subtitle Support
- Languages: Any (en, sw, fr, ar, pt, es, de, zh, etc.)
- Formats: SRT, VTT
- Multiple tracks per video
- Switchable during playback
- Encoding: UTF-8

---

## 📝 Question Bank Tips

### Best Practices

**Question Distribution:**
- Create 20-30 questions per course
- Use 3-5 different topics
- Mix difficulty levels (40% Easy, 40% Medium, 20% Hard)
- Random selection ensures fairness

**Question Types:**
- **Multiple Choice**: One correct answer
- **True/False**: Two options only
- **Multiple Answer**: Select all that apply

**Topics Examples:**
- "AML Basics"
- "KYC Requirements"
- "Suspicious Activity"
- "Reporting Procedures"
- "Regulations & Compliance"

### Quality Checks
✅ Clear question wording  
✅ Only one obviously correct answer  
✅ No trick questions  
✅ Relevant to video content  
✅ Explanation provided (optional)  

---

## 🔐 Access Control

### Admin Panel Access

| Role | Can Access Admin Panel? | Can Upload Content? |
|------|------------------------|---------------------|
| **Admin** | ✅ Full access | ✅ Yes |
| **Head of Risk** | ✅ Yes | ✅ Yes |
| **Risk & Compliance Specialist** | ✅ Yes | ✅ Yes |
| **Banker** | ❌ No | ❌ No |

### Content Visibility

**All courses are visible to ALL users:**
- Admins see everything
- Head of Risk sees everything
- Risk & Compliance Specialists see everything
- **Bankers see all published courses** ← Important!

This ensures training content is immediately available to learners.

---

## 📊 Quick Stats

### What's Built:

✅ 6 Django apps (accounts, courses, videos, quizzes, progress, certificates)  
✅ 12+ database models  
✅ Role-based permissions (4 roles)  
✅ File upload support (videos, thumbnails, subtitles)  
✅ Inline editing for subtitles & options  
✅ Smart filtering and search  
✅ Auto-reload on file changes  
✅ SQLite database (working)  
✅ SB Admin 2 template (1,832 files)  

### Admin Panel Features:

✅ Course management with counts  
✅ Video management with inline subtitles  
✅ Question management with inline options  
✅ Subtitle management with language support  
✅ User management with role selection  
✅ Certificate tracking  
✅ Progress monitoring  
✅ Quiz attempt tracking  

---

## 🎯 Test Your Setup

### Verification Checklist:

1. **Access Admin Panel:**
   ```
   http://127.0.0.1:8000/admin/
   Login with: martin.malopa@cbtbank.co.tz
   ```

2. **Create Test Course:**
   - Go to Courses > Add Course
   - Fill in: "Test AML Training"
   - Save

3. **Upload Test Video:**
   - Go to Videos > Add Video
   - Select test course
   - Upload small video file
   - Add English subtitle
   - Save

4. **Create Test Question:**
   - Go to Questions > Add Question
   - Select test course
   - Add question with 4 options
   - Mark one as correct
   - Save

5. **Verify Visibility:**
   - Logout from admin
   - Login as banker (if created)
   - Should see test course

---

## 🆘 Troubleshooting

### Common Issues:

**Issue**: Can't upload large videos  
**Fix**: Edit `risk_lms/settings.py`:
```python
DATA_UPLOAD_MAX_MEMORY_SIZE = 2147483648  # 2GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 2147483648  # 2GB
```

**Issue**: Subtitle not appearing  
**Fix**: Check file encoding (must be UTF-8), check format (.srt/.vtt)

**Issue**: Video won't play in browser  
**Fix**: Convert to MP4 with H.264 codec using HandBrake or FFmpeg

**Issue**: Don't see admin panel  
**Fix**: Ensure user role is NOT "banker"

**Issue**: Can't save inline subtitles  
**Fix**: Click "Save" button at bottom of page, not just inline "Add"

---

## 📚 Related Documentation

- **USER_ROLES_GUIDE.md** - Complete role system explanation
- **CONTENT_UPLOAD_GUIDE.md** - Step-by-step upload instructions
- **DJANGO_SETUP.md** - Initial setup and configuration
- **DJANGO_COMMANDS.md** - Django management commands

---

## ✅ Summary

**You have EVERYTHING you need to upload content:**

1. ✅ Admin panel accessible at http://127.0.0.1:8000/admin/
2. ✅ Course creation interface
3. ✅ Video upload with inline subtitle support
4. ✅ Question bank with inline option editor
5. ✅ Role-based access (Head of Risk + Risk & Compliance Specialist)
6. ✅ Enhanced displays with counts and previews
7. ✅ Smart filtering and search

**Start uploading NOW!** 🚀

The system is ready for Head of Risk and Risk & Compliance Specialists to create and upload training courses with videos, subtitles, and quizzes!
