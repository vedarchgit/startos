# STRATOS-DB - Start Here!

Welcome to STRATOS-DB! This guide will get you up and running in minutes.

## What is STRATOS-DB?

STRATOS-DB is a **Skill Training and Risk Assessment System** - a web platform for:
- Student skill development tracking
- AI risk analysis for technical competencies
- Project assignment and task management
- Learning progress monitoring

---

## Quick Start (Choose Your OS)

### 🐧 Linux / Ubuntu / macOS

```bash
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

Then open: **http://localhost:5000**

### 🪟 Windows 10/11

```bash
setup.bat
run.bat
```

Then open: **http://localhost:5000**

### 🐳 Docker (Any OS)

```bash
docker-compose up --build
```

Then open: **http://localhost:5000**

---

## Login Credentials

```
Admin Dashboard
Username: admin
Password: admin123

Student Dashboard  
Username: student1 (or student2, student3)
Password: student123
```

---

## What to Do First

1. **Run the app** (see above for your OS)
2. **Login as admin** to explore the dashboard
3. **Create a project** and assign tasks
4. **Login as student** to submit tasks
5. **View analytics** to see progress

---

## Documentation Files

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | 2-minute setup guide |
| `INSTALL.md` | Detailed installation for any OS |
| `RUN_ON_PC.md` | Run on any PC (step-by-step) |
| `COMMANDS.md` | All available commands |
| `README.md` | Full project documentation |

---

## Folder Overview

```
stratos-db/
├── app.py                 # Flask application
├── models.py              # Database models (User, Skill, Task, etc.)
├── requirements.txt       # Python dependencies
├── setup.sh / setup.bat   # Automated setup
├── run.sh / run.bat       # Run the app
├── Dockerfile             # Docker setup
├── docker-compose.yml     # Docker compose
├── templates/             # HTML pages (login, dashboard, etc.)
├── routes/                # API endpoints
├── static/                # CSS, JavaScript, images
└── stratos.db            # Database (created automatically)
```

---

## System Requirements

✅ **Python 3.8+** - https://www.python.org/downloads/  
✅ **~50MB disk space**  
✅ **Internet connection** (for setup only)  
✅ **All OS supported** (Windows, Mac, Linux, Ubuntu)

---

## Features Overview

### Admin Features
- Dashboard with analytics
- Manage students and accounts
- Create projects and assign tasks
- Define skills and risk parameters
- View detailed analytics

### Student Features
- Track assigned projects
- View available tasks
- Submit task attempts
- Monitor skill progress
- View AI risk analysis

### Technical Features
- Secure authentication
- SQLite database (local) / PostgreSQL (production)
- Responsive web interface
- Password hashing with bcrypt
- Session management
- Rate limiting

---

## Common Tasks

### Start the App
```bash
./run.sh              # Linux/Mac
run.bat               # Windows
docker-compose up     # Docker
```

### Stop the App
Press **CTRL+C** in terminal

### Check if App is Running
Visit **http://localhost:5000** in browser

### Reset Database
```bash
rm stratos.db         # Linux/Mac
del stratos.db        # Windows
./setup.sh            # or setup.bat on Windows
```

### View Logs
```bash
docker-compose logs -f  # If using Docker
# Or just watch terminal output
```

---

## Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| "Python not found" | Install Python 3.8+ from python.org |
| "Port 5000 in use" | Kill process: `lsof -i :5000` then `kill -9 <PID>` |
| "Module not found" | Rerun setup: `./setup.sh` |
| "Database locked" | Delete database: `rm stratos.db` then rerun setup |
| "Can't connect" | Check firewall allows port 5000 |

For more help, see **INSTALL.md** or **COMMANDS.md**.

---

## Next Steps

1. ✅ Choose your OS and run the app
2. ✅ Login to explore the interface
3. ✅ Create some projects and tasks
4. ✅ Submit task attempts as student
5. ✅ View analytics as admin

---

## Need Help?

- **Quick Start:** See `QUICKSTART.md`
- **Installation Issues:** See `INSTALL.md`
- **All Commands:** See `COMMANDS.md`
- **Full Docs:** See `README.md`
- **Run on PC:** See `RUN_ON_PC.md`

---

## Technology Stack

- **Backend:** Flask (Python web framework)
- **Database:** SQLite (local) / PostgreSQL (production)
- **Frontend:** HTML5, CSS3, JavaScript
- **ORM:** SQLAlchemy
- **Security:** Flask-Login, bcrypt, CSRF protection

---

## Deployment

### Local Testing
Perfect! You're already set up for local testing.

### Production (Vercel)
1. Click **Publish** in v0
2. Connect Supabase for persistent database
3. Set environment variables
4. Deploy automatically

See `README.md` for production setup details.

---

## What You Can Build

This platform is perfect for:
- **Educational institutions** - Track student learning
- **Training programs** - Monitor skill development
- **Corporate learning** - Assess employee capabilities
- **Research** - Analyze AI impact on skills

---

## Support & Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **Python Docs:** https://docs.python.org/3/
- **Docker Docs:** https://docs.docker.com/

---

## Ready to Start?

### Pick your OS and run:

**Linux/Mac:**
```bash
chmod +x setup.sh run.sh && ./setup.sh && ./run.sh
```

**Windows:**
```bash
setup.bat && run.bat
```

**Docker:**
```bash
docker-compose up --build
```

Then visit **http://localhost:5000** 🚀

---

**Enjoy learning with STRATOS-DB!**
