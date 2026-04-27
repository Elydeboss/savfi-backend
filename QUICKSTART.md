# 🚀 Quick Start Guide

## For Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## For Supabase Migration

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Update .env with Supabase DATABASE_URL
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# 3. Run migrations (creates tables in Supabase)
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

## For Deployment to Render

1. Push code to GitHub
2. Go to render.com
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Use existing `render.yaml` configuration
6. Set environment variables in Render dashboard:
   - `SECRET_KEY` (generate strong key)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=.onrender.com,yourdomain.com`
   - `DATABASE_URL` (Supabase URL)
   - `SENDGRID_API_KEY`
   - `DEFAULT_FROM_EMAIL`
   - `CORS_ALLOWED_ORIGINS`

## For Connecting Frontend

1. Add your frontend URL to `CORS_ALLOWED_ORIGINS` in settings
2. Deploy backend
3. In frontend, use API endpoints with JWT authentication

## API Documentation

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- OpenAPI Schema: `http://localhost:8000/schema/`

## Migrations to Run After Deployment

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

This creates the new OTP composite index.

## Files Created/Modified

**New Files**:
- `accounts/services.py` - Service layer for business logic
- `ledger/permissions.py` - Permission decorators
- `requirements.txt` - All dependencies
- `.env.example` - Environment template
- `ARCHITECTURAL_IMPROVEMENTS.md` - Full documentation
- `QUICKSTART.md` - This file

**Modified Files**:
- `accounts/models.py` - Added composite index
- `accounts/views.py` - Fixed user activation bug
- `ledger/views.py` - Added select_related for N+1 fix
- `wallet/views.py` - Added select_related
