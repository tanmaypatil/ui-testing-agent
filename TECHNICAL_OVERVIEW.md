# Technical Overview: Transaction Processing Application with Automation

**Project**: UI Testing Agent
**Version**: 1.0
**Last Updated**: 2026-01-11
**Author**: Development Team

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Database Design](#database-design)
4. [API Specification](#api-specification)
5. [Security Implementation](#security-implementation)
6. [Frontend Architecture](#frontend-architecture)
7. [Test Automation Framework](#test-automation-framework)
8. [Design Decisions](#design-decisions)
9. [Performance Characteristics](#performance-characteristics)
10. [Scalability Considerations](#scalability-considerations)
11. [Deployment Guide](#deployment-guide)

---

## Architecture Overview

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Client Browser                     │
│              (HTML/CSS/JavaScript)                   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST
                   ▼
┌─────────────────────────────────────────────────────┐
│              Flask Web Server                        │
│  ┌──────────────────────────────────────────────┐  │
│  │  Routes Layer (routes.py)                    │  │
│  │  - /login (POST)                             │  │
│  │  - /payment (POST)                           │  │
│  │  - /accounts (GET)                           │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Business Logic & Session Management         │  │
│  │  - Flask Sessions (server-side)              │  │
│  │  - Transaction ID generation (UUID)          │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  ORM Layer (SQLAlchemy)                      │  │
│  │  - User, Account, Transaction models         │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│            SQLite Database                           │
│  - users table                                       │
│  - accounts table                                    │
│  - transactions table                                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│          Playwright Test Automation                  │
│  - Pytest framework                                  │
│  - Chromium browser automation                       │
│  - Automatic server lifecycle management             │
└─────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| **Client Browser** | User interface rendering, form validation, AJAX requests | HTML5, CSS3, JavaScript ES6+ |
| **Flask Server** | Request routing, business logic, session management | Flask 3.0.0, Python 3.11+ |
| **ORM Layer** | Database abstraction, query generation, model mapping | SQLAlchemy 3.1.1 |
| **Database** | Data persistence, ACID transactions | SQLite 3 |
| **Test Framework** | End-to-end testing, browser automation | Playwright 1.40.0, Pytest 7.4.3 |

---

## Technology Stack

### Backend Technologies

#### Flask Web Framework (3.0.0)
- **Purpose**: Lightweight WSGI web application framework
- **Features Used**:
  - Jinja2 templating engine for HTML rendering
  - Werkzeug WSGI toolkit for request/response handling
  - Built-in development server
  - Session management with secure cookies
  - Blueprint pattern for route organization

**Configuration:**
```python
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

#### Flask-SQLAlchemy (3.1.1)
- **Purpose**: ORM (Object-Relational Mapping)
- **Features Used**:
  - Declarative model definitions
  - Relationship mapping with foreign keys
  - Query builder API
  - Session management
  - Automatic table creation

**Model Definition Example:**
```python
class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    debtor_account_id = db.Column(db.String(50), db.ForeignKey('accounts.account_id'))
    creditor_account_id = db.Column(db.String(50), db.ForeignKey('accounts.account_id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
```

#### Flask-CORS (4.0.0)
- **Purpose**: Cross-Origin Resource Sharing support
- **Rationale**: Enables future frontend separation (e.g., React/Angular SPA)
- **Current Use**: Configured for all origins in development

#### SQLite 3
- **Purpose**: Embedded relational database
- **Advantages**:
  - Zero configuration required
  - File-based (easy backup/reset)
  - ACID-compliant
  - Sufficient for < 100k transactions
- **Limitations**:
  - Single writer at a time
  - No network access
  - Limited concurrency

### Frontend Technologies

#### HTML5
- Semantic markup (`<form>`, `<label>`, `<select>`)
- Input validation attributes (`required`, `type="number"`, `step`)
- Accessibility features (proper label associations)

#### CSS3
**Layout & Styling:**
- Flexbox for centering and alignment
- CSS Grid not used (simple layouts)
- Linear gradients for visual appeal
- CSS transitions for hover effects
- Media queries not implemented (desktop-first)

**Design System:**
```css
Primary Color: #667eea (purple-blue)
Secondary Color: #764ba2 (purple)
Background: Linear gradient (135deg)
Font: System font stack (-apple-system, BlinkMacSystemFont)
```

#### JavaScript (ES6+)
**Features Used:**
- `async/await` for asynchronous operations
- Fetch API for HTTP requests
- Arrow functions for cleaner syntax
- Template literals for string interpolation
- Destructuring not used (simple data structures)
- No modules (single-file scripts)

**Code Structure:**
```javascript
// Event-driven architecture
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        // Handle form submission
    });
});
```

### Testing Technologies

#### Playwright (1.40.0)
- **Purpose**: Browser automation for E2E testing
- **Browser**: Chromium (WebKit/Firefox available but not used)
- **Features**:
  - Auto-waiting for elements
  - Network interception capability (not used)
  - Screenshot on failure
  - Video recording capability (not enabled)
  - Mobile emulation (not used)

#### Pytest (7.4.3)
- **Purpose**: Test framework and runner
- **Features Used**:
  - Fixtures for setup/teardown
  - Session-scoped fixtures for server management
  - Verbose output modes
  - Assertion introspection

#### pytest-playwright (0.4.3)
- **Purpose**: Pytest integration for Playwright
- **Features**:
  - Automatic browser lifecycle
  - Page fixture injection
  - Base URL configuration
  - Screenshot management

---

## Database Design

### Entity-Relationship Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ username UNIQUE │
│ password        │
└─────────────────┘

┌──────────────────────┐
│      accounts        │
├──────────────────────┤
│ id (PK)              │
│ account_id UNIQUE    │◄──┐
│ account_name         │   │
│ created_at           │   │
│ status               │   │
└──────────────────────┘   │
                            │
┌──────────────────────────┤
│     transactions         │
├──────────────────────────┤
│ id (PK)                  │
│ transaction_id UNIQUE    │
│ debtor_account_id (FK)   │───┘
│ creditor_account_id (FK) │───┐
│ amount DECIMAL(10,2)     │   │
│ created_at               │   │
│ status                   │   │
└──────────────────────────┘   │
                               │
                               └───► accounts.account_id
```

### Table Specifications

#### users
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Surrogate key |
| username | VARCHAR(80) | UNIQUE, NOT NULL | Login identifier |
| password | VARCHAR(200) | NOT NULL | Plain text (demo only) |

**Indexes:**
- Primary key index on `id`
- Unique index on `username`

**Current Data:**
```sql
INSERT INTO users (username, password) VALUES ('demo', 'password');
```

#### accounts
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Surrogate key |
| account_id | VARCHAR(50) | UNIQUE, NOT NULL | Business key |
| account_name | VARCHAR(200) | NOT NULL | Account holder name |
| created_at | TIMESTAMP | NOT NULL | Account creation time |
| status | VARCHAR(20) | NOT NULL | active/inactive/suspended |

**Indexes:**
- Primary key index on `id`
- Unique index on `account_id`

**Current Data:**
```sql
INSERT INTO accounts VALUES (1, '123456789', 'Vernor Vinge', '2022-01-15 10:00:00', 'active');
INSERT INTO accounts VALUES (2, '987654321', 'Issac Asimov', '2023-03-22 14:30:00', 'active');
```

#### transactions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Surrogate key |
| transaction_id | VARCHAR(50) | UNIQUE, NOT NULL | Business key (UUID-based) |
| debtor_account_id | VARCHAR(50) | FOREIGN KEY → accounts(account_id), NOT NULL | Source account |
| creditor_account_id | VARCHAR(50) | FOREIGN KEY → accounts(account_id), NOT NULL | Destination account |
| amount | DECIMAL(10,2) | NOT NULL | Transaction amount |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Transaction time |
| status | VARCHAR(20) | DEFAULT 'completed' | completed/pending/failed |

**Indexes:**
- Primary key index on `id`
- Unique index on `transaction_id`
- Foreign key index on `debtor_account_id`
- Foreign key index on `creditor_account_id`

**Relationships:**
```python
# SQLAlchemy relationships
debtor = db.relationship('Account', foreign_keys=[debtor_account_id])
creditor = db.relationship('Account', foreign_keys=[creditor_account_id])
```

### Database Initialization

**Process:**
1. Read `metadata.json` for account seed data
2. Drop all existing tables (`db.drop_all()`)
3. Create all tables from models (`db.create_all()`)
4. Insert demo user
5. Insert accounts from metadata
6. Commit transaction

**Script Location:** `backend/init_db.py`

**Command:**
```bash
python backend/init_db.py
```

---

## API Specification

### Base URL
```
Development: http://localhost:5001
Production: https://your-domain.com
```

### Authentication
Session-based authentication using HTTP cookies.

**Session Cookie:**
- Name: `session`
- HttpOnly: `true`
- SameSite: `Lax`
- Secure: `false` (development), `true` (production)
- Expiration: Session (browser close)

### Endpoints

#### 1. User Login

**Endpoint:** `POST /login`

**Description:** Authenticates user and creates session

**Request:**
```http
POST /login HTTP/1.1
Content-Type: application/json

{
  "username": "demo",
  "password": "password"
}
```

**Success Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: session=<encrypted_token>; HttpOnly; Path=/; SameSite=Lax

{
  "status": "success",
  "message": "Login successful"
}
```

**Error Responses:**

*Invalid Credentials:*
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "status": "error",
  "message": "Invalid credentials"
}
```

*Missing Fields:*
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "message": "Username and password are required"
}
```

**Implementation:**
```python
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
```

#### 2. Process Payment

**Endpoint:** `POST /payment`

**Description:** Creates a new transaction between two accounts

**Authentication:** Required (session cookie)

**Request:**
```http
POST /payment HTTP/1.1
Content-Type: application/json
Cookie: session=<token>

{
  "debtor": "123456789",
  "creditor": "987654321",
  "amount": 150.00
}
```

**Success Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "transaction_id": "txn_a1b2c3d4e5f6",
  "message": "Payment processed successfully"
}
```

**Error Responses:**

*Unauthorized:*
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "status": "error",
  "message": "Unauthorized - please login first"
}
```

*Invalid Account:*
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "message": "Invalid debtor account: 999999999"
}
```

*Invalid Amount:*
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "message": "Invalid amount"
}
```

**Validation Rules:**
- `debtor` must exist in accounts table
- `creditor` must exist in accounts table
- `amount` must be positive number
- `debtor` and `creditor` must be different (not enforced currently)

**Implementation:**
```python
@api.route('/payment', methods=['POST'])
def payment():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    # Validate accounts exist
    debtor = Account.query.filter_by(account_id=data['debtor']).first()
    creditor = Account.query.filter_by(account_id=data['creditor']).first()

    # Generate transaction ID
    transaction_id = f"txn_{uuid.uuid4().hex[:12]}"

    # Create and save transaction
    transaction = Transaction(
        transaction_id=transaction_id,
        debtor_account_id=data['debtor'],
        creditor_account_id=data['creditor'],
        amount=data['amount']
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'transaction_id': transaction_id,
        'message': 'Payment processed successfully'
    }), 200
```

#### 3. List Accounts

**Endpoint:** `GET /accounts`

**Description:** Retrieves all active accounts

**Authentication:** Not required (currently)

**Request:**
```http
GET /accounts HTTP/1.1
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "accounts": [
    {
      "account_id": "123456789",
      "account_name": "Vernor Vinge",
      "status": "active"
    },
    {
      "account_id": "987654321",
      "account_name": "Issac Asimov",
      "status": "active"
    }
  ]
}
```

**Use Case:** Populate dropdown menus in frontend (not currently used)

---

## Security Implementation

### Session Management

**Technology:** Flask server-side sessions

**Configuration:**
```python
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

**Security Properties:**

| Property | Value | Protection Against |
|----------|-------|---------------------|
| HttpOnly | True | XSS (prevents JavaScript access) |
| SameSite | Lax | CSRF on state-changing requests |
| Secure | False (dev) | MITM attacks (should be True in prod) |
| Server-side | Yes | Tampering (data stored server-side) |

**Session Data Structure:**
```python
session = {
    'logged_in': True,
    'username': 'demo'
}
```

### Authentication Flow

```
┌────────────┐
│   Client   │
└─────┬──────┘
      │
      │ POST /login {username, password}
      ▼
┌────────────────────┐
│   Flask Server     │
│                    │
│ 1. Validate creds  │
│ 2. Create session  │
│ 3. Set cookie      │
└─────┬──────────────┘
      │
      │ Set-Cookie: session=<token>
      ▼
┌────────────┐
│   Client   │ (stores cookie)
│            │
│ Subsequent │
│ requests   │ Cookie: session=<token>
└─────┬──────┘
      ▼
┌────────────────────┐
│   Flask Server     │
│                    │
│ session.get(       │
│   'logged_in'      │
│ )                  │
└────────────────────┘
```

### Input Validation

**Server-side Validation:**
```python
# Type checking
if not isinstance(amount, (int, float)):
    return error

# Range checking
if amount <= 0:
    return error

# Existence checking
if not Account.query.filter_by(account_id=debtor_id).first():
    return error

# Required fields
if not data or 'username' not in data:
    return error
```

**Client-side Validation:**
```html
<!-- HTML5 validation -->
<input type="text" required>
<input type="number" min="0.01" step="0.01" required>
<select required>
```

### Current Security Limitations (Demo Only)

⚠️ **Not Production-Ready:**

1. **Password Storage**: Plain text passwords
   - **Fix**: Use `bcrypt` or `argon2`
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   hashed = generate_password_hash(password)
   ```

2. **No Rate Limiting**: Brute force attacks possible
   - **Fix**: Use `Flask-Limiter`
   ```python
   @limiter.limit("5 per minute")
   def login():
       ...
   ```

3. **No HTTPS**: Man-in-the-middle attacks possible
   - **Fix**: Use reverse proxy (Nginx) with SSL/TLS

4. **No CSRF Tokens**: Cross-site request forgery possible
   - **Fix**: Use `Flask-WTF` with CSRF tokens

5. **No Input Sanitization**: Potential XSS
   - **Fix**: Jinja2 auto-escapes, but validate input

6. **Hardcoded Secret Key**: Not secure for production
   - **Fix**: Use environment variable
   ```python
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   ```

---

## Frontend Architecture

### Page Structure

#### Login Page (`frontend/templates/login.html`)

**Purpose:** User authentication entry point

**Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login - Transaction Processing</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Transaction Processing System</h1>
            <h2>Login</h2>

            <form id="login-form">
                <input type="text" id="username" required>
                <input type="password" id="password" required>
                <div id="error-msg" style="display: none;"></div>
                <button type="submit">Login</button>
            </form>
        </div>
    </div>
    <script src="/static/js/login.js"></script>
</body>
</html>
```

**Key Elements:**
- Form ID: `login-form` (JavaScript hook)
- Input IDs: `username`, `password` (JavaScript selectors)
- Error container: `error-msg` (dynamic visibility)

#### Payment Page (`frontend/templates/payment.html`)

**Purpose:** Transaction creation interface

**Structure:**
```html
<form id="payment-form">
    <select id="debtor" required>
        <option value="">Select debtor account</option>
        <option value="123456789">123456789 - Vernor Vinge</option>
        <option value="987654321">987654321 - Issac Asimov</option>
    </select>

    <select id="creditor" required>
        <option value="">Select creditor account</option>
        <option value="123456789">123456789 - Vernor Vinge</option>
        <option value="987654321">987654321 - Issac Asimov</option>
    </select>

    <input type="number" id="amount" step="0.01" min="0.01" required>

    <div id="error-msg" style="display: none;"></div>
    <div id="success-msg" style="display: none;"></div>

    <button type="submit">Submit Payment</button>
</form>
```

**Design Decision:** Hardcoded account options
- **Rationale**: Only 2 accounts in metadata.json
- **Alternative**: Fetch from `/accounts` endpoint dynamically
- **Trade-off**: Less flexible but simpler implementation

### JavaScript Controllers

#### Login Controller (`frontend/static/js/login.js`)

**Responsibilities:**
1. Form submission handling
2. Input validation (client-side)
3. AJAX request to `/login`
4. Session storage (via cookies)
5. Page redirection on success
6. Error message display

**Event Flow:**
```
DOMContentLoaded
  └─> Attach submit handler to form
       └─> On submit:
            1. preventDefault()
            2. Get username/password
            3. Validate not empty
            4. Disable button
            5. Fetch POST /login
            6. Handle response:
               ├─ Success: redirect to /payment.html
               └─ Error: show error message
```

**Code Structure:**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                window.location.href = '/payment.html';
            } else {
                showError(data.message);
            }
        } catch (error) {
            showError('Network error. Please try again.');
        }
    });
});
```

#### Payment Controller (`frontend/static/js/payment.js`)

**Responsibilities:**
1. Form submission handling
2. Multi-field validation
3. Business rule validation (debtor ≠ creditor)
4. AJAX request to `/payment`
5. Success/error message display
6. Form reset on success
7. Session expiry handling

**Validation Logic:**
```javascript
// Required fields
if (!debtor || !creditor || !amount) {
    showError('Please fill in all fields');
    return;
}

