## Why

The current codebase has critical security vulnerabilities (hardcoded secrets, debug mode enabled, no rate limiting) and missing functionality (no user-owned wallets, no withdrawal capability). These issues must be addressed before the backend can be considered production-ready.

## What Changes

### Security Fixes
- Move hardcoded `SECRET_KEY` to environment variable
- Change `DEBUG` from hardcoded `True` to environment variable with `False` default
- Add rate limiting (throttling) to OTP-related endpoints: RegisterView, VerifyOTPView, ResendOTPView
- Move `ALLOWED_HOSTS` to environment variable

### Wallet Integration
- Add `user = ForeignKey(User)` to `WalletProjection` model
- Update serializers to handle user association
- Add authentication (`IsAuthenticated`) permission to all wallet/deposit/withdrawal endpoints
- Include wallet app URLs in main URL configuration

### Withdrawal Implementation
- Add `WithdrawalProjection` model for tracking withdrawal state
- Add new event types: `WithdrawalInitiated`, `WithdrawalConfirmed`, `WithdrawalFailed`
- Add `InitiateWithdrawalView` endpoint (validates balance, creates event)
- Add `ConfirmWithdrawalView` endpoint (deducts balance, finalizes withdrawal)
- Add `GetWithdrawalView` endpoint for status retrieval

### Code Cleanup
- Register `User` and `OTP` models in accounts admin
- Consolidate duplicate OTP generation code into `accounts/utils.py`
- Register `WithdrawalProjection` in ledger admin

## Capabilities

### New Capabilities
- `wallet-user-association`: Link WalletProjection to User model for authenticated wallet access
- `withdrawals`: Two-step withdrawal API (initiate → confirm) with balance validation

### Modified Capabilities
- `otp-security`: Add rate limiting to OTP endpoints to prevent brute-force attacks (currently none)

## Impact

- **Files Modified**: 13 files across accounts, ledger, and finance apps
- **Database**: New migrations for `WalletProjection.user` field and `WithdrawalProjection` model (existing data preserved - no migration of existing records)
- **API Changes**: New endpoints for withdrawals, authentication required on wallet/deposit endpoints
- **Dependencies**: No new dependencies required
