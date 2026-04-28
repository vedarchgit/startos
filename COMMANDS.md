# STRATOS-DB Commands Reference

Quick reference for all commands to run STRATOS-DB.

---

## Linux / Ubuntu / macOS

### First Time Setup
```bash
chmod +x setup.sh run.sh
./setup.sh
```

### Run the App
```bash
./run.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 << 'EOF'
from app import app, db
from models import User, Skill, RiskParam

with app.app_context():
    db.create_all()
    
    admin = User(username='admin', email='admin@stratos.edu', role='Admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    for i in range(1, 4):
        s = User(username=f'student{i}', email=f'student{i}@stratos.edu', role='Student')
        s.set_password('student123')
        db.session.add(s)
    
    db.session.commit()
EOF

# Run
python app.py
```

### Stop the App
```bash
# In the terminal where Flask is running:
CTRL+C

# Or kill the process:
pkill -f "python app.py"
```

### Troubleshooting
```bash
# Check if app is running
curl http://localhost:5000

# Check which process is using port 5000
lsof -i :5000

# Kill a specific process
kill -9 <PID>

# Remove database and reinitialize
rm stratos.db
./setup.sh
```

---

## Windows

### First Time Setup
```bash
setup.bat
```

### Run the App
```bash
run.bat
```

### Manual Setup
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Initialize database
python << 'EOF'
from app import app, db
from models import User, Skill, RiskParam

with app.app_context():
    db.create_all()
    
    admin = User(username='admin', email='admin@stratos.edu', role='Admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    for i in range(1, 4):
        s = User(username=f'student{i}', email=f'student{i}@stratos.edu', role='Student')
        s.set_password('student123')
        db.session.add(s)
    
    db.session.commit()
EOF

# Run
python app.py
```

### Stop the App
```bash
# In the command prompt where Flask is running:
CTRL+C

# Or kill the process:
taskkill /F /IM python.exe
```

### Troubleshooting
```bash
# Check if app is running
curl http://localhost:5000

# Check which process is using port 5000
netstat -ano | findstr :5000

# Kill a specific process
taskkill /PID <PID> /F

# Remove database and reinitialize
del stratos.db
setup.bat
```

---

## Docker

### Build and Run
```bash
docker-compose up --build
```

### Run (after first build)
```bash
docker-compose up
```

### Stop
```bash
docker-compose down
```

### Rebuild
```bash
docker-compose build --no-cache
docker-compose up
```

### View Logs
```bash
docker-compose logs -f web
```

### Access Database
```bash
docker-compose exec web sqlite3 stratos.db
```

---

## Python Virtual Environment

### Activate (Linux/Mac)
```bash
source .venv/bin/activate
```

### Activate (Windows)
```bash
.venv\Scripts\activate.bat
```

### Deactivate
```bash
deactivate
```

### Install Packages
```bash
pip install -r requirements.txt
```

### Check Installed Packages
```bash
pip list
```

### Create Requirements File
```bash
pip freeze > requirements.txt
```

---

## Database Operations

### Initialize Database
```bash
python3 << 'EOF'
from app import app, db
db.create_all()
EOF
```

### Reset Database
```bash
# Remove old database
rm stratos.db  # Linux/Mac
del stratos.db # Windows

# Reinitialize
./setup.sh    # Linux/Mac
setup.bat     # Windows
```

### Add User
```bash
python3 << 'EOF'
from app import app, db
from models import User

with app.app_context():
    user = User(username='newuser', email='user@stratos.edu', role='Student')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    print("User created!")
EOF
```

### Query Users
```bash
python3 << 'EOF'
from app import app
from models import User

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"{user.username} - {user.role}")
EOF
```

---

## Useful Curl Commands

### Test Login Page
```bash
curl http://localhost:5000/login
```

### Test Login (Admin)
```bash
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=admin123"
```

### Get Admin Dashboard
```bash
curl -b cookies.txt http://localhost:5000/admin/dashboard
```

### Health Check
```bash
curl -I http://localhost:5000/
```

---

## Development Commands

### Run with Debug Mode
```bash
FLASK_APP=app.py FLASK_ENV=development python -m flask run
```

### Run on Different Port
```bash
python app.py --port 8080
```

### With Auto-Reload
```bash
FLASK_DEBUG=1 python app.py
```

### Generate Static Files
```bash
python3 << 'EOF'
from app import app
with app.app_context():
    print("App configured")
EOF
```

---

## Common Issues & Solutions

### "Address already in use"
```bash
# Linux/Mac
lsof -i :5000 | tail -1 | awk '{print $2}' | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x setup.sh run.sh
```

### "Python not found"
```bash
# Check installation
python3 --version

# Install if needed
sudo apt-get install python3  # Linux
brew install python3          # Mac
# Windows: Download from python.org
```

---

## File Locations

```
stratos-db/
├── app.py              # Main Flask app
├── config.py           # Configuration
├── models.py           # Database models
├── requirements.txt    # Dependencies
├── stratos.db          # SQLite database (auto-created)
├── setup.sh            # Setup script (Linux/Mac)
├── run.sh              # Run script (Linux/Mac)
├── setup.bat           # Setup script (Windows)
├── run.bat             # Run script (Windows)
├── Dockerfile          # Docker config
└── docker-compose.yml  # Docker compose config
```

---

## Environment Variables

### Available Variables
```bash
export FLASK_APP=app.py
export FLASK_ENV=development      # or production
export FLASK_DEBUG=1              # Enable debug mode
export SECRET_KEY=your-secret-key
export POSTGRES_URL=postgresql:// # For production with Supabase
```

### Set on Linux/Mac
```bash
export VARIABLE_NAME=value
```

### Set on Windows
```bash
set VARIABLE_NAME=value
```

---

## Deployment Checklist

- [ ] Database initialized
- [ ] All dependencies installed
- [ ] App runs on localhost:5000
- [ ] Can login as admin
- [ ] Can login as student
- [ ] Can view dashboards
- [ ] Can submit tasks
- [ ] Ready to deploy!

---

## Getting More Help

- `QUICKSTART.md` - Quick 2-minute setup
- `INSTALL.md` - Detailed installation guide
- `RUN_ON_PC.md` - Run on any PC
- `README.md` - Full documentation
- `COMMANDS.md` - This file

---

Happy coding! 🚀