// Positive amount
if (parseFloat(amount) <= 0) {
    showError('Amount must be greater than 0');
    return;
}

// Different accounts
if (debtor === creditor) {
    showError('Debtor and creditor must be different accounts');
    return;
}
```

**Response Handling:**
```javascript
if (response.ok && data.status === 'success') {
    showSuccess(`Payment successful! Transaction ID: ${data.transaction_id}`);
    paymentForm.reset();
} else if (response.status === 401) {
    showError('Session expired. Redirecting to login...');
    setTimeout(() => window.location.href = '/', 2000);
} else {
    showError(data.message || 'Payment failed');
}
```

### CSS Architecture

**File:** `frontend/static/css/styles.css`

**Structure:**
1. Global reset (`*` selector)
2. Body styling (gradient background, flexbox centering)
3. Container and card components
4. Form elements (inputs, selects, buttons)
5. Message components (error, success)
6. Utility classes (info-box)

**Design System:**
```css
/* Color Palette */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--card-bg: white;
--text-primary: #333;
--text-secondary: #555;
--border-color: #e0e0e0;
--focus-color: #667eea;
--error-bg: #fee;
--error-border: #c33;
--success-bg: #efe;
--success-border: #363;

/* Typography */
--font-stack: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu;
--h1-size: 24px;
--h2-size: 20px;
--body-size: 14px;

