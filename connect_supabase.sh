#!/bin/bash

# Supabase Migration Helper for SavFi-Backend
# This script guides you through connecting to Supabase

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          🔄 SavFi-Backend → Supabase Connector                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env from .env.example first"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Check if DATABASE_URL is configured
if grep -q "YOUR-PASSWORD" .env; then
    echo "⚠️  You need to set your Supabase password first!"
    echo ""
    echo "Your Supabase connection details:"
    echo "  Host: db.dclppupcwvjppkdblsrt.supabase.co"
    echo "  Port: 5432"
    echo "  Database: postgres"
    echo "  User: postgres"
    echo ""
    echo "To set your password:"
    echo "1. Open .env file in a text editor"
    echo "2. Find the line: DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@..."
    echo "3. Replace [YOUR-PASSWORD] with your actual Supabase password"
    echo "4. Save the file"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

echo ""
echo "🔍 Step 1: Checking Python environment..."
python3 --version || (echo "❌ Python 3 not found" && exit 1)
echo "✅ Python 3 is available"
echo ""

echo "📦 Step 2: Installing dependencies..."
pip3 install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

echo "🔐 Step 3: Testing Supabase connection..."
python3 -c "
import os
import dj_database_url

# Load DATABASE_URL from .env
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv('DATABASE_URL')

if not db_url or 'YOUR-PASSWORD' in db_url:
    print('❌ DATABASE_URL not properly configured')
    print('Please update .env with your actual Supabase password')
    exit(1)

try:
    config = dj_database_url.config(default=db_url)
    print('✅ DATABASE_URL is valid')
    print(f'   Engine: {config[\"ENGINE\"]}')
    print(f'   Host: {config[\"HOST\"]}')
    print(f'   Port: {config[\"PORT\"]}')
    print(f'   Database: {config[\"NAME\"]}')
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)
" || exit 1
echo ""

echo "🔧 Step 4: Running Django system check..."
python3 manage.py check --deploy 2>&1 | head -20
echo "✅ System check complete"
echo ""

echo "🗄️  Step 5: Creating database migrations..."
python3 manage.py makemigrations accounts
echo "✅ Migrations created"
echo ""

echo "⚠️  Step 6: Applying migrations to Supabase..."
echo "This will create all tables in your Supabase database"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 manage.py migrate
    echo "✅ Migrations applied successfully!"
    echo ""
else
    echo "❌ Migration cancelled"
    exit 1
fi

echo ""
echo "👤 Step 7: Create admin user (optional)..."
read -p "Create a superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 manage.py createsuperuser
else
    echo "⏭️  Skipping superuser creation"
    echo "   You can create one later with: python3 manage.py createsuperuser"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  ✅ MIGRATION COMPLETE! ✅                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Your Django backend is now connected to Supabase!"
echo ""
echo "📊 Supabase Dashboard:"
echo "   https://supabase.com/project/dclppupcwvjppkdblsrt"
echo ""
echo "🚀 Next steps:"
echo "   1. Test locally:   python3 manage.py runserver"
echo "   2. Visit docs:     http://localhost:8000/swagger/"
echo "   3. Deploy:         Follow DEPLOYMENT_GUIDE.md"
echo ""
echo "🎉 You're ready to go!"
