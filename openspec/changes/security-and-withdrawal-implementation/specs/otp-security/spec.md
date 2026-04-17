## MODIFIED Requirements

### Requirement: OTP rate limiting
The system SHALL enforce rate limiting on OTP-related endpoints to prevent brute-force attacks.

#### Scenario: Register throttled
- **WHEN** user submits POST /accounts/register/ more than 3 times within 1 minute
- **THEN** returns 429 Too Many Requests with throttle message

#### Scenario: Verify OTP throttled
- **WHEN** user submits POST /accounts/verify-otp/ more than 5 times within 1 minute
- **THEN** returns 429 Too Many Requests with throttle message

#### Scenario: Resend OTP throttled
- **WHEN** user submits POST /accounts/resend-otp/ more than 5 times within 1 minute
- **THEN** returns 429 Too Many Requests with throttle message