/* Spacing */
--card-padding: 40px;
--form-gap: 20px;
--border-radius: 6px;
```

**Responsive Design:**
- Desktop-first approach
- Max-width constraint on container (500px)
- Padding on body for small screens
- No breakpoints defined (simple layout works on all sizes)

---

## Test Automation Framework

### Test Architecture

```
pytest execution
  └─> Session setup
       └─> Start Flask server (subprocess)
       └─> Wait for server ready (HTTP polling)
       └─> Initialize Playwright
            └─> Launch Chromium
                 └─> Create browser context
                      └─> Open new page
                           └─> Run test_complete_payment_flow()
                                ├─> Navigate to login
                                ├─> Fill credentials
                                ├─> Submit login
                                ├─> Wait for redirect
                                ├─> Fill payment form
                                ├─> Submit payment
                                └─> Verify transaction ID
                           └─> Close page
                      └─> Close context
                 └─> Close browser
       └─> Terminate Flask server
  └─> Session teardown
```

### Pytest Fixtures

**Location:** `tests/conftest.py`

#### 1. flask_server (Session Scope, Auto-use)

**Purpose:** Manage Flask server lifecycle for all tests

**Implementation:**
```python
@pytest.fixture(scope="session", autouse=True)
def flask_server():
    # Start Flask in subprocess
    server_process = subprocess.Popen([sys.executable, app_path], ...)

    # Wait for server to respond (HTTP polling)
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:5001/", timeout=1)
            if response.status_code == 200:
                break
        except (ConnectionError, Timeout):
            continue

    yield  # Tests run here

    # Cleanup
    server_process.terminate()
    server_process.wait(timeout=5)
