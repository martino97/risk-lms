# Content Upload Guide - Risk LMS

## ✅ YES! You Have Full Upload Capabilities

Your Risk LMS **already has a complete content management system** built into the Django Admin Panel.

**Head of Risk** and **Risk & Compliance Specialists** can upload:
- ✅ Video courses
- ✅ Video files (MP4, AVI, MKV - up to 2GB)
- ✅ Multiple subtitle/translation files per video
- ✅ Question banks for quizzes
- ✅ Course thumbnails

---

## 🎯 How to Access Content Upload Module

### Step 1: Login to Admin Panel

1. Open your browser: **http://127.0.0.1:8000/admin/**
2. Login with your credentials:
   - Email: `martin.malopa@cbtbank.co.tz` (or your admin email)
   - Password: (your password)

### Step 2: Navigate to Content Sections

You'll see these sections in the admin panel:

```
┌─────────────────────────────────────────┐
│  DJANGO ADMIN PANEL                     │
├─────────────────────────────────────────┤
│                                         │
│  📚 COURSES                             │
│    ├── Courses         [+ Add]          │
│    └── Enrollments     [+ Add]          │
│                                         │
│  🎥 VIDEOS                              │
│    ├── Videos          [+ Add]  ← HERE! │
│    ├── Video subtitles [+ Add]  ← HERE! │
│    └── Video progresses                 │
│                                         │
│  📝 QUIZZES                             │
│    ├── Questions       [+ Add]  ← HERE! │
│    ├── Question options                 │
│    ├── Quiz attempts                    │
│    └── Quiz answers                     │
│                                         │
│  🎓 CERTIFICATES                        │
│    └── Certificates                     │
│                                         │
│  👥 ACCOUNTS                            │
│    └── Users                            │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📹 How to Upload Video Content

### Method 1: Upload Pre-recorded Video

#### Step A: Create a Course

1. Click **Courses** > **+ Add Course**
2. Fill in the form:

```
┌──────────────────────────────────────┐
│  Add Course                           │
├──────────────────────────────────────┤
│                                       │
│  Title: *                             │
│  ┌─────────────────────────────────┐ │
│  │ Anti-Money Laundering Training  │ │
│  └─────────────────────────────────┘ │
│                                       │
│  Description:                         │
│  ┌─────────────────────────────────┐ │
│  │ Comprehensive AML training for  │ │
│  │ all banking staff...            │ │
│  └─────────────────────────────────┘ │
│                                       │
│  Thumbnail: [Choose File]             │
│                                       │
│  Passing Score: 80                    │
│                                       │
│  ☑ Published                          │
│                                       │
│  Created by: (auto-filled)            │
│                                       │
│  [Save and add another]  [Save]       │
└──────────────────────────────────────┘
```

3. Click **Save**

#### Step B: Upload Video Files

1. Click **Videos** > **+ Add Video**
2. Fill in the video form:

```
┌──────────────────────────────────────┐
│  Add Video                            │
├──────────────────────────────────────┤
│                                       │
│  Course: *                            │
│  ┌─────────────────────────────────┐ │
│  │ Anti-Money Laundering Training ▼│ │
│  └─────────────────────────────────┘ │
│                                       │
│  Title: *                             │
│  ┌─────────────────────────────────┐ │
│  │ Module 1: Introduction to AML   │ │
│  └─────────────────────────────────┘ │
│                                       │
│  Description:                         │
│  ┌─────────────────────────────────┐ │
│  │ Basic concepts and regulations  │ │
│  └─────────────────────────────────┘ │
│                                       │
│  Video file: * [Choose File]          │
│  (Supported: MP4, AVI, MKV, MOV)      │
│  (Max size: 2GB)                      │
│                                       │
│  Thumbnail: [Choose File]             │
│  (Auto-generated if not provided)     │
│                                       │
│  Duration (seconds): * 1800           │
│  (30 minutes = 1800 seconds)          │
│                                       │
│  Order index: * 0                     │
│  (0 = first video)                    │
│                                       │
├──────────────────────────────────────┤
│  📝 SUBTITLES (Add translations)      │
├──────────────────────────────────────┤
│                                       │
│  Subtitle 1:                          │
│  ├─ Language code: en                 │
│  ├─ Language name: English            │
│  └─ Subtitle file: [Choose .srt]      │
│                                       │
│  Subtitle 2:                          │
│  ├─ Language code: sw                 │
│  ├─ Language name: Swahili            │
│  └─ Subtitle file: [Choose .srt]      │
│                                       │
│  [+ Add another subtitle]             │
│                                       │
│  [Save and add another]  [Save]       │
└──────────────────────────────────────┘
```

3. Click **Save**

#### Step C: Add More Translations (Optional)

You can also add subtitles separately:

1. Click **Video subtitles** > **+ Add video subtitle**
2. Fill in:
   - Video: (select your video)
   - Language code: `fr` (French), `ar` (Arabic), `pt` (Portuguese), etc.
   - Language name: `French`, `Arabic`, `Portuguese`
   - Subtitle file: Upload `.srt` or `.vtt` file

---

## 📝 How to Create Question Banks

### Add Questions for Quizzes

1. Click **Questions** > **+ Add Question**
2. Fill in the question form:

```
┌──────────────────────────────────────┐
│  Add Question                         │
├──────────────────────────────────────┤
│                                       │
│  Course: *                            │
│  ┌─────────────────────────────────┐ │
│  │ Anti-Money Laundering Training ▼│ │
│  └─────────────────────────────────┘ │
│                                       │
│  Question text: *                     │
│  ┌─────────────────────────────────┐ │
│  │ What is the primary purpose of  │ │
│  │ AML regulations?                │ │
│  └─────────────────────────────────┘ │
│                                       │
│  Question type: *                     │
│  ┌─────────────────────────────────┐ │
│  │ Multiple Choice              ▼  │ │
│  └─────────────────────────────────┘ │
│                                       │
│  Topic:                               │
│  ┌─────────────────────────────────┐ │
│  │ AML Basics                      │ │
│  └─────────────────────────────────┘ │
│                                       │
│  Difficulty:                          │
│  ┌─────────────────────────────────┐ │
│  │ Medium                       ▼  │ │
│  └─────────────────────────────────┘ │
│                                       │
│  Points: 1                            │
│                                       │
│  Explanation: (optional)              │
│  ┌─────────────────────────────────┐ │
│  │ AML prevents money laundering   │ │
│  └─────────────────────────────────┘ │
│                                       │
├──────────────────────────────────────┤
│  📌 OPTIONS (Add answer choices)      │
├──────────────────────────────────────┤
│                                       │
│  Option 1:                            │
│  ├─ Text: Prevent money laundering    │
│  ├─ ☑ Is correct                      │
│  └─ Order: 0                          │
│                                       │
│  Option 2:                            │
│  ├─ Text: Increase bank profits       │
│  ├─ ☐ Is correct                      │
│  └─ Order: 1                          │
│                                       │
│  Option 3:                            │
│  ├─ Text: Reduce customer numbers     │
│  ├─ ☐ Is correct                      │
│  └─ Order: 2                          │
│                                       │
│  Option 4:                            │
│  ├─ Text: Avoid tax payments          │
│  ├─ ☐ Is correct                      │
│  └─ Order: 3                          │
│                                       │
│  [+ Add another option]               │
│                                       │
│  [Save and add another]  [Save]       │
└──────────────────────────────────────┘
```

3. Add at least 4 options (one correct)
4. Click **Save**
5. Repeat for more questions

**💡 Pro Tip:** Create 20-30 questions per topic with different difficulty levels for better randomization!

---

## 🎙️ Recording Content (Alternative Method)

If you want to **record videos directly** instead of uploading:

### Option 1: Use Screen Recording Software

**Windows Built-in (Xbox Game Bar):**
1. Press `Windows + G`
2. Click **Record** button
3. Record your presentation/tutorial
4. Stop recording (saved to `Videos/Captures/`)
5. Upload the recorded file via Admin Panel

**Recommended Tools:**
- **OBS Studio** (Free): https://obsproject.com/
- **Camtasia** (Paid): Professional editing
- **Loom** (Free/Paid): Quick screen recordings

### Option 2: Use External Camera

1. Record with camera/phone
2. Transfer video file to computer
3. (Optional) Edit with video editor
4. Upload via Admin Panel

### Option 3: Use Zoom/Teams Recording

1. Start Zoom/Teams meeting (can be solo)
2. Share screen and record
3. Stop meeting - video auto-saves
4. Upload via Admin Panel

---

## 🌐 Creating Subtitle Files

### Subtitle Format: .SRT (SubRip)

Create a text file with `.srt` extension:

```srt
1
00:00:00,000 --> 00:00:05,000
Welcome to Anti-Money Laundering Training

