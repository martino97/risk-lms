# Risk Department Learning Management System (LMS)

A comprehensive Learning Management System designed for risk department training with video tutorials, translation support, mandatory viewing tracking, random quiz generation, and certificate issuance.

## 🎯 Features

### For Bankers (Users)
- 📹 **Video Learning** - Watch training videos with translation/subtitle support
- ⏯️ **Mandatory Viewing** - Videos must be watched completely (no skipping)
- 📝 **Random Quizzes** - Different questions for each attempt from topic-based question pools
- 📊 **Progress Tracking** - Real-time tracking of course completion
- 🎓 **Certificates** - Automatic certificate generation with 80% benchmark
- 🔗 **QR Codes** - Shareable certificate verification via QR codes

### For Risk Admins
- 📤 **Video Upload** - Upload training videos with automatic processing
- 🌐 **Translation Management** - Add subtitles in multiple languages
- ❓ **Question Bank** - Create and manage question pools by topic
- 👥 **User Management** - Manage banker accounts and roles
- 📈 **Analytics Dashboard** - Track user progress and course completion rates
- ✅ **Course Publishing** - Control when courses become available

## 🛠️ Technology Stack

### Backend
- **Node.js** with **Express.js** - RESTful API server
- **TypeScript** - Type-safe development
- **PostgreSQL** - Relational database
- **JWT** - Authentication & authorization
- **Multer** - File upload handling
- **FFmpeg** - Video processing
- **PDFKit** - Certificate generation
- **QRCode** - QR code generation

### Frontend
- **React 18** with **TypeScript** - UI framework
- **Vite** - Fast build tool
- **React Router** - Client-side routing
- **TailwindCSS** - Utility-first styling
- **Axios** - HTTP client
- **React Query** - Data fetching & caching
- **React Player** - Video playback

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v18 or higher)
- **PostgreSQL** (v14 or higher)
- **FFmpeg** (for video processing)
- **Git**

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "New folder"
```

### 2. Database Setup

```bash
# Create a PostgreSQL database
createdb risk_lms

# Or using psql
psql -U postgres
CREATE DATABASE risk_lms;
\q

# Run the schema
psql -U postgres -d risk_lms -f backend/src/db/schema.sql
```

### 3. Backend Setup

```bash
cd backend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env

# Edit .env with your configuration
# Update database credentials, JWT secret, etc.

# Build TypeScript
npm run build

# Run database migrations (if needed)
npm run migrate

# Start development server
npm run dev
```

The backend server will start on `http://localhost:5000`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env

# Edit .env if backend URL is different

# Start development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## 📝 Environment Variables

### Backend (.env)

```env
# Server
PORT=5000
NODE_ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=risk_lms
DB_USER=postgres
DB_PASSWORD=your_password

# JWT
JWT_SECRET=your_secret_key_here
JWT_EXPIRES_IN=7d

# File Upload
MAX_FILE_SIZE=2147483648
UPLOAD_DIR=./uploads
VIDEO_DIR=./uploads/videos
QUESTION_DIR=./uploads/questions
CERTIFICATE_DIR=./uploads/certificates

# Frontend URL
FRONTEND_URL=http://localhost:3000

# FFmpeg (Windows paths)
FFMPEG_PATH=C:/ffmpeg/bin/ffmpeg.exe
FFPROBE_PATH=C:/ffmpeg/bin/ffprobe.exe

# Certificate
CERTIFICATE_BASE_URL=http://localhost:5000/certificates
QR_CODE_SIZE=200
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:5000/api
```

## 🎮 Usage

### Initial Setup

1. **Create Admin Account**
   - Register a new account via `/register`
   - Manually update the user's role in the database to `risk_admin`:
   ```sql
   UPDATE users SET role = 'risk_admin' WHERE email = 'admin@example.com';
   ```

2. **Login**
   - Navigate to `/login`
   - Use your credentials to access the system

### For Risk Admins

1. **Create a Course**
   - Go to Admin → Course Management
   - Click "Create Course"
   - Fill in course details
   - Set passing score (default: 80%)

2. **Upload Videos**
   - Select a course
   - Upload video files (MP4, MOV supported)
   - Add video titles and descriptions
   - Upload subtitles/translations (VTT, SRT format)

3. **Create Questions**
   - Go to Admin → Question Management
   - Select a course
   - Add questions with multiple-choice options
   - Assign topics to questions
   - Set correct answers

4. **Publish Course**
   - Review course content
   - Click "Publish" to make it available to bankers

### For Bankers

1. **Browse Courses**
   - View available courses on the Dashboard
   - Click on a course to see details

2. **Enroll in Course**
   - Click "Enroll" button
   - Start watching videos in sequence