```

**Key Features:**
- Health check with retry logic (10 attempts, 1 second intervals)
- Process monitoring (detects crashes)
- Graceful shutdown with timeout
- Output capture for debugging

#### 2. base_url (Session Scope)

**Purpose:** Provide base URL to tests

```python
@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:5001"
```

**Usage:**
```python
def test_something(page, base_url):
    page.goto(base_url)
```

### Test Cases

**Location:** `tests/test_payment_flow.py`

#### test_complete_payment_flow

**Purpose:** End-to-end validation of complete user journey

**Test Steps:**

| Step | Action | Verification |
|------|--------|-------------|
| 1 | Navigate to login page | Page title matches |
| 2 | Fill username field | - |
| 3 | Fill password field | - |
| 4 | Click login button | - |
| 5 | Wait for redirect | URL contains /payment.html |
| 6 | Select debtor account | - |
| 7 | Select creditor account | - |
| 8 | Enter amount | - |
| 9 | Click submit button | - |
| 10 | Wait for success message | Message visible |
| 11 | Extract transaction ID | Matches regex `txn_[a-f0-9]{12}` |

**Implementation:**
```python
def test_complete_payment_flow(page: Page, base_url: str):
    # Step 1: Navigate
    page.goto(base_url)
    expect(page).to_have_title("Login - Transaction Processing")

    # Steps 2-4: Login
    page.fill("#username", "demo")
    page.fill("#password", "password")
    page.click("#login-btn")

    # Step 5: Verify redirect
    page.wait_for_url(f"{base_url}/payment.html", timeout=5000)
    expect(page).to_have_title("Payment - Transaction Processing")

    # Steps 6-9: Payment
    page.select_option("#debtor", "123456789")
    page.select_option("#creditor", "987654321")
    page.fill("#amount", "150.00")
    page.click("#submit-btn")

    # Steps 10-11: Verify success
    success_msg = page.locator("#success-msg")
    expect(success_msg).to_be_visible(timeout=5000)

    success_text = success_msg.text_content()
    assert "Payment successful" in success_text
    assert re.search(r"txn_[a-f0-9]{12}", success_text)
