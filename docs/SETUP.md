# Quick Setup Guide for Risk LMS

## ⚠️ IMPORTANT: Prerequisites Installation

Before running this project, you MUST install the following:

### 1. Install Node.js (REQUIRED)
- Download: https://nodejs.org/
- Version: v18 or higher
- Verify installation:
  ```bash
  node --version
  npm --version
  ```

### 2. Install PostgreSQL (REQUIRED)
- Download: https://www.postgresql.org/download/windows/
- Version: v14 or higher
- Remember the password you set during installation

### 3. Install FFmpeg (REQUIRED for video features)
- Download: https://ffmpeg.org/download.html
- Windows Guide: https://www.wikihow.com/Install-FFmpeg-on-Windows
- Add to PATH or note the installation path

## 🚀 Setup Steps (After Installing Prerequisites)

### Step 1: Set Up Database
```powershell
# Open psql or pgAdmin and run:
CREATE DATABASE risk_lms;

# Then run the schema file:
# In psql:
\i 'C:/Users/Paul/New folder/backend/src/db/schema.sql'

# Or using command line:
psql -U postgres -d risk_lms -f "C:\Users\Paul\New folder\backend\src\db\schema.sql"
```

### Step 2: Configure Backend
```powershell
cd "C:\Users\Paul\New folder\backend"

# Copy environment file
copy .env.example .env

# Edit .env file and update:
# - DB_PASSWORD (your PostgreSQL password)
# - JWT_SECRET (any random string)
# - FFMPEG_PATH and FFPROBE_PATH (if not in PATH)
```

### Step 3: Install Backend Dependencies
```powershell
cd "C:\Users\Paul\New folder\backend"
npm install
```

### Step 4: Configure Frontend
```powershell
cd "C:\Users\Paul\New folder\frontend"

# Copy environment file
copy .env.example .env
```

### Step 5: Install Frontend Dependencies
```powershell
cd "C:\Users\Paul\New folder\frontend"
npm install
```

### Step 6: Run the Application

Open TWO PowerShell windows:

**Window 1 - Backend:**
```powershell
cd "C:\Users\Paul\New folder\backend"
npm run dev
```

**Window 2 - Frontend:**
```powershell
cd "C:\Users\Paul\New folder\frontend"
npm run dev
```

### Step 7: Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Step 8: Create Admin User
1. Register a new account at http://localhost:3000/register
2. In psql or pgAdmin, promote your user to admin:
   ```sql
   UPDATE users SET role = 'risk_admin' WHERE email = 'your_email@example.com';
   ```
3. Logout and login again to see admin features

## 🎯 What to Do Next

As a Risk Admin, you can:
1. Create courses
2. Upload training videos
3. Add questions for quizzes
4. Manage users

As a Banker, you can:
1. Browse and enroll in courses
2. Watch videos (must watch completely)
3. Take quizzes
4. Earn certificates

## ❓ Troubleshooting

### "npm is not recognized"
- Node.js is not installed. Install from https://nodejs.org/

### "psql is not recognized"
- PostgreSQL is not installed or not in PATH

### "FFmpeg not found"
- FFmpeg is not installed or not in PATH
- Update FFMPEG_PATH in backend/.env

### Port 5000 or 3000 already in use
```powershell
# Find process using port
netstat -ano | findstr :5000
# Kill process (replace PID)
taskkill /PID <process_id> /F
```

### Database connection error
- Check PostgreSQL is running
- Verify DB_PASSWORD in backend/.env
- Ensure database 'risk_lms' exists

## 📚 Full Documentation

See README.md for complete documentation including:
- Detailed API endpoints
- Security features
- Production deployment
- Architecture details

---

**Need Help?** Check the main README.md or create an issue in the repository.