3. **Watch Videos**
   - Videos must be watched without skipping
   - Progress is tracked automatically
   - Subtitles can be enabled if available

4. **Take Quizzes**
   - After completing all videos
   - Answer random questions (10 per quiz)
   - Each attempt has different questions
   - Get instant feedback

5. **Earn Certificates**
   - Complete all courses
   - Maintain 80%+ average score
   - Certificate is auto-generated
   - Download PDF or share QR code
   - Anyone can verify certificate authenticity

## 📁 Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── config/         # Database & app configuration
│   │   ├── controllers/    # Route controllers
│   │   ├── db/            # Database schema & migrations
│   │   ├── middleware/    # Auth, upload, error handling
│   │   ├── routes/        # API route definitions
│   │   └── server.ts      # Express app entry point
│   ├── uploads/           # Uploaded files (videos, certificates)
│   ├── package.json
│   └── tsconfig.json
│
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── context/       # React context (Auth)
│   │   ├── pages/         # Page components
│   │   │   └── admin/    # Admin pages
│   │   ├── types/         # TypeScript interfaces
│   │   ├── utils/         # API utilities
│   │   ├── App.tsx        # Main app component
│   │   └── main.tsx       # Entry point
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Courses
- `GET /api/courses` - List all published courses
- `GET /api/courses/:id` - Get course details
- `POST /api/courses` - Create course (admin)
- `PUT /api/courses/:id` - Update course (admin)
- `DELETE /api/courses/:id` - Delete course (admin)
- `POST /api/courses/:id/enroll` - Enroll in course

### Videos
- `GET /api/videos/course/:courseId` - Get course videos
- `GET /api/videos/:id` - Get video details
- `POST /api/videos/upload` - Upload video (admin)
- `POST /api/videos/:id/progress` - Update watch progress
- `POST /api/videos/:id/subtitles` - Upload subtitles (admin)
- `DELETE /api/videos/:id` - Delete video (admin)

### Quizzes
- `POST /api/quizzes/start/:courseId` - Start quiz attempt
- `POST /api/quizzes/answer/:attemptId` - Submit answer
- `POST /api/quizzes/complete/:attemptId` - Complete quiz
- `GET /api/quizzes/results/:attemptId` - Get quiz results
- `POST /api/quizzes/questions` - Create question (admin)
- `GET /api/quizzes/questions/course/:courseId` - List questions (admin)

### Progress
- `GET /api/progress/user/:userId` - Get user progress
- `GET /api/progress/course/:courseId` - Get course progress
- `GET /api/progress/overall/:userId` - Get overall progress

### Certificates
- `POST /api/certificates/generate/:userId` - Generate certificate
- `GET /api/certificates/:id` - Get certificate
- `GET /api/certificates/user/:userId` - Get user certificates
- `GET /api/certificates/verify/:certificateNumber` - Verify certificate (public)

## 🎯 Key Features Implementation

### Mandatory Video Watching
- Frontend tracks playback position every 5 seconds
- Skip attempts are logged in the database
- Video marked complete only after watching 95% or more
- Progress bar cannot be dragged to skip ahead

### Random Question Selection
- Questions are randomly selected from the pool for each quiz attempt
- Topic-based filtering ensures relevant questions
- 10 questions per quiz by default
- Different questions for each user and attempt

### 80% Benchmark Grading
- Each quiz calculates score (correct/total * 100)
- Overall average must be ≥80% across all course quizzes
- Certificate generation checks this requirement
- Visual feedback on pass/fail status

### Certificate Generation
- Automatically generated when user meets requirements
- PDF certificate with user name, date, score
- Unique certificate number
- QR code for verification
- Public verification endpoint

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- File upload validation & sanitization
- SQL injection prevention with parameterized queries
- CORS configuration
- Helmet.js for HTTP headers security

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_ctl status

# Test connection
psql -U postgres -d risk_lms
```

### FFmpeg Not Found
```bash
# Install FFmpeg on Windows
# Download from: https://ffmpeg.org/download.html
# Add to PATH or update .env with full path
```

### Port Already in Use
```bash
# Backend (port 5000)
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Frontend (port 3000)
netstat -ano | findstr :3000
taskkill /PID <process_id> /F
```

## 📦 Building for Production

### Backend
```bash
cd backend
npm run build
npm start
```

### Frontend
```bash
cd frontend
npm run build
# Serve the 'dist' folder with a static server
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Support

For support, email support@example.com or create an issue in the repository.

## 🎉 Acknowledgments

- Risk Department team for requirements
- Open source community for excellent libraries
- All contributors to this project

---

**Built with ❤️ for Risk Department Training**
