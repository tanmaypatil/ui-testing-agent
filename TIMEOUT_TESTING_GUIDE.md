# Timeout Testing Guide

Complete guide for testing timeout scenarios in the transaction processing application.

---

## Overview

This application includes a built-in mechanism to simulate backend processing delays, enabling comprehensive timeout scenario testing without modifying production code.

**Key Feature:** The `/payment` endpoint accepts an optional `test_delay` parameter that causes the backend to sleep for a specified duration.

---

## Implementation Details

### Backend (routes.py)

```python
# TEST SCENARIO: Simulate processing delay
test_delay = data.get('test_delay', 0)
if test_delay > 0:
    print(f"[TEST MODE] Simulating {test_delay} second delay...")
    time.sleep(test_delay)
```

### Frontend (payment.js)

```javascript
// TEST SCENARIO: Check for test_delay parameter in URL
const urlParams = new URLSearchParams(window.location.search);
const testDelay = urlParams.get('test_delay');

if (testDelay) {
    requestBody.test_delay = parseInt(testDelay);
    console.log(`[TEST MODE] Requesting ${testDelay} second delay`);
}
```

---

## Usage Methods

### Method 1: URL Parameter (Easiest)

Navigate to the payment page with the delay parameter in the URL:

```
http://localhost:5001/payment.html?test_delay=25
```

**Workflow:**
1. User logs in normally
2. Gets redirected to payment page with `?test_delay=25`
3. Frontend JavaScript extracts the parameter
4. Payment request includes `test_delay: 25`
5. Backend delays 25 seconds before processing

**Use Case:** Manual browser testing

---

### Method 2: Direct API Call

Use Python `requests` or `curl` to call the API directly:

#### Python
```python
import requests

# Login
session = requests.Session()
login_response = session.post(
    "http://localhost:5001/login",
    json={"username": "demo", "password": "password"}
)

# Payment with 25-second delay
payment_response = session.post(
    "http://localhost:5001/payment",
    json={
        "debtor": "123456789",
        "creditor": "987654321",
        "amount": 100.00,
        "test_delay": 25  # 25 second delay
    }
)
```

#### cURL
```bash
# Login and save cookies
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"password"}' \
  -c cookies.txt

# Payment with delay
curl -X POST http://localhost:5001/payment \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"debtor":"123456789","creditor":"987654321","amount":150.00,"test_delay":25}'
```

**Use Case:** API integration testing

---

### Method 3: Playwright Test

The comprehensive timeout test in `tests/test_payment_timeout.py`:

```python
def test_payment_timeout_with_diagnostics(page: Page, base_url: str):
    # Login
    page.goto(base_url)
    page.fill("#username", "demo")
    page.fill("#password", "password")
    page.click("#login-btn")
    page.wait_for_url(f"{base_url}/payment.html")

    # Navigate with delay parameter
    page.goto(f"{base_url}/payment.html?test_delay=25")

    # Fill and submit
    page.select_option("#debtor", "123456789")
    page.select_option("#creditor", "987654321")
    page.fill("#amount", "150.00")
    page.click("#submit-btn")

    # Wait with 20-second timeout (will fail!)
    success_msg = page.locator("#success-msg")
    expect(success_msg).to_be_visible(timeout=20000)  # TimeoutError
```

**Use Case:** Automated regression testing

---

### Method 4: Playwright Route Interception (Alternative)

Intercept network requests and add delays without backend changes:

```python
import time

def test_with_route_interception(page: Page, base_url: str):
    # Intercept payment requests
    def handle_payment_route(route):
        # Add artificial delay
        time.sleep(25)
        # Continue with original request
        route.continue_()

    page.route("**/payment", handle_payment_route)

    # Rest of test...
    page.goto(base_url)
    # ... normal test flow
```

**Use Case:** Testing without backend modifications

---

## Running the Timeout Test

