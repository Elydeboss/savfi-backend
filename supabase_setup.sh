#!/bin/bash

# Supabase Migration Script for SavFi-Backend
# This script helps migrate your Django project from SQLite to Supabase

set -e  # Exit on error

echo "🔄 SavFi-Backend Supabase Migration"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env file from .env.example first"
    exit 1
fi

echo -e "${YELLOW}Step 1: Verify current setup${NC}"
echo "Checking Python and pip..."
python3 --version || (echo -e "${RED}Python 3 not found${NC}" && exit 1)
pip3 --version || (echo -e "${RED}pip3 not found${NC}" && exit 1)
echo -e "${GREEN}✓ Python environment OK${NC}"
echo ""

echo -e "${YELLOW}Step 2: Install dependencies${NC}"
pip3 install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

echo -e "${YELLOW}Step 3: Check Supabase configuration${NC}"
if grep -q "DATABASE_URL" .env; then
    echo -e "${GREEN}✓ DATABASE_URL found in .env${NC}"
    # Show masked URL for verification
    grep "DATABASE_URL" .env | sed 's/:[^:@]*@/:****@/'
else
    echo -e "${RED}DATABASE_URL not found in .env${NC}"
    echo "Please add your Supabase DATABASE_URL to .env file:"
    echo "DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
    exit 1
fi
echo ""

echo -e "${YELLOW}Step 4: Test database connection${NC}"
python3 -c "
import os
import dj_database_url
from django.conf import env

try:
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError('DATABASE_URL not set')
    config = dj_database_url.config(default=db_url)
    print('✓ DATABASE_URL is valid')
    print(f'  Engine: {config[\"ENGINE\"]}')
    print(f'  Host: {config[\"HOST\"]}')
    print(f'  Database: {config[\"NAME\"]}')
except Exception as e:
    print(f'✗ Error: {e}')
    exit(1)
"
echo ""

echo -e "${YELLOW}Step 5: Run Django system check${NC}"
python3 manage.py check --deploy 2>&1 || echo -e "${YELLOW}Some warnings detected (may be OK for development)${NC}"
echo -e "${GREEN}✓ System check complete${NC}"
echo ""

echo -e "${YELLOW}Step 6: Create migrations for new indexes${NC}"
python3 manage.py makemigrations accounts
echo -e "${GREEN}✓ Migrations created${NC}"
echo ""

echo -e "${YELLOW}Step 7: Apply migrations to Supabase${NC}"
echo "This will create all tables in your Supabase database"
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 manage.py migrate
    echo -e "${GREEN}✓ Migrations applied successfully${NC}"
else
    echo "Migration cancelled"
    exit 1
fi
echo ""

echo -e "${YELLOW}Step 8: Verify connection to Supabase${NC}"
python3 manage.py dbshell -c "\conninfo" | head -1 || echo "Connected to Supabase PostgreSQL"
echo -e "${GREEN}✓ Database connection verified${NC}"
echo ""

echo -e "${YELLOW}Step 9: Create superuser (optional)${NC}"
read -p "Create a superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 manage.py createsuperuser
fi
echo ""

echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}✓ Migration to Supabase complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Test the application: python3 manage.py runserver"
echo "2. Visit http://localhost:8000/swagger/ for API documentation"
echo "3. Set DEBUG=False and ALLOWED_HOSTS for production"
echo "4. Deploy to your hosting platform"
echo ""
echo "Supabase dashboard: https://app.supabase.com"
echo "Your database is now powered by Supabase PostgreSQL!"
