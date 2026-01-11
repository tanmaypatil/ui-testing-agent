# Quick Start Guide

Get the Transaction Processing Application running in under 2 minutes.

---

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Terminal/Command prompt access

---

## First Time Setup

### Step 1: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

**Expected output:**
```
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 Flask-CORS-4.0.0
```

### Step 2: Initialize Database

```bash
python backend/init_db.py
```

**Expected output:**
```
Database initialized at: /Users/tanmaypatil/ui-testing-agent/database/transactions.db
Created demo user: username='demo', password='password'
Created account: 123456789 - Vernor Vinge
Created account: 987654321 - Issac Asimov

Database populated successfully!
Total users: 1
Total accounts: 2
```

### Step 3: Start the Application

```bash
python backend/app.py
```

**Expected output:**
```
============================================================
Transaction Processing Application Started
============================================================
Access the application at: http://localhost:5001
Login credentials: username='demo', password='password'
============================================================

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.x.x:5001
```

### Step 4: Access the Application

Open your web browser and navigate to:
```
http://localhost:5001
```

You should see the login page.

---

## Using the Application

### Login

1. Enter the following credentials:
   - **Username**: `demo`
   - **Password**: `password`

2. Click the **Login** button

3. You will be redirected to the payment page

### Create a Payment

1. Select a **Debtor Account**:
   - `123456789 - Vernor Vinge` or
   - `987654321 - Issac Asimov`

2. Select a **Creditor Account**:
   - Choose a different account than the debtor

3. Enter an **Amount**:
   - Any positive number (e.g., `150.00`)

4. Click **Submit Payment**

5. You should see a success message with a transaction ID:
   ```
   Payment successful! Transaction ID: txn_abc123def456
   ```

---

## Stopping the Application

To stop the Flask server:

1. Go to the terminal where the server is running
2. Press `Ctrl+C`

**Expected output:**
```
^C
Keyboard interrupt received, exiting.
```

---

## Subsequent Runs

After the first time setup, you only need to run:

```bash
python backend/app.py
```

The database persists between runs, so you don't need to reinitialize it.

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Install dependencies
```bash
pip install -r backend/requirements.txt
```

### Problem: "No such file or directory: database/transactions.db"

**Solution:** Initialize the database
```bash
python backend/init_db.py
```

### Problem: "Address already in use" or "Port 5001 is in use"

**Solution 1:** Find and kill the existing process
```bash
# macOS/Linux
lsof -ti:5001 | xargs kill -9

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

**Solution 2:** Change the port
Edit `backend/app.py` (line 57):
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Change to any available port
```

### Problem: Port 5000 conflicts with macOS AirPlay

**Explanation:** macOS AirPlay Receiver uses port 5000 by default. This application uses port 5001 to avoid conflicts.

**Alternative:** Disable AirPlay Receiver in System Settings > General > AirDrop & Handoff > AirPlay Receiver

### Problem: "Permission denied" when running Python

**Solution:** Check Python installation
```bash
# Check Python version
python --version

# If not found, try
python3 --version

# Use python3 instead
python3 backend/app.py
```

### Problem: Database contains old test data

**Solution:** Reset the database
```bash
# Delete the old database
rm database/transactions.db

# Reinitialize
python backend/init_db.py
```

### Problem: Login fails with "Invalid credentials"

**Verification:** Ensure you're using the correct credentials:
- Username: `demo` (lowercase)
- Password: `password` (lowercase)

**Reset:** If the database was modified, reinitialize it:
```bash
python backend/init_db.py
```

---

## Running Tests

### Install Test Dependencies

```bash
pip install -r tests/requirements.txt
playwright install chromium
```

### Run Automated Tests

```bash
# Run all tests
pytest tests/test_payment_flow.py -v

# Run with detailed output
pytest tests/test_payment_flow.py -v -s

# Run with visible browser (not headless)
pytest tests/test_payment_flow.py --headed
```

**Expected output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.11.13, pytest-7.4.3, pluggy-1.6.0
collected 1 item

tests/test_payment_flow.py::test_complete_payment_flow[chromium] PASSED [100%]

============================== 1 passed in 2.09s ===============================
```

**Note:** The test automatically starts and stops the Flask server. Do not run the server manually when running tests.

---

## Directory Structure

After setup, your directory should look like this:

```
ui-testing-agent/
├── backend/
│   ├── app.py              ← Start the server with this
│   ├── init_db.py          ← Initialize database with this
│   ├── routes.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt    ← Install dependencies from this
├── frontend/
│   ├── templates/
│   │   ├── login.html
│   │   └── payment.html
│   └── static/
│       ├── css/
│       └── js/
├── tests/
│   ├── test_payment_flow.py
│   ├── conftest.py
│   └── requirements.txt
├── database/
│   └── transactions.db     ← Created after init_db.py
├── metadata.json
└── README.md
```

---

## Common Commands Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r backend/requirements.txt` |
| Initialize database | `python backend/init_db.py` |
| Start application | `python backend/app.py` |
| Stop application | Press `Ctrl+C` |
| Reset database | `rm database/transactions.db && python backend/init_db.py` |
| Run tests | `pytest tests/test_payment_flow.py -v` |
| Check if port is in use | `lsof -i :5001` (macOS/Linux) |
| View application logs | Check terminal output |

---

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Read the [TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md) for architecture details
- Explore the code in `backend/` and `frontend/` directories
- Modify `metadata.json` to add more test accounts
- Add more test cases in `tests/` directory

---

## Getting Help

If you encounter issues not covered in this guide:

1. Check the [README.md](README.md) troubleshooting section
2. Review the [TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md) for technical details
3. Check the terminal output for error messages
4. Ensure all prerequisites are installed correctly

---

## Production Deployment

This quick start is for **development only**. For production deployment:

- See the **Deployment Guide** section in [TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md)
- Use a production WSGI server (Gunicorn)
- Use PostgreSQL instead of SQLite
- Enable HTTPS
- Set secure SECRET_KEY
- Hash passwords properly

**Do NOT use the development server in production.**

---

**Last Updated:** 2026-01-11
**Version:** 1.0