### Execute Test
```bash
# Run with verbose output
pytest tests/test_payment_timeout.py -v -s

# Expected output:
# ============================================================
# TIMEOUT TEST: Payment with 25s backend delay, 20s timeout
# Diagnostics will be saved to: test_diagnostics/...
# ============================================================
#
# Step 1: Logging in...
#   ✓ Login successful
# Step 2: Navigating to payment page with test_delay=25...
#   ✓ Payment page loaded
# Step 3: Filling payment form...
#   ✓ Form filled
# Step 4: Submitting payment (backend will delay 25s)...
#   ✓ Submit clicked
# Step 5: Waiting for success (20s timeout)...
#
# ============================================================
# ❌ TIMEOUT OCCURRED (Expected behavior)
# ============================================================
# Duration: 20.XX seconds
# Error: TimeoutError: ...
```

### View Diagnostics
```bash
# Find latest diagnostics folder
ls -ltr test_diagnostics/

# Open HTML report
open test_diagnostics/payment_timeout_<timestamp>/report.html
```

---

## Diagnostics Captured on Timeout

When a timeout occurs, the following artifacts are automatically captured:

| Artifact | Filename | Contains |
|----------|----------|----------|
| **Screenshot (before)** | `before_submit.png` | UI state before clicking submit |
| **Screenshot (failure)** | `failure_screenshot.png` | UI state at timeout (20s) |
| **Page HTML** | `page_content.html` | Full DOM at failure |
| **Console Logs** | `console_logs.json` | JavaScript console messages/errors |
| **Network Requests** | `network_requests.json` | All HTTP requests with headers |
| **Network Responses** | `network_responses.json` | All HTTP responses with status |
| **Cookies** | `cookies.json` | Session cookies |
| **Element States** | `element_states.json` | Visibility/text of key elements |
| **Database State** | `database_state.json` | Recent transactions |
| **Summary** | `failure_summary.json` | Consolidated test information |
| **HTML Report** | `report.html` | Human-readable report with images |

---

## Test Scenarios

### Scenario 1: Expected Timeout (Default)
```
Backend Delay: 25 seconds
Test Timeout: 20 seconds
Expected Result: FAIL (timeout after 20s)
```

### Scenario 2: Just Under Timeout
```
Backend Delay: 19 seconds
Test Timeout: 20 seconds
Expected Result: PASS (completes in time)
```

### Scenario 3: Extreme Delay
```
Backend Delay: 60 seconds
Test Timeout: 20 seconds
Expected Result: FAIL (timeout after 20s)
```

### Scenario 4: No Delay
```
Backend Delay: 0 seconds (omit test_delay)
Test Timeout: 20 seconds
Expected Result: PASS (completes immediately)
```

---

## Common Use Cases

### 1. Testing Timeout Handling
**Goal:** Verify UI shows proper error message when backend times out

```python
def test_timeout_error_message(page, base_url):
    # Navigate with 25s delay
    page.goto(f"{base_url}/payment.html?test_delay=25")

    # Submit payment
    page.click("#submit-btn")

    # Check error message appears
    error_msg = page.locator("#error-msg")
    expect(error_msg).to_be_visible(timeout=25000)
    assert "timeout" in error_msg.text_content().lower()
```

### 2. Testing Loading States
**Goal:** Verify loading spinner or disabled button during processing

```python
def test_loading_state(page, base_url):
    page.goto(f"{base_url}/payment.html?test_delay=10")
    page.click("#submit-btn")

    # Check button is disabled during processing
    submit_btn = page.locator("#submit-btn")
    expect(submit_btn).to_be_disabled()
    assert "Processing..." in submit_btn.text_content()
```

### 3. Testing Retry Logic
**Goal:** Verify automatic retry on timeout

```python
def test_retry_on_timeout(page, base_url):
    retry_count = 0

    def handle_route(route):
        nonlocal retry_count
        retry_count += 1
        if retry_count < 3:
            time.sleep(25)  # Timeout first 2 attempts
        route.continue_()

    page.route("**/payment", handle_route)

    # Should retry and eventually succeed
    # ... test logic
```

---

## Best Practices

### ✅ DO

1. **Use test_delay for timeout scenarios**
   ```python
   # Good: Explicit delay for testing
   page.goto(f"{base_url}/payment.html?test_delay=25")
   ```

