# 🧪 Test Plan for SavFi-Backend Improvements

## Prerequisites

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

---

## Test 1: OTP Model Index Migration

**What to test**: Verify composite index was added to OTP model

```bash
# Check migration was created
python manage.py showmigrations accounts

# Expected output should show a new migration for OTP indexes
```

**Manual database check**:
```python
# In Django shell: python manage.py shell
from accounts.models import OTP
from django.db import connection

cursor = connection.cursor()
cursor.execute("""
    SELECT indexname, indexdef 
    FROM pg_indexes 
    WHERE tablename = 'accounts_otp';
""")
print(cursor.fetchall())
# Should see indexes on (user, is_used, created_at) and code
```

---

## Test 2: User Activation Bug Fix

**What to test**: Users can log in after OTP verification

**Test case**:
```bash
# Test via API
curl -X POST http://localhost:8000/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

# Note the OTP code from console/email
# Then verify:
curl -X POST http://localhost:8000/accounts/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","code":"YOUR_OTP_CODE"}'

# Now try to login (should work!)
curl -X POST http://localhost:8000/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Expected: JWT tokens returned (previously would fail with "Account not verified")
```

**Success criteria**:
- ✅ OTP verification returns "Account activated"
- ✅ Login attempt returns access/refresh tokens
- ✅ User.is_active = True in database

---

## Test 3: N+1 Query Elimination

**What to test**: Verify queries use JOIN instead of separate queries

**Enable query logging**:
```python
# Add to settings.py temporarily:
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

**Test case**:
```bash
# Create wallet and access it
curl -X POST http://localhost:8000/wallet/wallets/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"owner":"Test Owner"}'

# Check logs - should see 1 query with JOIN
# Before fix: 2 separate queries (SELECT wallet, SELECT user)
# After fix: 1 query with JOIN (SELECT wallet.* JOIN user.*)
```

**Django shell verification**:
```python
from django.db import connection
from django.test.utils import override_settings
from ledger.models import WalletProjection

@override_settings(DEBUG=True)
def test_query_count():
    # Clear query log
    connection.queries_log.clear()

    # Perform query
    wallet = WalletProjection.objects.select_related('user').first()
    _ = wallet.user  # Access related object

    # Check query count
    print(f"Queries executed: {len(connection.queries)}")
    # Expected: 1 query (with JOIN)
    # Before fix: 2 queries (without JOIN)
```

---

## Test 4: Service Layer Functionality

**What to test**: Verify OTPService works correctly

**Django shell test**:
```python
from accounts.services import OTPService
from accounts.models import User

# Test OTP generation
user = User.objects.get(username='testuser')
otp = OTPService.generate_and_send(user)
print(f"OTP created: {otp.code}, expires: {otp.expires_at}")

# Test OTP verification
success, message = OTPService.verify(user, otp.code)
print(f"Verification result: {success}, message: {message}")

# Test resend
success, message, otp = OTPService.resend('testuser')
print(f"Resend result: {success}, message: {message}")
```

**Success criteria**:
- ✅ OTPService.generate_and_send() creates OTP and sends email
- ✅ OTPService.verify() returns True and activates user
- ✅ OTPService.resend() creates new OTP

---

## Test 5: Permission Decorators

**What to test**: Verify custom permissions work

**Test case**:
```python
# Test IsWalletOwner permission
from ledger.permissions import IsWalletOwner
from rest_framework.test import APIRequestFactory
from ledger.models import WalletProjection

factory = APIRequestFactory()
request = factory.get('/api/wallets/test-uuid/')
request.user = some_user  # Set user

permission = IsWalletOwner()
wallet = WalletProjection.objects.get(wallet_id='test-uuid')
has_permission = permission.has_object_permission(request, None, wallet)

# Expected: True if wallet.user == request.user, False otherwise
```

---

## Test 6: Database Query Performance

**Benchmark before/after**:

```python
import time
from accounts.models import OTP, User

# Create test data
user = User.objects.first()
for i in range(1000):
    OTP.objects.create(user=user, code=f"{i:06d}",
                       expires_at='2099-12-31')

# Benchmark OTP lookup
start = time.time()
for _ in range(100):
    otp = OTP.objects.filter(user=user, code='000001', is_used=False).first()
end = time.time()

print(f"100 queries took: {end - start:.3f} seconds")
# After index: Should be significantly faster
```

---

## Test 7: API Endpoints

**Test all endpoints work**:

```bash
# Get API documentation
curl http://localhost:8000/swagger/
curl http://localhost:8000/redoc/

# Test authentication endpoints
curl -X POST http://localhost:8000/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user1@test.com","password":"pass123"}'

curl -X POST http://localhost:8000/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123"}'

# Test wallet endpoints (with token)
TOKEN="your-access-token"
curl -X POST http://localhost:8000/wallet/wallets/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"owner":"My Wallet"}'

curl http://localhost:8000/wallet/addresses/list/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Automated Tests

**Run Django test suite**:
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test ledger
python manage.py test wallet

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Pre-Deployment Checklist

Before deploying:
- [ ] All tests pass
- [ ] No console errors
- [ ] Database migrations applied
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Environment variables configured
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS configured
- [ ] CORS settings updated with frontend domain

---

## Smoke Test (Quick Verification)

```bash
# Quick smoke test - run in order
python manage.py check                    # ✅ No issues
python manage.py makemigrations           # ✅ "No changes detected"
python manage.py migrate                  # ✅ Migrations applied
python manage.py collectstatic --noinput  # ✅ Static files collected
python manage.py runserver                # ✅ Server starts
```

Visit `http://localhost:8000/swagger/` and verify API documentation loads.

---

## Expected Results Summary

| Test | Expected Result | How to Verify |
|------|----------------|---------------|
| User Activation | User can login after OTP | JWT tokens returned on login |
| N+1 Queries | 1 query with JOIN | Check Django query log |
| OTP Index | Fast lookup | Benchmark query time |
| Service Layer | Clean business logic | Code runs without errors |
| Permissions | Proper access control | 403 for unauthorized access |
| API Endpoints | All return 200/201 | Swagger UI works |

---

## Troubleshooting

**Migration issues**:
```bash
# Reset migrations (development only)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

**Import errors**:
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

**Database issues**:
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```
