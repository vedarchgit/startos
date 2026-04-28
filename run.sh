#!/bin/bash

# STRATOS-DB Run Script
# Activate virtual environment and start the Flask app

set -e

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found"
    echo "Run setup first: ./setup.sh"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if database exists
if [ ! -f "stratos.db" ]; then
    echo "⚠️  Database not found, initializing..."
    python3 << 'EOF'
from app import app, db
from models import User, Skill, RiskParam

with app.app_context():
    db.create_all()
    print("✓ Database created")
EOF
fi

echo ""
echo "======================================"
echo "  STRATOS-DB is Starting"
echo "======================================"
echo ""
echo "Server running at: http://localhost:5000"
echo ""
echo "Login Credentials:"
echo "  Admin:    admin / admin123"
echo "  Students: student1-3 / student123"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Start the Flask app
python app.py
