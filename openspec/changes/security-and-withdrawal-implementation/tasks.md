## 1. Security Fixes

- [x] 1.1 Create .env file with SECRET_KEY, DEBUG, ALLOWED_HOSTS, SENDGRID_API_KEY, EMAIL_HOST_USER
- [x] 1.2 Update finance/settings.py to read SECRET_KEY from os.getenv()
- [x] 1.3 Update finance/settings.py: DEBUG = os.getenv("DEBUG", False)
- [x] 1.4 Update finance/settings.py: ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
- [x] 1.5 Create OTPThrottle class (5/min) in accounts/views.py
- [x] 1.6 Create RegisterThrottle class (3/min) in accounts/views.py
- [x] 1.7 Apply throttle to RegisterView
- [x] 1.8 Apply throttle to VerifyOTPView
- [x] 1.9 Apply throttle to ResendOTPView

## 2. Wallet App Integration

- [x] 2.1 Add user = ForeignKey(User) to WalletProjection in ledger/models.py
- [x] 2.2 Run: python manage.py makemigrations ledger (no migrate of existing data)
- [x] 2.3 Update CreateWalletSerializer in ledger/serializers.py to handle user from request
- [x] 2.4 Update WalletProjectionSerializer to include user field
- [x] 2.5 Add permission_classes = [IsAuthenticated] to CreateWalletView
- [x] 2.6 Add permission_classes = [IsAuthenticated] to AddAddressView
- [x] 2.7 Add permission_classes = [IsAuthenticated] to InitiateDepositView
- [x] 2.8 Add permission_classes = [IsAuthenticated] to ConfirmDepositView
- [x] 2.9 Add permission_classes = [IsAuthenticated] to EditWalletSettingsView
- [x] 2.10 Link request.user to wallet in CreateWalletView
- [x] 2.11 Add ownership validation in AddAddressView (wallet.user == request.user)
- [x] 2.12 Add ownership validation in EditWalletSettingsView
- [x] 2.13 Include wallet URLs in finance/urls.py: path("wallet/", include("wallet.urls"))

## 3. Withdrawal Implementation

- [x] 3.1 Add WithdrawalProjection model to ledger/models.py
- [x] 3.2 Add InitiateWithdrawalSerializer to ledger/serializers.py
- [x] 3.3 Add ConfirmWithdrawalSerializer to ledger/serializers.py
- [x] 3.4 Add WithdrawalProjectionSerializer to ledger/serializers.py
- [x] 3.5 Add WithdrawalInitiated event to ledger/events.py
- [x] 3.6 Add WithdrawalConfirmed event to ledger/events.py
- [x] 3.7 Add WithdrawalFailed event to ledger/events.py
- [x] 3.8 Add _apply_withdrawal_event() handler in ledger/projections.py
- [x] 3.9 Handle WithdrawalInitiated in projections: create WithdrawalProjection, status="initiated"
- [x] 3.10 Handle WithdrawalConfirmed in projections: update status, deduct wallet balance
- [x] 3.11 Handle WithdrawalFailed in projections: update status, no balance change
- [x] 3.12 Add InitiateWithdrawalView to ledger/views.py with balance validation
- [x] 3.13 Add ConfirmWithdrawalView to ledger/views.py
- [x] 3.14 Add GetWithdrawalView to ledger/views.py
- [x] 3.15 Add withdrawal endpoints to ledger/urls.py

## 4. Code Cleanup

- [x] 4.1 Register User in accounts/admin.py
- [x] 4.2 Register OTP in accounts/admin.py
- [x] 4.3 Create accounts/utils.py with generate_otp() function
- [x] 4.4 Update accounts/serializers.py to use accounts.utils.generate_otp
- [x] 4.5 Update accounts/views.py to use accounts.utils.generate_otp
- [x] 4.6 Register WithdrawalProjection in ledger/admin.py
