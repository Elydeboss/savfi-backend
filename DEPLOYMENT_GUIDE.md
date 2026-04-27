# 🚀 SavFi-Backend Deployment Guide

Complete guide to deploy SavFi-Backend with Supabase to production.

---

## Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Supabase account and project created
- [ ] Supabase DATABASE_URL available
- [ ] SendGrid API key (for emails)
- [ ] Domain name (optional, for custom URL)
- [ ] Hosting account (Render.com recommended)

---

## Option 1: Deploy to Render.com (Recommended)

### Step 1: Prepare Your Repository

```bash
# Ensure all changes are committed
git add .
git status  # Review changes
git commit -m "Architectural improvements and Supabase migration"
git push origin Main
```

### Step 2: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login
3. Click "New Project"
4. Configure:
   - **Name**: savfi-backend
   - **Database Password**: [Generate strong password - SAVE THIS!]
   - **Region**: Choose closest to your users
5. Wait for provisioning (~2 minutes)

### Step 3: Get Supabase Credentials

1. In Supabase dashboard, go to **Settings → Database**
2. Copy the **Connection string** (URI format):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
3. Save this for Render environment variables

### Step 4: Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click **New +** → **Web Service**
4. Connect your GitHub repository
5. Configure deployment:

   - **Name**: savfi-backend
   - **Region**: Same as Supabase (if possible)
   - **Branch**: Main
   - **Root Directory**: Leave empty
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh` (or `pip install -r requirements.txt`)
   - **Start Command**: `gunicorn finance.wsgi:application`

6. **Environment Variables** (click "Advanced" → "Add Environment Variable"):

   ```bash
   # Required
   SECRET_KEY=[generate with: python -c "import secrets; print(secrets.token_urlsafe(50))"]
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com,https://savfi-backend.onrender.com
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

   # Optional but recommended
   SENDGRID_API_KEY=[your-sendgrid-key]
   DEFAULT_FROM_EMAIL=noreply@yourdomain.com
   CORS_ALLOWED_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
   ```

7. Click **Deploy Web Service**

### Step 5: Run Database Migrations

After deployment, you need to create the tables:

**Option A**: Use Render Shell

1. Go to your deployed service on Render
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

**Option B**: Remote connection

```bash
# From your local machine
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
python manage.py migrate --database=default
```

### Step 6: Verify Deployment

1. Your API should be available at: `https://savfi-backend.onrender.com`
2. Visit:
   - `https://savfi-backend.onrender.com/swagger/` - API docs
   - `https://savfi-backend.onrender.com/redoc/` - Alternative docs
   - `https://savfi-backend.onrender.com/admin/` - Django admin

---

## Option 2: Deploy to Railway.app

### Step 1: Prepare Repository

(Same as Render)

### Step 2: Create Supabase Project

(Same as Render)

### Step 3: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your repository
4. Railway will auto-detect Django
5. **Environment Variables** (Settings → Variables):

   ```bash
   PORT=8000
   SECRET_KEY=[your-secret]
   DEBUG=False
   ALLOWED_HOSTS=.railway.app,https://savfi-backend.up.railway.app
   DATABASE_URL=[your-supabase-url]
   SENDGRID_API_KEY=[your-key]
   DEFAULT_FROM_EMAIL=noreply@yourdomain.com
   CORS_ALLOWED_ORIGINS=https://your-frontend.com
   ```

6. Add **Procfile** (if not exists):

   ```
   web: gunicorn finance.wsgi:application --bind 0.0.0.0:$PORT
   ```

7. Click **Deploy**

### Step 4: Run Migrations

(Same as Render, use Railway Shell or remote)

---

## Option 3: Deploy to Heroku

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login and Create App

```bash
heroku login
heroku create savfi-backend
```

### Step 3: Add Buildpack

```bash
heroku buildpacks:set heroku/python
```

### Step 4: Set Environment Variables

