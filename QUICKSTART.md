# Quick Start - STRATOS-DB

Get STRATOS-DB running in 2 minutes on any PC.

## For Ubuntu/Linux/Mac

```bash
# 1. Make scripts executable
chmod +x setup.sh run.sh

# 2. Setup the project (one-time)
./setup.sh

# 3. Start the app
./run.sh
```

**Then open:** http://localhost:5000

## For Windows

```bash
# 1. Setup the project (one-time)
setup.bat

# 2. Start the app
run.bat
```

**Then open:** http://localhost:5000

## Demo Credentials

### Admin Dashboard
```
Username: admin
Password: admin123
```

### Student Dashboard
```
Username: student1
Password: student123

(or student2, student3 with same password)
```

## First Time Setup

The `setup.sh` or `setup.bat` script will:
- ✓ Create Python virtual environment
- ✓ Install all dependencies
- ✓ Create SQLite database
- ✓ Add demo users and skills

**You only need to run setup ONCE.**

## Every Time You Run the App

Just use:
- **Linux/Mac:** `./run.sh`
- **Windows:** `run.bat`

## What You Can Do

1. **As Admin:**
   - Manage students
   - Create projects
   - Assign tasks
   - View analytics

2. **As Student:**
   - View assigned tasks
   - Submit task attempts
   - Track skill progress
   - View risk reports

## Stop the App

Press **CTRL+C** in the terminal

## Need Help?

See `INSTALL.md` for detailed installation guide and troubleshooting.

---

**That's it! You're ready to go.** 🚀