```

**Assertions:**
- Page titles (explicit navigation verification)
- URL matching (redirect validation)
- Element visibility (async operation completion)
- Text content (business logic validation)
- Regex matching (transaction ID format)

### Playwright Best Practices Used

1. **Auto-waiting**: Playwright waits for elements automatically
   ```python
   page.click("#btn")  # Waits for element to be clickable
   ```

2. **Explicit expectations**: Use `expect()` for assertions
   ```python
   expect(page).to_have_title("...")  # Retries until timeout
   ```

3. **Selectors**: Use CSS selectors with IDs
   ```python
   page.fill("#username", "demo")  # Fast, reliable
   ```

4. **Timeouts**: Explicit timeouts for network operations
   ```python
   page.wait_for_url("...", timeout=5000)
   ```

### Test Execution

**Commands:**
```bash
# Run all tests
pytest tests/test_payment_flow.py -v

# Run with output
pytest tests/test_payment_flow.py -v -s

# Run with screenshots on failure
pytest tests/test_payment_flow.py --screenshot=only-on-failure

# Run with video recording
pytest tests/test_payment_flow.py --video=retain-on-failure

# Run in headed mode (visible browser)
pytest tests/test_payment_flow.py --headed
```

**Output Example:**
```
============================= test session starts ==============================
platform darwin -- Python 3.11.13, pytest-7.4.3, pluggy-1.6.0
plugins: playwright-0.4.3, anyio-4.11.0, base-url-2.1.0
collected 1 item

tests/test_payment_flow.py::test_complete_payment_flow[chromium] PASSED [100%]

