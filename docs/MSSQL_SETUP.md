# Microsoft SQL Server Setup Guide for Risk LMS

## Overview
This guide will help you set up the Risk LMS system with Microsoft SQL Server for production deployment.

---

## Step 1: Install ODBC Driver for SQL Server

### Download and Install
1. Download **ODBC Driver 17 for SQL Server** from Microsoft:
   - https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

2. Or use the direct download link:
   - **Windows x64**: https://go.microsoft.com/fwlink/?linkid=2249004

3. Run the installer and follow the prompts.

### Verify Installation
```powershell
# Check installed ODBC drivers
Get-OdbcDriver | Where-Object {$_.Name -like '*SQL Server*'}
```

---

## Step 2: Create the Database in SQL Server

### Using SQL Server Management Studio (SSMS)
```sql
-- Create the database
CREATE DATABASE risk_lms;
GO

-- Create a dedicated user (optional but recommended)
USE risk_lms;
GO

CREATE LOGIN risk_lms_user WITH PASSWORD = 'YourStrongPassword123!';
GO

CREATE USER risk_lms_user FOR LOGIN risk_lms_user;
GO

-- Grant permissions
ALTER ROLE db_owner ADD MEMBER risk_lms_user;
GO
```

### Alternative: Using sqlcmd
```powershell
sqlcmd -S localhost -U sa -P YourPassword -Q "CREATE DATABASE risk_lms"
```

---

## Step 3: Install Python Dependencies

```powershell
# Activate your virtual environment first
.\venv\Scripts\Activate.ps1

# Install/update all dependencies including MSSQL support
pip install -r requirements.txt

# Or install MSSQL packages separately
pip install mssql-django pyodbc
```

---

## Step 4: Configure Environment Variables

### Option A: Set Environment Variables (Recommended for Production)

**PowerShell (temporary for current session):**
```powershell
$env:DB_ENGINE = "mssql"
$env:DB_NAME = "risk_lms"
$env:DB_USER = "sa"
$env:DB_PASSWORD = "YourStrongPassword123!"
$env:DB_HOST = "localhost"
$env:DB_PORT = "1433"
```

**Windows System Environment Variables (permanent):**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to **Advanced** tab → **Environment Variables**
3. Add new System variables:
   - `DB_ENGINE` = `mssql`
   - `DB_NAME` = `risk_lms`
   - `DB_USER` = `sa` (or your SQL user)
   - `DB_PASSWORD` = `YourStrongPassword123!`
   - `DB_HOST` = `localhost` (or your SQL Server hostname/IP)
   - `DB_PORT` = `1433`

### Option B: Create a .env file (for development)

Create a file named `.env` in the project root:
```
DB_ENGINE=mssql
DB_NAME=risk_lms
DB_USER=sa
DB_PASSWORD=YourStrongPassword123!
DB_HOST=localhost
DB_PORT=1433
```

---

## Step 5: Run Database Migrations

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Create migration files
python manage.py makemigrations

# Apply migrations to MSSQL database
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

---

## Step 6: Migrate Existing Data (Optional)

If you have data in SQLite that you want to migrate to MSSQL:

### Export from SQLite
```powershell
# Set to use SQLite temporarily
$env:DB_ENGINE = "sqlite"

# Export data
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data_backup.json
```

### Import to MSSQL
```powershell
# Switch back to MSSQL
$env:DB_ENGINE = "mssql"

# Load data into MSSQL
python manage.py loaddata data_backup.json
```

---

## Step 7: Start the Application

```powershell
# Development server
python manage.py runserver 0.0.0.0:8000

# For production, use Gunicorn (Windows alternative: waitress)
pip install waitress
waitress-serve --listen=0.0.0.0:8000 risk_lms.wsgi:application
```

---

## Production Deployment Checklist

### Security Settings
Update `settings.py` for production:

```python
# In settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-server-ip', 'your-domain.com', 'localhost']
SECRET_KEY = 'your-very-long-random-secret-key-here'  # Generate a new one!
```

### Generate a New Secret Key
```python
# Run this in Python to generate a secret key
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Collect Static Files
```powershell
python manage.py collectstatic --noinput
```

### IIS Deployment (Windows Server)
1. Install **wfastcgi** for IIS integration:
   ```powershell
   pip install wfastcgi
   wfastcgi-enable
   ```

2. Configure IIS with the appropriate handler mapping.

---

## Troubleshooting

### Connection Error: "Login failed for user"
- Verify SQL Server is running
- Check username and password
- Ensure SQL Server allows SQL authentication (mixed mode)

### Error: "ODBC Driver not found"
- Install ODBC Driver 17 for SQL Server
- Restart your terminal/IDE after installation

### Error: "TCP/IP connection refused"
1. Open **SQL Server Configuration Manager**
2. Enable **TCP/IP** under SQL Server Network Configuration
3. Restart SQL Server service

### Error: "Cannot open database"
- Ensure the database `risk_lms` exists
- Check user has permissions to access the database

### Test Database Connection
```python
# Run this Python script to test connection
import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=risk_lms;"
    "UID=sa;"
    "PWD=YourStrongPassword123!;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

---

## Quick Reference

### Switch Between Databases

**Use MSSQL (Production):**
```powershell
$env:DB_ENGINE = "mssql"
python manage.py runserver
```

**Use SQLite (Development):**
```powershell
$env:DB_ENGINE = "sqlite"
python manage.py runserver
```

### Common Commands
```powershell
# Check database connection
python manage.py dbshell

# Show migrations status
python manage.py showmigrations

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

---

## Server Access URLs

After deployment:
- **Main Application**: http://your-server:8000/
- **Admin Panel**: http://your-server:8000/admin/
- **API Endpoint**: http://your-server:8000/api/

---

## Support

For issues related to:
- **Django + MSSQL**: https://github.com/microsoft/mssql-django
- **ODBC Driver**: https://learn.microsoft.com/en-us/sql/connect/odbc/
- **SQL Server**: https://learn.microsoft.com/en-us/sql/sql-server/
