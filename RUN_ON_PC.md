# How to Run STRATOS-DB on Any PC

This guide shows how to run STRATOS-DB on **Ubuntu, Linux, Windows, Mac, or any PC with Docker**.

---

## Option 1: Ubuntu/Linux (Recommended for Beginners)

### Requirements
- Ubuntu 18.04 or later
- Internet connection

### Installation & Run

```bash
# 1. Install Python
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# 2. Navigate to project folder
cd /path/to/stratos-db

# 3. Setup (one-time only)
chmod +x setup.sh
./setup.sh

# 4. Run the app
./run.sh
```

**Access:** Open browser to http://localhost:5000

**Credentials:**
- Admin: `admin` / `admin123`
- Student: `student1` / `student123`

---

## Option 2: Windows 10/11

### Requirements
- Python 3.8+ (https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### Installation & Run

```bash
# 1. Extract the ZIP file to a folder
# e.g., C:\Users\YourName\stratos-db

# 2. Open Command Prompt in that folder

# 3. Setup (one-time only)
setup.bat

# 4. Run the app
run.bat
```

**Access:** Open browser to http://localhost:5000

**Credentials:**
- Admin: `admin` / `admin123`
- Student: `student1` / `student123`

---

## Option 3: macOS

### Requirements
- Python 3.8+ (https://www.python.org/downloads/)
- Homebrew (optional): `brew install python3`

### Installation & Run

```bash
# 1. Navigate to project folder
cd /path/to/stratos-db

# 2. Setup (one-time only)
chmod +x setup.sh
./setup.sh

# 3. Run the app
./run.sh
```

**Access:** Open browser to http://localhost:5000

**Credentials:**
- Admin: `admin` / `admin123`
- Student: `student1` / `student123`

---

## Option 4: Docker (Advanced - Works Everywhere)

### Requirements
- Docker installed: https://docs.docker.com/get-docker/

### Installation & Run

```bash
# 1. Navigate to project folder
cd /path/to/stratos-db

# 2. Build and run
docker-compose up --build

# 3. Done! App starts automatically
```

**Access:** Open browser to http://localhost:5000

**Stop the app:**
```bash
docker-compose down
```

---

## Project Structure

```
stratos-db/
├── setup.sh              # Linux/Mac setup script
├── run.sh                # Linux/Mac run script
├── setup.bat             # Windows setup script
├── run.bat               # Windows run script
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Docker compose configuration
├── app.py                # Flask application
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── templates/            # HTML pages
├── routes/               # API routes
├── static/               # CSS/JS/Images
└── stratos.db           # Database (created automatically)
```

---

## What Each Setup Does

### setup.sh / setup.bat
1. Creates Python virtual environment
2. Installs all dependencies
3. Creates SQLite database
4. Creates admin account: `admin` / `admin123`
5. Creates 3 student accounts: `student1-3` / `student123`
6. Creates 5 demo skills

### run.sh / run.bat
1. Activates virtual environment
2. Starts Flask server on port 5000
3. Shows login page at http://localhost:5000

---

## Features

Once running, you can:

### As Admin
- View all students
- Create/manage projects
- Assign tasks to students
- View analytics
- Manage skills and risk levels

### As Student
- View assigned tasks
- Submit task attempts
- Track skill progress
- View AI risk analysis
- Complete projects

---

## Troubleshooting

### "Python not found"
- **Windows:** Reinstall Python and check "Add Python to PATH"
- **Linux:** `sudo apt-get install python3`
- **Mac:** `brew install python3` or download from python.org

### "Port 5000 already in use"
```bash
# Linux/Mac - Kill existing process
lsof -i :5000
kill -9 <PID>

# Or use different port
python app.py --port 8080
```

### "Module not found"
```bash
# Reactivate virtual environment
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate.bat   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "Database locked"
```bash
rm stratos.db
./setup.sh  # or setup.bat on Windows
```

### Still having issues?
See `INSTALL.md` for detailed troubleshooting.

---

## System Requirements

| Feature | Ubuntu/Linux | Windows | macOS | Docker |
|---------|-------------|---------|-------|--------|
| Python 3.8+ | ✓ | ✓ | ✓ | ✓ |
| ~50MB disk | ✓ | ✓ | ✓ | ✓ |
| Internet (setup only) | ✓ | ✓ | ✓ | ✓ |
| Virtual environment | Auto | Auto | Auto | Auto |
| Database setup | Auto | Auto | Auto | Auto |

---

## Next Steps

1. **Run the app** using your OS instructions above
2. **Login** with admin or student credentials
3. **Explore the dashboard**
4. **Create projects** and assign tasks
5. **Submit task attempts** as a student

---

## Getting Help

- **Installation Issues:** See `INSTALL.md`
- **Quick Start:** See `QUICKSTART.md`
- **Full Documentation:** See `README.md`
- **Flask Docs:** https://flask.palletsprojects.com/

---

## Production Deployment

To deploy to Vercel/production:
1. Click **Publish** in v0
2. Connect Supabase for persistent database
3. Set environment variables
4. Deploy automatically

See `README.md` for details.

---

**You're all set! Run the app and start learning.** 🚀
