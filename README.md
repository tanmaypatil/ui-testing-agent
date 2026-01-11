# Transaction Processing Application with Automation Testing

A complete web application for transaction processing with automated Playwright testing.

## 🚀 Quick Start

**New to this project?** See [QUICKSTART.md](QUICKSTART.md) for a step-by-step guide to get running in under 2 minutes.

**TL;DR:**
```bash
pip install -r backend/requirements.txt
python backend/init_db.py
python backend/app.py
# Open http://localhost:5001
```

## Overview

This project includes:
- **Backend**: Flask-based REST API (Python)
- **Frontend**: HTML/JavaScript web interface
- **Database**: SQLite for data persistence
- **Automation**: Playwright end-to-end tests

## Project Structure

```
ui-testing-agent/
├── backend/              # Flask application
│   ├── app.py           # Main entry point
│   ├── routes.py        # API endpoints
│   ├── models.py        # Database models
│   ├── database.py      # Database setup
│   ├── init_db.py       # Database initialization script
│   └── requirements.txt # Python dependencies
├── frontend/            # Web interface
│   ├── templates/       # HTML pages
│   └── static/          # CSS and JavaScript
├── tests/               # Playwright automation tests
│   ├── test_payment_flow.py
│   ├── conftest.py
│   └── requirements.txt
├── database/            # SQLite database files
└── metadata.json        # Test data
```

## Features

### Backend APIs
- **POST /login** - User authentication
- **POST /payment** - Process payment transactions
- **GET /accounts** - List all accounts

### Frontend Pages
- **Login Page** - User authentication with username/password
- **Payment Page** - Transaction form (debtor, creditor, amount)

### Test Data
- Demo user: `username=demo`, `password=password`
- Accounts:
  - Account 1: `123456789` (Vernor Vinge)
  - Account 2: `987654321` (Issac Asimov)

## Setup Instructions

### 1. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 2. Initialize Database

```bash
python backend/init_db.py
```

This will:
- Create the SQLite database
- Load accounts from `metadata.json`
- Create the demo user

### 3. Run the Application

```bash
python backend/app.py
```

The application will be available at: http://localhost:5001

### 4. Manual Testing

1. Open your browser to http://localhost:5001
2. Login with credentials:
   - Username: `demo`
   - Password: `password`
3. Fill out the payment form:
   - Select debtor account
   - Select creditor account
   - Enter amount
4. Submit and verify transaction ID is displayed

## Automated Testing

### Install Test Dependencies

```bash
pip install -r tests/requirements.txt
playwright install chromium
```

### Run Tests

```bash
# Run all tests
pytest tests/test_payment_flow.py -v

# Run with verbose output
pytest tests/test_payment_flow.py -v -s

# Run with screenshots on failure
pytest tests/test_payment_flow.py --screenshot=only-on-failure
```

### Test Coverage

The automated test (`test_payment_flow.py`) covers:
1. Navigate to login page
2. Enter credentials (demo/password)
3. Click login button
4. Verify redirect to payment page
5. Fill payment form (debtor, creditor, amount)
6. Submit payment
7. Verify success message with transaction ID

## API Documentation

### Login Endpoint

**POST** `/login`

Request:
```json
{
  "username": "demo",
  "password": "password"
}
```

Response:
```json
{
  "status": "success",
  "message": "Login successful"
}
```

### Payment Endpoint

**POST** `/payment`

Request:
```json
{
  "debtor": "123456789",
  "creditor": "987654321",
  "amount": 150.00
}
```

Response:
```json
{
  "status": "success",
  "transaction_id": "txn_abc123def456",
  "message": "Payment processed successfully"
}
```

## Development

### Adding New Accounts

Edit `metadata.json` and run:
```bash
python backend/init_db.py
```

### Modifying the Database Schema

1. Update `backend/models.py`
2. Reinitialize the database: `python backend/init_db.py`

### Adding More Tests

Create new test files in the `tests/` directory following the pattern in `test_payment_flow.py`.

## Troubleshooting

### Port 5000 Already in Use

The application runs on port 5001 to avoid conflicts with macOS AirPlay Receiver. To use a different port, modify `backend/app.py` and `tests/conftest.py`.

### Database Issues

Delete the database and reinitialize:
```bash
rm database/transactions.db
python backend/init_db.py
```

### Test Failures

Ensure the Flask server is not running manually when executing tests. The test suite starts its own server automatically.

## License

See LICENSE file for details.