```bash
heroku config:set SECRET_KEY=[your-secret]
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=.herokuapp.com
heroku config:set DATABASE_URL=[your-supabase-url]
heroku config:set SENDGRID_API_KEY=[your-key]
heroku config:set DEFAULT_FROM_EMAIL=noreply@yourdomain.com
heroku config:set CORS_ALLOWED_ORIGINS=https://your-frontend.com
```

### Step 5: Deploy

```bash
git push heroku Main
```

### Step 6: Run Migrations

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## Frontend Connection Setup

### Step 1: Update CORS Settings

In your deployed backend, update environment variable:

```bash
CORS_ALLOWED_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
```

Or in `finance/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend.com',
    'https://www.your-frontend.com',
]
```

### Step 2: Frontend Configuration

In your frontend project:

**Create environment file** (.env):

```bash
# For React
REACT_APP_API_URL=https://savfi-backend.onrender.com

# For Vue
VUE_APP_API_URL=https://savfi-backend.onrender.com

# For Next.js
NEXT_PUBLIC_API_URL=https://savfi-backend.onrender.com
```

**API Client Example** (JavaScript):

```javascript
const API_URL = process.env.REACT_APP_API_URL;

// Login
async function login(username, password) {
  const response = await fetch(`${API_URL}/accounts/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  localStorage.setItem("access", data.access);
  localStorage.setItem("refresh", data.refresh);
  return data;
}

// Authenticated request
async function getWallets() {
  const token = localStorage.getItem("access");
  const response = await fetch(`${API_URL}/wallet/addresses/list/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.json();
}
```

---

## Production Settings Optimization

### Update JWT Token Lifetimes

For better security, reduce access token lifetime:

In `finance/settings.py`:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  # Was 7 days
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),     # Was 30 days
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}
```

### Add Production Security Settings

In `finance/settings.py`, add:

```python
# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

---

## Monitoring and Logging

### Add Error Tracking (Sentry)

```bash
# Install
pip install sentry-sdk

# In finance/settings.py:
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
)
```

---

## Database Backups

Supabase provides automatic backups:

- Go to **Database → Backups** in Supabase dashboard
- Backups run daily (on free tier)
- Can manually trigger backups anytime

---

## Custom Domain Setup (Optional)

### For Render:

1. Go to your service → Settings → Custom Domain
2. Add your domain: `api.yourdomain.com`
3. Update DNS records as instructed
4. Update ALLOWED_HOSTS to include new domain

### For Railway:

1. Settings → Domains → Add Domain
2. Configure DNS
3. Update ALLOWED_HOSTS

---

## Performance Optimization

### Enable Static File Caching

In `finance/settings.py`:

```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Add Connection Pooling

Already configured in current settings:

```python
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,  # 10 minutes
        conn_health_checks=True,
    )
}
```

---

## Troubleshooting

### Issue: Migration Fails

**Solution**: Ensure DATABASE_URL is correct and Supabase is accepting connections

### Issue: CORS Errors

**Solution**: Add your frontend domain to CORS_ALLOWED_ORIGINS

### Issue: 503 Service Unavailable

**Solution**: Check Render/Railway logs, likely missing environment variable

### Issue: 500 Internal Server Error

**Solution**: Enable DEBUG temporarily, check logs, fix issue, disable DEBUG

---

## Post-Deployment Verification

After deployment, verify:

- [ ] API documentation loads at `/swagger/`
- [ ] User registration works
- [ ] OTP verification activates account
- [ ] User can login and receive JWT tokens
- [ ] Wallet creation works
- [ ] Deposit/withdrawal operations work
- [ ] No errors in logs

---

## Cost Summary

| Service     | Free Tier            | Paid Tier  |
| ----------- | -------------------- | ---------- |
| Render.com  | 750 hours/month      | $7/month+  |
| Railway.app | $5 free credit/month | $5/month+  |
| Heroku      | No free tier         | $5/month+  |
| Supabase    | 500MB database       | $25/month+ |

**Recommended**: Render.com + Supabase = $0/month to start!

---

## Support Links

- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Supabase Documentation](https://supabase.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/5.1/howto/deployment/)
