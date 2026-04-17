## ADDED Requirements

### Requirement: Initiate withdrawal with balance validation
The system SHALL allow authenticated users to initiate withdrawals from their wallets, validating sufficient balance exists before creating the withdrawal record.

#### Scenario: Successful withdrawal initiation with sufficient balance
- **WHEN** authenticated user submits POST /ledger/withdrawals/ with {wallet_id, amount, currency}
- **AND** wallet.user matches request.user
- **AND** wallet.balance >= amount
- **THEN** WithdrawalInitiated event is appended
- **AND** WithdrawalProjection is created with status "initiated"
- **AND** response returns withdrawal_id with status "initiated"

#### Scenario: Withdrawal initiation with insufficient balance
- **WHEN** authenticated user submits POST /ledger/withdrawals/ with {wallet_id, amount}
- **AND** wallet.balance < amount
- **THEN** returns 400 Bad Request with error "Insufficient balance"

#### Scenario: Initiate withdrawal from another user's wallet
- **WHEN** authenticated user submits POST /ledger/withdrawals/ with {wallet_id}
- **AND** wallet.user does not match request.user
- **THEN** returns 403 Forbidden

#### Scenario: Initiate withdrawal without authentication
- **WHEN** unauthenticated user submits POST /ledger/withdrawals/
- **THEN** returns 401 Unauthorized

#### Scenario: Withdrawal with idempotency key
- **WHEN** authenticated user submits POST /ledger/withdrawals/ with duplicate idempotency_key
- **THEN** returns original response without creating duplicate withdrawal

### Requirement: Confirm withdrawal and deduct balance
The system SHALL allow authenticated users to confirm initiated withdrawals, finalizing the transaction and deducting the amount from the wallet balance.

#### Scenario: Successfully confirm withdrawal
- **WHEN** authenticated user submits POST /ledger/withdrawals/{withdrawal_id}/confirm/
- **AND** withdrawal exists with status "initiated"
- **AND** withdrawal wallet belongs to request.user
- **THEN** WithdrawalConfirmed event is appended
- **AND** wallet balance is reduced by withdrawal amount
- **AND** withdrawal status updated to "confirmed"
- **AND** response returns withdrawal with status "confirmed"

#### Scenario: Confirm already confirmed withdrawal
- **WHEN** authenticated user submits POST /ledger/withdrawals/{withdrawal_id}/confirm/
- **AND** withdrawal status is already "confirmed"
- **THEN** returns 400 Bad Request with error "Withdrawal already confirmed"

#### Scenario: Confirm non-existent withdrawal
- **WHEN** authenticated user submits POST /ledger/withdrawals/{invalid_id}/confirm/
- **THEN** returns 404 Not Found

#### Scenario: Confirm withdrawal without authentication
- **WHEN** unauthenticated user submits POST /ledger/withdrawals/{withdrawal_id}/confirm/
- **THEN** returns 401 Unauthorized

### Requirement: Get withdrawal status
The system SHALL allow authenticated users to retrieve the current status of their withdrawals.

#### Scenario: Get own withdrawal status
- **WHEN** authenticated user submits GET /ledger/withdrawals/{withdrawal_id}/
- **AND** withdrawal wallet belongs to request.user
- **THEN** returns withdrawal projection with current status

#### Scenario: Get another user's withdrawal
- **WHEN** authenticated user submits GET /ledger/withdrawals/{withdrawal_id}/
- **AND** withdrawal wallet does not belong to request.user
- **THEN** returns 403 Forbidden
