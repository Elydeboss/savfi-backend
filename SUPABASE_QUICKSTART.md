# 🚀 Connect to Supabase - Quick Start Guide

## Your Supabase Details

```
Host: db.dclppupcwvjppkdblsrt.supabase.co
Port: 5432
Database: postgres
User: postgres
```

---

## Step 1: Set Your Password

**IMPORTANT**: Before running anything, you need to add your Supabase password to `.env`

1. Open `.env` file in your text editor
2. Find this line:
   ```
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.dclppupcwvjppkdblsrt.supabase.co:5432/postgres
   ```
3. Replace `[YOUR-PASSWORD]` with your actual Supabase database password
4. Save the file

**Example** (if your password is "abc123xyz"):
```
DATABASE_URL=postgresql://postgres:abc123xyz@db.dclppupcwvjppkdblsrt.supabase.co:5432/postgres
```

---

## Step 2: Run the Connection Script

```bash
./connect_supabase.sh
```

This script will:
- ✅ Check your Python environment
- ✅ Install dependencies
- ✅ Test the connection
- ✅ Create migrations
- ✅ Apply migrations to Supabase
- ✅ Create admin user (optional)

---

## Step 3: Test the Connection

```bash
# Start the development server
python3 manage.py runserver
```

Then visit:
- API Docs: http://localhost:8000/swagger/
- Admin: http://localhost:8000/admin/
- API Schema: http://localhost:8000/schema/

---

## Manual Setup (If Script Fails)

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Test Connection
```bash
python3 manage.py check --database default
```

### Create Migrations
```bash
python3 manage.py makemigrations accounts
```

### Apply Migrations
```bash
python3 manage.py migrate
```

### Create Superuser
```bash
python3 manage.py createsuperuser
```

---

## Verify It Works

### In Django Shell
```bash
python3 manage.py shell
```

```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
# Should show PostgreSQL version info
```

### Check Tables in Supabase Dashboard
1. Go to https://supabase.com/dashboard
2. Select your project
3. Click "Table Editor" in left sidebar
4. You should see Django tables:
   - accounts_user
   - accounts_otp
   - ledger_event
   - ledger_walletprojection
   - etc.

---

## Troubleshooting

### Error: "could not connect to server"
**Solution**: Check your password in .env file

### Error: "database does not exist"
**Solution**: Database name should be "postgres" (already set)

### Error: "password authentication failed"
**Solution**: Verify your Supabase password in Supabase dashboard

### Migration Errors
```bash
# Reset and try again
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python3 manage.py makemigrations
python3 manage.py migrate
```

---

## What Happens Next?

### 1. Tables Created in Supabase

The following tables will be created automatically:
- ✅ `accounts_user` - User accounts
- ✅ `accounts_otp` - OTP codes
- ✅ `wallet_walletaddress` - Wallet addresses
- ✅ `ledger_event` - Event sourcing
- ✅ `ledger_walletprojection` - Wallet projections
- ✅ `ledger_depositprojection` - Deposits
- ✅ `ledger_withdrawalprojection` - Withdrawals

### 2. Performance Benefits

Your app will now have:
- ✅ Faster queries (PostgreSQL optimization)
- ✅ Better concurrency handling
- ✅ Native UUID support
- ✅ JSONB for faster JSON queries
- ✅ Automatic backups

### 3. Supabase Dashboard

Monitor your database at:
https://supabase.com/project/dclppupcwvjppkdblsrt

---

## Next Steps

1. **Test locally**:
   ```bash
   python3 manage.py runserver
   ```

2. **Create a test user**:
   - Visit http://localhost:8000/swagger/
   - Try the `/accounts/register/` endpoint
   - Verify OTP and login

3. **Deploy to production**:
   - Follow `DEPLOYMENT_GUIDE.md`
   - Update DATABASE_URL in production environment

---

## Quick Reference

| Task | Command |
|------|---------|
| Connect to Supabase | `./connect_supabase.sh` |
| Start server | `python3 manage.py runserver` |
| Create superuser | `python3 manage.py createsuperuser` |
| Run migrations | `python3 manage.py migrate` |
| Check connection | `python3 manage.py check --database default` |
| Open Django shell | `python3 manage.py shell` |

---

## Support

If you encounter issues:
1. Check `.env` file has correct password
2. Verify Supabase project is active
3. Check Supabase dashboard for any alerts
4. Review `DEPLOYMENT_GUIDE.md` for troubleshooting

---

**Your Supabase Project**: dclppupcwvjppkdblsrt
**Database Host**: db.dclppupcwvjppkdblsrt.supabase.co
**Status**: 🟢 Ready to connect!

🚀 **Run `./connect_supabase.sh` to get started!**
