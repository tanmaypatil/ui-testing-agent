# Create automation for web testing of a transaction processing application

## Technology
* **Application** - HTML, JavaScript (Vanilla JS, not Angular)
* **Backend** - Python Flask, exposes REST APIs
* **Communication** - REST APIs with JSON
* **Database** - SQLite with SQLAlchemy ORM

## Frontend
* **Login screen** - username and password fields
  - Username: `demo`
  - Password: `password`
  - Successful login redirects to payment page

* **Payment screen** - Displayed after successful login
  - Fields:
    1. Debtor (dropdown with account selection)
    2. Creditor (dropdown with account selection)
    3. Amount (numeric input)
    4. Submit button
  - Submits to `/payment` REST endpoint
  - Displays transaction ID on success

## REST API Endpoints

### POST /login
**Request:**
```json
{
  "username": "demo",
  "password": "password"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful"
}
```

### POST /payment
**Request:**
```json
{
  "debtor": "123456789",
  "creditor": "987654321",
  "amount": 150.00,
  "test_delay": 25  // OPTIONAL: For testing timeout scenarios
}
```

**Response:**
```json
{
  "status": "success",
  "transaction_id": "txn_abc123def456",
  "message": "Payment processed successfully"
}
```

**Test Parameters:**
- `test_delay` (optional): Simulates backend processing delay in seconds
  - Used for testing timeout scenarios
  - Backend will sleep for specified duration before processing
  - Example: `"test_delay": 25` causes 25-second delay

### GET /accounts
**Response:**
```json
{
  "accounts": [
    {
      "account_id": "123456789",
      "account_name": "Vernor Vinge",
      "status": "active"
    }
  ]
}
```

## Automation Testing

### Playwright Tool
- **Framework:** Pytest + Playwright (Python)
- **Browser:** Chromium (headless)
- **Tests:** End-to-end UI automation

### Test Types

#### 1. Happy Path Test (`tests/test_payment_flow.py`)
- Login with valid credentials
- Complete payment transaction
- Verify transaction ID displayed
- **Status:** ✅ Passing

#### 2. Timeout Test (`tests/test_payment_timeout.py`)
- Simulates backend delay using `test_delay` parameter
- Expected timeout: 20 seconds
- Backend delay: 25 seconds
- **Status:** ❌ Expected failure (captures diagnostics)

**Timeout Test Features:**
- Comprehensive diagnostic capture on failure:
  - Screenshots (before submit, at failure)
  - Full page HTML
  - Console logs (JavaScript errors)
  - Network traffic (HAR format - HTTP Archive standard)
  - Browser cookies
  - Element states (visibility, text content)
  - Database state (transaction records)
  - HTML report with all diagnostics

**Usage:**
```bash
# Run timeout test
pytest tests/test_payment_timeout.py -v -s

# View diagnostics after failure
open test_diagnostics/payment_timeout_<timestamp>/report.html
```

### Testing Timeout Scenarios

#### Method 1: URL Parameter (Frontend)
Navigate to payment page with delay parameter:
```
http://localhost:5001/payment.html?test_delay=25
```

The frontend JavaScript will include `test_delay` in the payment request.

#### Method 2: Direct API Call (Backend)
```python
import requests

session = requests.Session()
session.post("http://localhost:5001/login", json={"username": "demo", "password": "password"})

response = session.post(
    "http://localhost:5001/payment",
    json={
        "debtor": "123456789",
        "creditor": "987654321",
        "amount": 100.00,
        "test_delay": 25  # 25 second delay
    }
)
```

#### Method 3: Playwright Route Interception
```python
def test_with_route_delay(page):
    # Intercept payment request and delay response
    def handle_route(route):
        time.sleep(25)
        route.continue_()

    page.route("**/payment", handle_route)
    # ... rest of test
```

## Input Data

### Test Accounts (from metadata.json)
```json
{
  "accounts": [
    {
      "account_id": "123456789",
      "account_name": "Vernor Vinge",
      "created_at": "2022-01-15T10:00:00Z",
      "status": "active"
    },
    {
      "account_id": "987654321",
      "account_name": "Issac Asimov",
      "created_at": "2023-03-22T14:30:00Z",
      "status": "active"
    }
  ]
}
```