2
00:00:05,000 --> 00:00:10,000
In this module, we will cover the basics of AML

3
00:00:10,000 --> 00:00:15,000
AML stands for Anti-Money Laundering
```

### Tools to Create Subtitles

**Automatic (AI):**
- **YouTube Studio**: Upload video, auto-generate, download SRT
- **Happy Scribe**: https://www.happyscribe.com/
- **Otter.ai**: https://otter.ai/

**Manual:**
- **Subtitle Edit** (Free): https://www.nikse.dk/subtitleedit/
- **Aegisub** (Free): http://www.aegisub.org/

**Translation:**
- Use Google Translate or DeepL
- Hire professional translator
- Use AI translation services

---

## 📊 Admin Panel Features

### Enhanced Features Already Built:

1. **Course Management**
   - ✅ See video count per course
   - ✅ See question count per course
   - ✅ Publish/unpublish courses
   - ✅ Auto-set creator on save

2. **Video Management**
   - ✅ Add multiple subtitles inline
   - ✅ See subtitle count per video
   - ✅ Preview thumbnail
   - ✅ Duration formatted (minutes:seconds)
   - ✅ Drag-and-drop file upload

3. **Question Management**
   - ✅ Add 4+ options inline
   - ✅ Mark correct answers
   - ✅ Organize by topic
   - ✅ Set difficulty levels
   - ✅ See option count

4. **Smart Filters**
   - Filter courses by creator
   - Filter videos by course
   - Filter questions by topic/difficulty
   - Search by title/description

---

## 🔐 Permissions

### Who Can Upload?

| Role | Upload Courses | Upload Videos | Create Questions |
|------|----------------|---------------|------------------|
| **Admin** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Head of Risk** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Risk & Compliance Specialist** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Banker** | ❌ No | ❌ No | ❌ No |

---

## 🎯 Quick Upload Workflow

### Complete Course Setup (30 minutes):

1. **Create Course** (2 min)
2. **Upload 3-5 Videos** (10 min)
3. **Add Subtitles for each** (5 min)
4. **Create 20 Questions** (10 min)
5. **Publish Course** (1 min)
6. **Done!** Bankers can now enroll

---

## 📱 Video Requirements

### Supported Formats
- ✅ MP4 (recommended)
- ✅ AVI
- ✅ MKV
- ✅ MOV
- ✅ WMV

### Recommended Settings
- **Resolution**: 1280x720 (720p) or 1920x1080 (1080p)
- **Frame Rate**: 30fps
- **Bitrate**: 2-5 Mbps
- **Audio**: AAC, 128-192 kbps
- **Max Size**: 2GB per file

### Optimization Tips
- Compress large videos with **HandBrake** (free)
- Remove silent parts with video editor
- Use consistent naming: `Module1_Introduction.mp4`

---

## ✅ Current Status

### What's Already Working:

✅ Django Admin Panel accessible at http://127.0.0.1:8000/admin/  
✅ Course upload interface with thumbnail support  
✅ Video upload with subtitle inline forms  
✅ Question creation with multiple options  
✅ Role-based permissions (Head of Risk + Risk & Compliance Specialist)  
✅ Auto-set creator on course save  
✅ Smart filtering and search  
✅ Enhanced list displays with counts  
✅ Subtitle management for translations  

### Ready to Use NOW! 🚀

Just login to the admin panel and start uploading!

---

## 🆘 Support

### Common Issues

**Problem**: Can't upload large video  
**Solution**: Check `settings.py` - increase `DATA_UPLOAD_MAX_MEMORY_SIZE`

**Problem**: Subtitle not showing  
**Solution**: Ensure `.srt` file is properly formatted (check encoding: UTF-8)

**Problem**: Video won't play  
**Solution**: Convert to MP4 with H.264 codec using HandBrake

**Problem**: Can't access admin panel  
**Solution**: Ensure user role is `admin`, `head_of_risk`, or `risk_compliance_specialist`

---

**Ready to start uploading? Go to: http://127.0.0.1:8000/admin/**
