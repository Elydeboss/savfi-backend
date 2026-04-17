## ADDED Requirements

### Requirement: Wallet linked to authenticated user
The system SHALL associate each WalletProjection with a User via a ForeignKey relationship, enabling authenticated access control.

#### Scenario: Create wallet with authenticated user
- **WHEN** authenticated user submits POST /ledger/wallets/ with valid data
- **THEN** WalletProjection is created with user field set to the requesting user
- **AND** response includes wallet_id with user field populated

#### Scenario: Access own wallet
- **WHEN** authenticated user requests GET /ledger/wallets/{wallet_id}/
- **AND** wallet.user matches request.user
- **THEN** returns wallet projection with 200 status

#### Scenario: Access another user's wallet
- **WHEN** authenticated user requests GET /ledger/wallets/{wallet_id}/
- **AND** wallet.user does not match request.user
- **THEN** returns 403 Forbidden

#### Scenario: Create wallet without authentication
- **WHEN** unauthenticated user submits POST /ledger/wallets/
- **THEN** returns 401 Unauthorized

### Requirement: Wallet addresses manageable by owner
The system SHALL allow wallet owners to add addresses to their wallets through authenticated endpoints.

#### Scenario: Add address to own wallet
- **WHEN** authenticated user submits POST /ledger/wallets/{wallet_id}/add-address/
- **AND** wallet.user matches request.user
- **THEN** AddressAdded event is appended
- **AND** wallet projection is updated with new address

#### Scenario: Add address to another user's wallet
- **WHEN** authenticated user submits POST /ledger/wallets/{wallet_id}/add-address/
- **AND** wallet.user does not match request.user
- **THEN** returns 403 Forbidden
