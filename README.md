# 🛠️ Savfi Backend – Django + Web3 Hybrid Savings Infrastructure

Savfi Backend powers the Web2 + Web3 hybrid savings system.  
It combines **Django REST Framework** (off-chain logic, authentication, savings workflow) with **Web3.py** and an **Ethereum Smart Contract** deployed via Remix.

This backend manages user accounts, savings events, wallet interactions, and Web3 contract calls.

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#1️⃣-prerequisites)
  - [Installation](#2️⃣-installation)
- [Environment Variables](#-environment-variables)
- [Smart Contract Integration](#-smart-contract-integration)
- [API Endpoints](#-api-endpoints)
- [Running Tests](#-running-tests)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ⚙️ Overview

The backend manages:

- User authentication (JWT or session)
- Off-chain savings workflows (deposit events, withdrawal logs, histories)
- Connection to an Ethereum smart contract
- Hybrid savings calculations (Django + Smart Contract)
- Secure API endpoints for frontend and mobile clients

---

## ✨ Features

- 🔐 User registration & authentication  
- 🧾 Track deposits/withdrawals off-chain  
- 🔗 Interact with Solidity smart contracts via Web3.py  
- 🧮 Hybrid savings logic  
- 🧱 Django REST Framework APIs  
- 🌐 Supports Ethereum testnets (Sepolia/Holesky)  

---

## 🧱 Tech Stack

### **Backend**
- Django 4+
- Django REST Framework
- Web3.py
- PostgreSQL / SQLite

### **Blockchain**
- Solidity
- Remix.ethereum.org
- MetaMask / Testnet RPC

---

## 📂 Project Structure

savfi-backend/
│
├── savfi/ # Main project folder
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│
├── savings/ # Savings app
│ ├── models.py # Deposit / withdrawal models
│ ├── views.py # API views
│ ├── serializers.py
│ ├── services.py # Web3.py + business logic
│
├── accounts/ # User authentication app
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│
├── contracts/
│ ├── SavfiSavings.json # Contract ABI
│ └── address.txt # Contract address
│
├── requirements.txt
├── manage.py
└── .env.example


---

## 🚀 Getting Started

### 1️⃣ Prerequisites

Ensure you have:

- Python 3.10+
- pip
- virtualenv
- PostgreSQL (optional; SQLite works for development)
- MetaMask wallet + testnet RPC (Infura/Alchemy)

---

### 2️⃣ Installation

```bash
git clone https://github.com/your-username/savfi-backend.git
cd savfi-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

SECRET_KEY=your-secret-key
DEBUG=True

# Database (PostgreSQL recommended for production)
DB_NAME=savfi
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Web3
WEB3_PROVIDER=https://sepolia.infura.io/v3/YOUR_RPC_KEY
CONTRACT_ADDRESS=0xYourContractAddress
CONTRACT_ABI_PATH=contracts/SavfiSavings.json

---

📘 API Endpoints
Authentication
Method	Endpoint	Description
POST	/api/auth/register	Register new user
POST	/api/auth/login	Login and get token
Savings
Method	Endpoint	Description
POST	/api/savings/deposit	Create a deposit (off-chain + triggers on-chain)
GET	/api/savings/balance	Get user's hybrid balance
GET	/api/savings/history	Full savings & transaction history
Smart Contract
Method	Endpoint	Description
POST	/api/smart/trigger	Trigger any smart contract function

---

🚢 Deployment
You can deploy on:

Render

Railway

Heroku

Docker / AWS ECS

Example Gunicorn command:

nginx
Copy code
gunicorn savfi.wsgi --bind 0.0.0.0:8000
🤝 Contributing
Fork the repository

Create a new branch

Commit your changes

Submit a PR