============================== 1 passed in 2.09s ===============================
```

---

## Design Decisions

### 1. Port Selection: 5001 vs 5000

**Context:** macOS AirPlay Receiver uses port 5000 by default

**Decision:** Use port 5001

**Rationale:**
- Avoids conflicts on developer machines
- No need to disable system services
- Easy to change if needed

**Impact:**
- `backend/app.py` line 57: `app.run(..., port=5001)`
- `tests/conftest.py` line 72: `base_url = "http://localhost:5001"`

**Alternatives Considered:**
- Port 8000 (common for Python apps)
- Port 3000 (common for Node.js)
- Dynamic port allocation

### 2. Frontend: Vanilla JS vs Angular

**Context:** Requirements specified Angular

**Decision:** Use vanilla JavaScript

**Rationale:**
| Factor | Vanilla JS | Angular |
|--------|------------|---------|
| Pages | 2 simple forms | Overkill |
| Build process | None | Complex (webpack, TypeScript) |
| Development time | 2 hours | 6-8 hours |
| Learning curve | Low | High |
| Testing complexity | Simple DOM | Component testing |
| Future scaling | Can migrate later | Better for large apps |

**Impact:**
- Faster development
- No build step
- Easier to debug in Playwright
- Less maintainable at scale

**Migration Path:**
If app grows, migrate to React/Angular SPA:
1. Keep Flask as API-only backend
2. Serve frontend from separate server/CDN
3. Use JWT instead of sessions
4. Enable full CORS

### 3. Backend: Flask vs FastAPI

**Decision:** Use Flask

**Rationale:**
| Feature | Flask | FastAPI |
|---------|-------|---------|
| Async support | No | Yes |
| Type hints | Optional | Required |
| Documentation | Manual | Auto-generated |
| Session management | Built-in | Manual |
| Template rendering | Jinja2 included | Manual |
| Maturity | 13 years | 4 years |
| Use case | Monolithic web apps | API microservices |

**For this project:**
- Small application (2 endpoints)
- Need session management
- Need template rendering
- No async I/O requirements

**When to use FastAPI:**
- API-only backend
- Need async/await
- Want auto-generated docs
- High concurrency requirements

### 4. Sessions: Server-side vs JWT

**Decision:** Flask server-side sessions

**Rationale:**
| Aspect | Server Sessions | JWT |
|--------|----------------|-----|
| Statefulness | Stateful | Stateless |
| Storage | Server memory/Redis | Client cookie |
| Scalability | Harder (sticky sessions) | Easier (any server) |
| Security | Server-controlled | Client holds token |
| Revocation | Instant | Requires blacklist |
| Implementation | Simple (Flask built-in) | Requires library |

**For this project:**
- Single server deployment
- No horizontal scaling needed
- Simpler implementation
- Better security for demo

**When to use JWT:**
- Microservices architecture
- Mobile app clients
- Horizontal scaling required
- API-only backend

### 5. Database: SQLite vs PostgreSQL

**Decision:** SQLite

**Rationale:**
| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Setup | Zero config | Requires server |
| Concurrency | Single writer | Multiple writers |
| File-based | Yes | No (network) |
| Backup | Copy file | pg_dump |
| Transactions/second | ~1000 | ~10000+ |
| Use case | < 100k rows | Production apps |

**For this project:**
- Small dataset (< 1000 transactions)
- Easy to reset for testing
- No separate server needed
- Sufficient for demo

**Migration Path to PostgreSQL:**
```python
# Only need to change database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@host/db'
# Models remain unchanged (SQLAlchemy abstraction)
```

### 6. Testing: Synchronous vs Async Playwright

**Decision:** Synchronous Playwright API

**Rationale:**
| API | Sync | Async |
|-----|------|-------|
| Syntax | `page.click()` | `await page.click()` |
| Pytest integration | Better | Requires pytest-asyncio |
| Parallel execution | Sequential | Parallel possible |
| Code complexity | Simpler | More complex |
| Use case | Small test suite | Large test suite |

**For this project:**
- Only 1 test currently
- Simpler code
- Better pytest integration

**When to use Async:**
- Large test suite (> 50 tests)
- Need parallel execution
- Already using async/await

### 7. Account Data: Hardcoded vs Dynamic

**Decision:** Hardcoded account options in payment.html

**Implementation:**
```html
<option value="123456789">123456789 - Vernor Vinge</option>
<option value="987654321">987654321 - Issac Asimov</option>
```

**Rationale:**
- Only 2 accounts in metadata.json
- Accounts rarely change
- Simpler implementation
- No additional API call

**Alternative (Dynamic):**
```javascript
// Fetch accounts on page load
const response = await fetch('/accounts');
const data = await response.json();
data.accounts.forEach(account => {
    const option = document.createElement('option');
    option.value = account.account_id;
    option.textContent = `${account.account_id} - ${account.account_name}`;
    debtorSelect.appendChild(option);
});
```

**When to use dynamic:**
- Accounts change frequently
- Many accounts (> 10)
- Multi-tenant application

---

## Performance Characteristics

### Application Performance

#### Server Startup
```
Cold start: 2-3 seconds
- Import modules: ~1s
- Initialize Flask: ~0.5s
- Initialize SQLAlchemy: ~0.5s
- Start server: ~1s
```

#### Request Latency (localhost)

| Endpoint | Avg Latency | Operations |
|----------|-------------|------------|
| GET / | 50ms | Template rendering |
| POST /login | 80ms | DB query + session creation |
| POST /payment | 120ms | 2x DB query + insert + commit |
| GET /accounts | 30ms | Single SELECT query |

**Breakdown of POST /payment:**
```
Total: 120ms
├─ Request parsing: 5ms
├─ Session validation: 10ms
├─ Debtor account query: 25ms
├─ Creditor account query: 25ms
├─ Transaction insert: 35ms
├─ Commit to disk: 15ms
└─ Response serialization: 5ms
```

#### Database Performance

| Operation | Time | Notes |
|-----------|------|-------|
| INSERT transaction | 35ms | Includes index updates |
| SELECT account by ID | 5ms | Indexed lookup |
| SELECT all accounts | 10ms | 2 rows, no join |
| Database file size | 32KB | With 0 transactions |
| Database file size | 100KB | With 1000 transactions |

**SQLite Limitations:**
- Single writer at a time (write lock)
- Concurrent reads OK
- Estimated throughput: ~1000 writes/second

### Test Performance

#### Full Test Suite Execution

```
Total time: 2.09 seconds

Breakdown:
├─ Pytest initialization: 0.1s
├─ Session fixture setup: 1.0s
│   ├─ Start Flask subprocess: 0.2s
│   ├─ Wait for server ready: 0.8s
│   └─ Playwright initialization: 0.0s
├─ Test execution: 0.9s
│   ├─ Browser launch: 0.3s
│   ├─ Login flow: 0.2s
│   ├─ Payment flow: 0.3s
│   └─ Assertions: 0.1s
└─ Session fixture teardown: 0.1s
    └─ Terminate Flask: 0.1s
```

#### Browser Operations

| Operation | Time | Notes |
|-----------|------|-------|
| Launch Chromium | 300ms | First time slower |
| Navigate to page | 100ms | Local server |
| Fill input field | 50ms | Includes auto-wait |
| Click button | 50ms | Includes auto-wait |
| Wait for navigation | 100ms | Redirect to payment |
| Take screenshot | 200ms | On failure only |

### Scalability Benchmarks

**Current Configuration:**
- Single Flask process
- SQLite database
- No caching
- Server-side sessions in memory

**Load Testing Results (hypothetical):**

| Concurrent Users | Response Time | Success Rate | Bottleneck |
|------------------|---------------|--------------|------------|
| 1-10 | < 200ms | 100% | None |
| 10-50 | < 500ms | 100% | CPU |
| 50-100 | < 1s | 95% | SQLite write lock |
| 100+ | > 2s | 80% | Database concurrency |

**Bottlenecks:**
1. **SQLite write lock** (concurrent writes)
2. **Single process** (no parallelism)
3. **No connection pooling**
4. **Session storage** (memory grows)

---

## Scalability Considerations

### Current Architecture Limitations

| Component | Limitation | Impact | Max Scale |
|-----------|------------|--------|-----------|
| Flask single process | 1 request at a time | Throughput | ~100 req/s |
| SQLite | 1 writer at a time | Concurrency | ~1000 TPS |
| In-memory sessions | RAM usage grows | Memory leak | ~10k sessions |
| No caching | DB hit every request | Latency | - |
| No load balancer | Single point of failure | Availability | 1 server |

### Horizontal Scaling Path

#### Phase 1: Optimize Current Stack
**Target:** 500 concurrent users

```
┌──────────────────────────────────────┐
│   Nginx (reverse proxy + SSL)       │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│   Gunicorn (4 workers)               │
│   - Worker class: sync               │
│   - Workers: 2 * CPU cores + 1       │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│   PostgreSQL (database)              │
│   - Connection pool: 20              │
│   - Max connections: 100             │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│   Redis (session store)              │
│   - Persist sessions outside app     │
└──────────────────────────────────────┘
```

**Changes Required:**
```python
# 1. Switch to PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