2. **Capture diagnostics on failure**
   ```python
   # Always capture screenshots, logs, etc.
   page.screenshot(path="diagnostics/failure.png")
   ```

3. **Test both success and timeout paths**
   ```python
   # Test with delay < timeout (success)
   # Test with delay > timeout (failure)
   ```

4. **Set reasonable timeouts**
   ```python
   # Good: Explicit timeout
   expect(element).to_be_visible(timeout=20000)
   ```

5. **Clean up test artifacts**
   ```bash
   # Periodically clean old diagnostics
   rm -rf test_diagnostics/old_*
   ```

### ❌ DON'T

1. **Don't use test_delay in production**
   ```python
   # Bad: test_delay should NEVER be in production code
   if environment == "production" and test_delay > 0:
       raise ValueError("test_delay not allowed in production")
   ```

2. **Don't use arbitrary sleep() in tests**
   ```python
   # Bad: Arbitrary delays
   time.sleep(25)

   # Good: Explicit backend delay
   page.goto(f"{base_url}/payment.html?test_delay=25")
   ```

3. **Don't ignore timeout failures**
   ```python
   # Bad: Catching and ignoring
   try:
       expect(element).to_be_visible(timeout=20000)
   except TimeoutError:
       pass  # Don't do this!
   ```

4. **Don't set infinite timeouts**
   ```python
   # Bad: No timeout
   expect(element).to_be_visible(timeout=0)

   # Good: Reasonable timeout
   expect(element).to_be_visible(timeout=20000)
   ```

---

## Troubleshooting

### Backend doesn't delay

**Problem:** Payment completes immediately even with `test_delay=25`

**Solution:**
```bash
# Check backend logs
python backend/app.py
# Look for: [TEST MODE] Simulating 25 second delay...

# Verify parameter is passed
curl -X POST http://localhost:5001/payment \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"debtor":"123456789","creditor":"987654321","amount":150,"test_delay":25}' \
  -v
```

### Test hangs forever

**Problem:** Test never completes or times out

**Solution:**
- Check if backend delay > test timeout
- Verify Flask server is running
- Check for infinite loops in frontend JavaScript

### No diagnostics captured

**Problem:** Test fails but no diagnostic files created

**Solution:**
```python
# Ensure diagnostics directory exists
diagnostics_dir = Path(f"test_diagnostics/...")
diagnostics_dir.mkdir(parents=True, exist_ok=True)

# Check file permissions
```

### Transaction created despite timeout

**Problem:** Database shows transaction even though test timed out

**Solution:**
- This is expected! Backend continues processing after frontend timeout
- Test timeout doesn't cancel backend processing
- Check `database_state.json` to see if transaction was created

---

## Performance Implications

### Test Execution Time

| Scenario | Duration | Use Case |
|----------|----------|----------|
| No delay | ~2 seconds | Happy path testing |
| 5s delay | ~7 seconds | Short timeout testing |
| 25s delay | ~22 seconds | Timeout failure testing |
| 60s delay | ~22 seconds | Extreme timeout (test aborts at 20s) |

### CI/CD Considerations

```yaml
# .github/workflows/tests.yml
- name: Run happy path tests (fast)
  run: pytest tests/test_payment_flow.py

- name: Run timeout tests (slow, optional)
  run: pytest tests/test_payment_timeout.py
  if: github.event_name == 'pull_request'
```

---

## Summary

### Key Takeaways

1. ✅ Backend supports `test_delay` parameter for timeout simulation
2. ✅ Frontend reads `test_delay` from URL parameter
3. ✅ Comprehensive diagnostics captured automatically
4. ✅ Multiple testing approaches available (URL, API, Playwright)
5. ⚠️ `test_delay` should ONLY be used in test environments
6. 📊 HTML reports generated for easy debugging

### Quick Reference

```bash
# Manual testing
http://localhost:5001/payment.html?test_delay=25

# Automated testing
pytest tests/test_payment_timeout.py -v -s

# View diagnostics
open test_diagnostics/payment_timeout_*/report.html
```

---

**Last Updated:** 2026-01-11
**Version:** 1.0
