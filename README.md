# STRATOS-DB - Skill Training and Risk Assessment System

A web-based platform for tracking student skill development, assessing risk levels for different competencies, and analyzing the impact of AI on technical skills.

## Features

- **Student Dashboard** - View assigned projects, track task progress, and monitor skill depth
- **Admin Dashboard** - Manage students, projects, skills, tasks, and view analytics
- **Skill Tracking** - Monitor skill development with depth scoring and risk assessment
- **Task Management** - Submit lab tasks and track attempts with detailed feedback
- **Risk Analysis** - AI-powered risk assessment for skills based on automation threat level
- **Project Assignment** - Assign projects to students and track progress
- **Authentication** - Secure login system with role-based access

## Quick Start (Ubuntu/Linux/Mac)

### Prerequisites

- Python 3.8 or later
- pip (Python package manager)

### 1. Clone the Project

```bash
cd stratos-db
```

### 2. Run the Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Initialize the SQLite database with demo data

### 3. Start the Application

```bash
chmod +x run.sh
./run.sh
```

Open your browser to **http://localhost:5000**

## Login Credentials

### Admin Account
- **Username:** admin
- **Password:** admin123

### Student Accounts
- **Username:** student1, student2, student3
- **Password:** student123 (for all)

## Manual Installation (if setup.sh fails)

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

## Folder Structure

```
stratos-db/
├── app.py                 # Flask application entry point
├── config.py              # Configuration settings
├── models.py              # Database models
├── extensions.py          # Flask extensions
├── requirements.txt       # Python dependencies
├── setup.sh              # Automated setup script
├── run.sh                # Script to run the application
├── routes/               # URL routes and handlers
│   ├── auth.py          # Authentication routes
│   ├── admin.py         # Admin dashboard routes
│   ├── student.py       # Student dashboard routes
│   └── api.py           # API endpoints
├── templates/           # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── base.html
│   ├── admin/           # Admin pages
│   └── student/         # Student pages
├── static/              # CSS, JavaScript, images
└── stratos.db          # SQLite database
```

## Troubleshooting

### Issue: "command not found: python3"
```bash
sudo apt-get install python3 python3-pip
```

### Issue: "No module named 'flask'"
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Address already in use"
```bash
pkill -f "python app.py"
# Or use different port: python app.py --port 5001
```

### Issue: Database locked error
```bash
rm stratos.db
./setup.sh
```

## Technologies Used

- **Backend:** Flask (Python web framework)
- **Database:** SQLite (local) / PostgreSQL (production)
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Flask-Login with password hashing
- **ORM:** SQLAlchemy

## For Production (Vercel Deployment)

To deploy to Vercel with persistent Supabase database:

1. Connect your Supabase account in project settings
2. Set `POSTGRES_URL` environment variable
3. Click Publish

The app will automatically use PostgreSQL instead of SQLite.

---

**Happy Learning!** 🚀