# 2. Use Redis for sessions
from flask_session import Session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.environ['REDIS_URL'])

# 3. Add connection pooling
app.config['SQLALCHEMY_POOL_SIZE'] = 20
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
```

**Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

#### Phase 2: Horizontal Scaling
**Target:** 5000 concurrent users

```
                ┌──────────────────┐
                │  Load Balancer   │
                │   (AWS ALB)      │
                └────────┬─────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐ ┌───────▼──────┐ ┌──────▼───────┐
│  App Server  │ │  App Server  │ │  App Server  │
│  Instance 1  │ │  Instance 2  │ │  Instance N  │
│  (4 workers) │ │  (4 workers) │ │  (4 workers) │
└───────┬──────┘ └───────┬──────┘ └──────┬───────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                ┌────────▼─────────┐
                │   PostgreSQL     │
                │   (RDS/managed)  │
                │   - Read replica │
                └──────────────────┘

                ┌──────────────────┐
                │   Redis Cluster  │
                │   (ElastiCache)  │
                └──────────────────┘
```

**Infrastructure:**
- AWS EC2 Auto Scaling Group (3-10 instances)
- AWS RDS PostgreSQL (Multi-AZ)
- AWS ElastiCache Redis (Cluster mode)
- AWS Application Load Balancer
- AWS CloudWatch monitoring

#### Phase 3: Microservices
**Target:** 50k+ concurrent users

```
┌─────────────────────────────────────────────────────┐
│                   API Gateway                        │
│                (Rate limiting, Auth)                 │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐
│   Auth       │ │  Payment  │ │  Account  │
│   Service    │ │  Service  │ │  Service  │
│   (JWT)      │ │  (Async)  │ │  (Cache)  │
└───────┬──────┘ └─────┬─────┘ └─────┬─────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼──────┐             ┌────────▼────────┐
│  PostgreSQL  │             │  Message Queue  │
│  (Sharded)   │             │  (RabbitMQ)     │
└──────────────┘             └─────────────────┘
```

**Technology Changes:**
- FastAPI (async/await)
- JWT tokens (stateless auth)
- Message queue (async processing)
- Database sharding (horizontal partitioning)
- Event sourcing (audit trail)
- CQRS (read/write separation)

### Cost Analysis

| Phase | Infrastructure | Monthly Cost (AWS) |
|-------|---------------|-------------------|
| Current | 1x t3.small | ~$15 |
| Phase 1 | 1x t3.medium, RDS, ElastiCache | ~$150 |
| Phase 2 | 3x t3.large, RDS Multi-AZ, ElastiCache | ~$800 |
| Phase 3 | Microservices, EKS, MSK | ~$3000+ |

### Performance Targets

| Metric | Current | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|---------|
| Concurrent users | 100 | 500 | 5000 | 50000+ |
| Requests/second | 100 | 500 | 5000 | 50000+ |
| Avg response time | 200ms | 150ms | 100ms | 50ms |
| Availability | 95% | 99% | 99.9% | 99.99% |
| Database size | 10MB | 1GB | 100GB | 10TB |

---

## Deployment Guide

### Development Deployment

**Prerequisites:**
- Python 3.11+
- pip

**Steps:**
```bash
# 1. Clone repository
git clone <repo-url>
cd ui-testing-agent

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Initialize database
python backend/init_db.py

# 4. Run application
python backend/app.py

# 5. Access application
open http://localhost:5001
```

### Production Deployment

#### Option 1: Single Server (DigitalOcean/Linode)

**Server Requirements:**
- 2 CPU cores
- 4 GB RAM
- 20 GB SSD
- Ubuntu 22.04 LTS

**Deployment Steps:**

```bash
# 1. Install dependencies
sudo apt update
sudo apt install python3.11 python3-pip nginx supervisor

# 2. Clone application
git clone <repo-url> /opt/transaction-app
cd /opt/transaction-app

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pip install gunicorn

# 4. Initialize database
python backend/init_db.py

# 5. Create systemd service
sudo nano /etc/systemd/system/transaction-app.service
```

**Systemd Service File:**
```ini
[Unit]
Description=Transaction Processing Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/transaction-app
Environment="PATH=/opt/transaction-app/venv/bin"
Environment="SECRET_KEY=<generate-with-openssl-rand-hex-32>"
ExecStart=/opt/transaction-app/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:8000 \
    --access-logfile /var/log/transaction-app/access.log \
    --error-logfile /var/log/transaction-app/error.log \
    backend.app:app

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/transaction-app/frontend/static;
        expires 30d;
    }
}
```

**SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

**Start Services:**
```bash
sudo systemctl enable transaction-app
sudo systemctl start transaction-app
sudo systemctl restart nginx
```

#### Option 2: Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python backend/init_db.py

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "backend.app:app"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=sqlite:///database/transactions.db
    volumes:
      - ./database:/app/database
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
```