### Database Schema

**users table:**
- id (Primary Key)
- username (unique)
- password (plain text for demo)

**accounts table:**
- id (Primary Key)
- account_id (unique, business key)
- account_name
- created_at
- status

**transactions table:**
- id (Primary Key)
- transaction_id (unique, format: `txn_<12-char-uuid>`)
- debtor_account_id (Foreign Key → accounts)
- creditor_account_id (Foreign Key → accounts)
- amount (DECIMAL 10,2)
- created_at (timestamp)
- status (default: 'completed')

### Querying Database

```bash
# Connect to database
sqlite3 database/transactions.db

# View all transactions
SELECT * FROM transactions;

# View accounts
SELECT * FROM accounts;

# View recent transactions with account names
SELECT
    t.transaction_id,
    t.amount,
    d.account_name AS debtor,
    c.account_name AS creditor,
    t.created_at
FROM transactions t
JOIN accounts d ON t.debtor_account_id = d.account_id
JOIN accounts c ON t.creditor_account_id = c.account_id
ORDER BY t.created_at DESC;
```

## Test Execution

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
# Happy path test
pytest tests/test_payment_flow.py -v

# Timeout test
pytest tests/test_payment_timeout.py -v -s
```

### With Screenshots on Failure
```bash
pytest tests/ --screenshot=only-on-failure
```

### With Video Recording
```bash
pytest tests/ --video=on
```

### With Playwright Traces
```bash
pytest tests/ --tracing=on

# View trace
playwright show-trace trace.zip
```

## Diagnostic Artifacts

When tests fail, the following artifacts are captured:

| Artifact | Location | Purpose |
|----------|----------|---------|
| Screenshots | `test_diagnostics/*/before_submit.png` | Visual state before action |
| Screenshots | `test_diagnostics/*/failure_screenshot.png` | Visual state at failure |
| Page HTML | `test_diagnostics/*/page_content.html` | Full DOM for debugging |
| Console Logs | `test_diagnostics/*/console_logs.json` | JavaScript errors |
| Network HAR | `test_diagnostics/*/network.har` | HTTP Archive (standard format) |
| Cookies | `test_diagnostics/*/cookies.json` | Session state |
| Element States | `test_diagnostics/*/element_states.json` | UI component visibility |
| Database State | `test_diagnostics/*/database_state.json` | Transaction records |
| HTML Report | `test_diagnostics/*/report.html` | Human-readable summary |

## Environment Configuration

### Application
- **URL:** http://localhost:5001
- **Port:** 5001 (avoids macOS AirPlay conflict on 5000)

### Test Credentials
- **Username:** demo
- **Password:** password

### Database Location
- **Path:** `database/transactions.db`
- **Initialization:** `python backend/init_db.py`

## Future Testing Enhancements

### Planned Test Scenarios
1. ✅ Happy path (login → payment → success)
2. ✅ Timeout scenario (backend delay)
3. ⏳ Invalid login credentials
4. ⏳ Invalid account IDs
5. ⏳ Negative/zero amounts
6. ⏳ Same debtor and creditor
7. ⏳ Session expiry during payment
8. ⏳ Network interruption
9. ⏳ Database unavailable

### Autonomous Agent Testing (Future)
See `AGENT_IMPLEMENTATION_PLAN.md` for details on:
- AI-powered test agents using Claude Vision API
- Autonomous exploration of UI without pre-scripted steps
- Hybrid approach (traditional + agent tests)
- Estimated cost: $0.015 per agent test run

## Development Workflow

1. **Start Application**
   ```bash
   python backend/app.py
   ```

2. **Initialize/Reset Database**
   ```bash
   python backend/init_db.py
   ```

3. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

4. **View Test Diagnostics**
   ```bash
   open test_diagnostics/latest/report.html
   ```

## Notes

- Application uses Flask sessions (server-side) for authentication
- Transaction IDs are generated using UUID (format: `txn_<12-hex>`)
- All timestamps are in UTC
- Database file is gitignored
- Screenshots and diagnostics are auto-captured on test failures
- `test_delay` parameter should ONLY be used in test environments 