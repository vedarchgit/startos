@echo off
REM STRATOS-DB Run Script for Windows
REM Activate virtual environment and start the Flask app

REM Check if virtual environment exists
if not exist ".venv" (
    echo Error: Virtual environment not found
    echo Run setup first: setup.bat
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if database exists
if not exist "stratos.db" (
    echo Database not found, initializing...
    python << 'PYTHON_EOF'
from app import app, db

with app.app_context():
    db.create_all()
    print("Database created")
PYTHON_EOF
)

echo.
echo ======================================
echo   STRATOS-DB is Starting
echo ======================================
echo.
echo Server running at: http://localhost:5000
echo.
echo Login Credentials:
echo   Admin:    admin / admin123
echo   Students: student1-3 / student123
echo.
echo Press CTRL+C to stop the server
echo.

REM Start the Flask app
python app.py
pause