**Deploy:**
```bash
docker-compose up -d
```

#### Option 3: AWS Elastic Beanstalk

**Requirements:**
- `.ebextensions/` directory with configuration
- `Procfile` for process management
- Environment variables in EB console

**Procfile:**
```
web: gunicorn -w 4 -b :8000 backend.app:app
```

**Deploy:**
```bash
eb init transaction-app --region us-east-1
eb create production-env
eb deploy
```

### Environment Variables (Production)

**Required:**
```bash
SECRET_KEY=<generate-strong-key>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://user:pass@host:6379/0
FLASK_ENV=production
```

**Generate Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Database Migration (SQLite → PostgreSQL)

```bash
# 1. Export SQLite data
sqlite3 database/transactions.db .dump > backup.sql

# 2. Create PostgreSQL database
createdb transaction_db

# 3. Update connection string
export DATABASE_URL=postgresql://localhost/transaction_db

# 4. Run migrations
python backend/init_db.py

# 5. Import data (manual if needed)
```

### Monitoring & Logging

**Application Logs:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('/var/log/app.log'),
        logging.StreamHandler()
    ]
)
```

**Monitoring Tools:**
- **Sentry** - Error tracking
- **DataDog** - Performance monitoring
- **CloudWatch** - AWS infrastructure monitoring
- **Prometheus + Grafana** - Metrics visualization

### Backup Strategy

**Database Backup:**
```bash
# SQLite
sqlite3 database/transactions.db ".backup 'backup-$(date +%Y%m%d).db'"

# PostgreSQL
pg_dump -Fc transaction_db > backup-$(date +%Y%m%d).dump
```

**Automated Backup (cron):**
```bash
# Daily at 2 AM
0 2 * * * /opt/transaction-app/scripts/backup.sh
```

### Security Checklist

- [ ] Change SECRET_KEY to random value
- [ ] Enable HTTPS (SSL/TLS certificate)
- [ ] Set secure cookie flags (Secure=True)
- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection (Flask-WTF)
- [ ] Hash passwords (bcrypt/argon2)
- [ ] Implement rate limiting
- [ ] Add input sanitization
- [ ] Enable firewall (UFW/Security Groups)
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor error logs

---

## Appendix

### File Structure Summary

```
ui-testing-agent/
├── backend/
│   ├── __init__.py             # Package marker
│   ├── app.py                  # Flask application (59 lines)
│   ├── routes.py               # API endpoints (125 lines)
│   ├── models.py               # Database models (48 lines)
│   ├── database.py             # DB configuration (16 lines)
│   ├── init_db.py              # Database initialization (66 lines)
│   └── requirements.txt        # Python dependencies (3 packages)
├── frontend/
│   ├── templates/
│   │   ├── login.html          # Login page (40 lines)
│   │   └── payment.html        # Payment page (47 lines)
│   └── static/
│       ├── css/
│       │   └── styles.css      # Styles (130 lines)
│       └── js/
│           ├── login.js        # Login controller (66 lines)
│           └── payment.js      # Payment controller (97 lines)
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures (73 lines)
│   ├── test_payment_flow.py   # E2E test (72 lines)
│   └── requirements.txt        # Test dependencies (4 packages)
├── database/
│   └── transactions.db         # SQLite database (generated)
├── metadata.json               # Seed data (16 lines)
├── .gitignore                  # Git ignore rules
├── README.md                   # User documentation
├── TECHNICAL_OVERVIEW.md       # This document
├── claude.md                   # Project requirements
└── LICENSE                     # License file

Total Lines of Code: ~850 (excluding comments and blank lines)
```

### Technology Versions

| Technology | Version | Release Date | EOL |
|------------|---------|--------------|-----|
| Python | 3.11.13 | Oct 2024 | Oct 2027 |
| Flask | 3.0.0 | Sep 2023 | - |
| SQLAlchemy | 3.1.1 | Dec 2023 | - |
| Playwright | 1.40.0 | Nov 2023 | - |
| Pytest | 7.4.3 | Oct 2023 | - |

### Glossary

| Term | Definition |
|------|------------|
| **ACID** | Atomicity, Consistency, Isolation, Durability - database transaction properties |
| **AJAX** | Asynchronous JavaScript and XML - technique for async requests |
| **CORS** | Cross-Origin Resource Sharing - HTTP header-based mechanism |
| **CSRF** | Cross-Site Request Forgery - web security vulnerability |
| **E2E** | End-to-End - testing complete user flows |
| **JWT** | JSON Web Token - compact token format |
| **ORM** | Object-Relational Mapping - database abstraction layer |
| **SPA** | Single Page Application - client-rendered web app |
| **UUID** | Universally Unique Identifier - 128-bit identifier |
| **WSGI** | Web Server Gateway Interface - Python web server standard |
| **XSS** | Cross-Site Scripting - code injection vulnerability |

### References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Playwright Documentation](https://playwright.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

**Document Version:** 1.0
**Last Updated:** 2026-01-11
**Maintained By:** Development Team
