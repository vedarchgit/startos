# Installation Guide - STRATOS-DB

This guide covers how to run STRATOS-DB on any PC (Linux, Ubuntu, Windows, Mac).

## Quick Links
- [Ubuntu/Linux](#ubuntulinux)
- [Windows 10/11](#windows-1011)
- [macOS](#macos)
- [Docker (Advanced)](#docker-advanced)
- [Troubleshooting](#troubleshooting)

---

## Ubuntu/Linux

### Step 1: Install Python

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
```

Verify installation:
```bash
python3 --version
```

### Step 2: Clone or Extract the Project

```bash
cd /path/to/stratos-db
```

### Step 3: Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

### Step 4: Start the App

```bash
./run.sh
```

Open browser to: **http://localhost:5000**

### Step 5: Stop the App

Press `CTRL+C` in the terminal

---

## Windows 10/11

### Step 1: Install Python

1. Download Python from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT:** Check ✓ "Add Python to PATH"
4. Click "Install Now"

Verify installation:
```bash
python --version
```

### Step 2: Extract the Project

Extract `stratos-db.zip` to any folder, e.g., `C:\Users\YourName\stratos-db`

### Step 3: Run Setup Script

1. Open Command Prompt or PowerShell
2. Navigate to the project folder:
   ```bash
   cd C:\Users\YourName\stratos-db
   ```
3. Run setup:
   ```bash
   setup.bat
   ```
4. Wait for "Setup Complete!" message

### Step 4: Start the App

In the same Command Prompt:
```bash
run.bat
```

Open browser to: **http://localhost:5000**

### Step 5: Stop the App

Press `CTRL+C` in the command prompt

---

## macOS

### Step 1: Install Python

Using Homebrew:
```bash
brew install python3
```

Or download from: https://www.python.org/downloads/

Verify installation:
```bash
python3 --version
```

### Step 2: Clone or Extract the Project

```bash
cd /path/to/stratos-db
```

### Step 3: Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

### Step 4: Start the App

```bash
./run.sh
```

Open browser to: **http://localhost:5000**

### Step 5: Stop the App

Press `CTRL+C` in the terminal

---

## Docker (Advanced)

### Prerequisites
- Docker installed: https://docs.docker.com/get-docker/

### Step 1: Build Docker Image

```bash
docker build -t stratos-db .
```

### Step 2: Run Container

```bash
docker run -p 5000:5000 stratos-db
```

### Step 3: Access the App

Open browser to: **http://localhost:5000**

### Step 4: Stop Container

```bash
docker stop <container_id>
```

---

## Manual Setup (If Scripts Don't Work)

### 1. Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python3 << 'EOF'
from app import app, db
from models import User, Skill, RiskParam

with app.app_context():
    db.create_all()
    
    # Admin user
    admin = User(username='admin', email='admin@stratos.edu', role='Admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Students
    for i in range(1, 4):
        s = User(username=f'student{i}', email=f'student{i}@stratos.edu', 
                 role='Student', branch='CSE', year=2)
        s.set_password('student123')
        db.session.add(s)
    
    # Skills
    for name, cat in [('Python', 'Programming'), ('JavaScript', 'Programming'),
                       ('Database Design', 'Database'), ('Web Development', 'Web')]:
        skill = Skill(name=name, category=cat, description=f'{name} fundamentals')
        db.session.add(skill)
        db.session.flush()
        risk = RiskParam(skill_id=skill.skill_id, repetitiveness=5, 
                        ai_threat_level=6, complexity=7)
        db.session.add(risk)
    
    db.session.commit()
    print("Database initialized!")
EOF
```

### 4. Run the App

```bash
python app.py
```

---

## Troubleshooting

### Python not found

**Windows:**
- Make sure Python was added to PATH during installation
- Close and reopen Command Prompt
- Try `python --version` instead of `python3 --version`

**Linux/Mac:**
```bash
which python3
sudo apt-get install python3.10
```

### Module not found errors

```bash
# Reactivate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate.bat  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Port 5000 already in use

**Linux/Mac:**
```bash
lsof -i :5000
kill -9 <PID>
# Or run on different port: python app.py --port 5001
```

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database locked error

```bash
rm stratos.db      # Linux/Mac
del stratos.db     # Windows

# Then reinitialize:
./setup.sh         # Linux/Mac
setup.bat          # Windows
```

### Can't access http://localhost:5000

1. Make sure the Flask app is running
2. Check if port 5000 is blocked by firewall
3. Try: http://127.0.0.1:5000
4. Try different port: `python app.py --port 8080`

### Connection timeout

1. Verify app is running: Check terminal for "Running on http://..."
2. Try restarting: Press CTRL+C and run `./run.sh` again
3. Check network: App needs to bind to localhost

### Permission denied (on .sh files)

```bash
chmod +x setup.sh run.sh
```

### Still having issues?

1. Check you're in the correct directory
2. Ensure Python 3.8+ is installed
3. Try manual setup steps above
4. Verify all files are extracted/cloned properly

---

## Verify Installation

After setup, test with:

```bash
curl http://localhost:5000/login
```

You should see HTML content (login page).

Test login:
```bash
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=admin123"
```

---

## Next Steps

1. Open http://localhost:5000 in browser
2. Login with credentials:
   - **Admin:** admin / admin123
   - **Students:** student1-3 / student123
3. Explore the dashboard
4. Create new projects and assign tasks
5. Submit task attempts as a student

---

## Getting Help

- **Flask Docs:** https://flask.palletsprojects.com/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **Python Docs:** https://docs.python.org/3/

---

Happy learning! 🚀
