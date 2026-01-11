# Command Reference

Quick reference for common commands.

---

## Application Management

### Start Application
```bash
python backend/app.py
```
Access at: http://localhost:5001

### Stop Application
```
Ctrl+C
```

---

## Database Operations

### Initialize/Reset Database
```bash
python backend/init_db.py
```

### Delete Database
```bash
rm database/transactions.db
```

### View Database
```bash
sqlite3 database/transactions.db
```

Useful SQL queries:
```sql
-- View all transactions
SELECT * FROM transactions;

-- View all accounts
SELECT * FROM accounts;

-- View all users
SELECT * FROM users;

-- Count transactions
SELECT COUNT(*) FROM transactions;

-- Exit sqlite
.quit
```

---

## Testing

### Install Test Dependencies
```bash
pip install -r tests/requirements.txt
playwright install chromium
```

### Run Tests
```bash
# Basic test run
pytest tests/test_payment_flow.py -v

# With detailed output
pytest tests/test_payment_flow.py -v -s

# With visible browser
pytest tests/test_payment_flow.py --headed

# With screenshots on failure
pytest tests/test_payment_flow.py --screenshot=only-on-failure
```

---

## Port Management

### Check if Port is in Use
```bash
# macOS/Linux
lsof -i :5001

# Windows
netstat -ano | findstr :5001
```

### Kill Process on Port
```bash
# macOS/Linux
lsof -ti:5001 | xargs kill -9

# Windows (replace PID with actual process ID)
taskkill /PID <PID> /F
```

---

## Dependency Management

### Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### Install Test Dependencies
```bash
pip install -r tests/requirements.txt
```

### List Installed Packages
```bash
pip list
```

### Update Dependencies
```bash
pip install --upgrade -r backend/requirements.txt
```

---

## Git Operations

### Check Status
```bash
git status
```

### View Changes
```bash
git diff
```

### Stage All Changes
```bash
git add .
```

### Commit Changes
```bash
git commit -m "Your message here"
```

### Push to Remote
```bash
git push origin main
```

---

## API Testing with cURL

### Test Login
```bash
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"password"}' \
  -c cookies.txt
```

### Test Payment
```bash
curl -X POST http://localhost:5001/payment \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"debtor":"123456789","creditor":"987654321","amount":150.00}'
```

### Get Accounts
```bash
curl http://localhost:5001/accounts
```

---

## Logs and Debugging

### View Real-time Logs
Application logs appear in the terminal where `python backend/app.py` is running.

### Check Python Version
```bash
python --version
```

### Check pip Version
```bash
pip --version
```

### Verify Installation
```bash
python -c "import flask; print(flask.__version__)"
```

---

## File Operations

### View File Contents
```bash
# View entire file
cat backend/app.py

# View first 20 lines
head -20 backend/app.py

# View last 20 lines
tail -20 backend/app.py

# View with line numbers
cat -n backend/app.py
```

### Find Files
```bash
# Find Python files
find . -name "*.py"

# Find HTML files
find frontend -name "*.html"
```

### Search in Files
```bash
# Search for text in Python files
grep -r "def login" backend/

# Search with line numbers
grep -rn "POST /login" backend/
```

---

## Production Deployment

### Run with Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

### Run in Background
```bash
# Using nohup
nohup python backend/app.py &

# View logs
tail -f nohup.out

# Stop
ps aux | grep "python backend/app.py"
kill <PID>
```

---

## Default Credentials

| Field | Value |
|-------|-------|
| Username | `demo` |
| Password | `password` |

## Default Test Accounts

| Account ID | Name | Status |
|------------|------|--------|
| 123456789 | Vernor Vinge | active |
| 987654321 | Issac Asimov | active |

## Default URLs

| Environment | URL |
|-------------|-----|
| Development | http://localhost:5001 |
| Production | https://your-domain.com |

---

**Quick Access:**
- [Quick Start Guide](QUICKSTART.md)
- [Full Documentation](README.md)
- [Technical Overview](TECHNICAL_OVERVIEW.md)
