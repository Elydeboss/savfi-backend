## Context

The savfi-backend is a Django REST API using event sourcing for wallet management. Current state:

- **Security**: Hardcoded SECRET_KEY, DEBUG=True, no rate limiting on OTP endpoints
- **Wallet Model**: WalletProjection has `owner` as string field, not linked to User
- **Withdrawal**: Not implemented (only deposits exist)
- **Database**: SQLite, no existing migrations needed (new fields added)

The backend is deployed on Render with a public API.

## Goals / Non-Goals

**Goals:**
1. Fix critical security vulnerabilities (env vars, rate limiting)
2. Link wallets to authenticated users via ForeignKey
3. Implement two-step withdrawal flow with balance validation
4. Clean up duplicate code and register admin models

**Non-Goals:**
- Database migration of existing records (preserve current data)
- Switching from SQLite to another database
- Implementing on-chain blockchain withdrawals (off-chain only)
- Adding email/SMS notifications beyond existing OTP

## Decisions

### D1: Environment Variable Strategy
**Choice**: Use django-environ for all configuration
**Rationale**: Already in requirements.txt, standard Django pattern
**Alternatives**: os.environ directly (more verbose), django-environ (chosen)

### D2: Rate Limiting Implementation
**Choice**: Use DRF's built-in UserRateThrottle
**Rationale**: No new dependency, integrates with DRF
**Alternatives**: django-ratelimit (additional dep), custom middleware (more code)
**Decision**: RegisterThrottle(3/min), OTPThrottle(5/min)

### D3: Wallet-User Linking
**Choice**: Add nullable ForeignKey to WalletProjection
**Rationale**: Allows existing wallets to remain valid, new wallets linked to user
**Alternatives**: 
- Required FK - BREAKING: would fail on existing wallets
- Separate UserWallet join table - more complex, unnecessary

### D4: Withdrawal Balance Check Timing
**Choice**: Check balance in view layer before appending event
**Rationale**: Fail-fast, clear error response, simpler than handling in projections
**Alternatives**: 
- Check in projection handler - more complex error handling
- Check on confirm - wastes user time on invalid withdrawal

### D5: Withdrawal Flow (Hold vs. Deduct on Confirm)
**Choice**: Validate balance on initiation, deduct on confirmation
**Rationale**: Simpler than implementing hold system, user can't spend balance during initiated state anyway
**Alternatives**: Hold funds on initiation - requires additional "available_balance" field

### D6: No Database Migration of Existing Records
**Choice**: Use nullable fields, migrations create new tables without moving data
**Rationale**: User explicitly requested no migration of existing data
**Implication**: Some existing wallets won't have user association (can be backfilled manually if needed)

## Risks / Trade-offs

**[Risk: Race condition on concurrent withdrawals]**
→ Mitigation: Use `select_for_update()` in views when checking balance
→ Alternative: Use expected_version from wallet event (future enhancement)

**[Risk: Wallet ownership check missing]**
→ Mitigation: Add ownership validation: `if wallet.user != request.user: return 403`
→ Must implement in Phase 2 wallet integration

**[Risk: Hardcoded production values in .env.example]**
→ Mitigation: Create .env file with placeholder values, add .env to .gitignore

**[Risk: Test coverage gaps]**
→ Mitigation: Add integration tests for withdrawal flow and rate limiting

## Migration Plan

1. **Phase 1** (1-2 days): Security fixes
   - Create .env, update settings.py
   - Add throttling classes
   - Test locally with DEBUG=False

2. **Phase 2** (1-2 days): Wallet integration
   - Add migration for user FK (nullable)
   - Update serializers/views
   - Include wallet URLs

3. **Phase 3** (2-3 days): Withdrawal implementation
   - Add models (no migration for existing data)
   - Add events, projections, views, URLs
   - Test two-step flow

4. **Phase 4** (0.5 day): Cleanup
   - Register admin models
   - Consolidate OTP utils

**Rollback**: Each phase is independent. Revert git commit to roll back any phase.

## Open Questions

1. **Q: Should we backfill user association for existing wallets?**
   - Currently: New wallets linked, existing wallets have user=null
   - Alternative: Run one-time script to link by owner string matching username
   
2. **Q: What happens if user deletes account?**
   - Currently: CASCADE deletes wallets
   - Alternative: SET_NULL with handling in views (future)

3. **Q: Rate limit counts - per user or per IP?**
   - Currently: UserRateThrottle (per user, requires auth)
   - Consider: IP-based for unauthenticated (register, verify-otp)
