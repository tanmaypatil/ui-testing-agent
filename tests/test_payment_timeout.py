"""
Test payment timeout scenario with comprehensive diagnostics.

This test demonstrates a timeout failure and captures extensive
diagnostic information for debugging.
"""

import pytest
import json
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page, expect


def test_payment_timeout_with_diagnostics(page: Page, base_url: str):
    """
    Test payment processing with intentional timeout.

    Scenario:
    - Backend is configured to delay for 25 seconds (via test_delay parameter)
    - Test expects success within 20 seconds
    - Test will timeout and capture comprehensive diagnostics

    Expected Result: FAILURE (timeout after 20 seconds)
    Actual Backend Delay: 25 seconds

    Diagnostics Captured:
    - Screenshots (before submit, at failure)
    - Page HTML
    - Console logs
    - Network requests/responses
    - Cookies/session state
    - Element states
    - Database state
    - HTML report
    """

    # Setup diagnostics directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    diagnostics_dir = Path(f"test_diagnostics/payment_timeout_{timestamp}")
    diagnostics_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"TIMEOUT TEST: Payment with 25s backend delay, 20s test timeout")
    print(f"Diagnostics will be saved to: {diagnostics_dir}")
    print(f"{'='*70}\n")

    # Enable console logging
    console_logs = []
    page.on("console", lambda msg: console_logs.append({
        "type": msg.type,
        "text": msg.text,
        "location": f"{msg.location.get('url', 'unknown')}:{msg.location.get('lineNumber', 0)}"
    }))

    # Enable request/response logging
    requests_log = []
    responses_log = []

    def log_request(request):
        requests_log.append({
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "post_data": request.post_data,
            "timestamp": datetime.now().isoformat()
        })

    def log_response(response):
        responses_log.append({
            "url": response.url,
            "status": response.status,
            "headers": dict(response.headers),
            "timestamp": datetime.now().isoformat()
        })

    page.on("request", log_request)
    page.on("response", log_response)

    # Initialize submit_time to avoid UnboundLocalError if early failure occurs
    submit_time = datetime.now()

    try:
        # Step 1: Login
        print("Step 1: Logging in...")
        page.goto(base_url)
        page.fill("#username", "demo")
        page.fill("#password", "password")
        page.click("#login-btn")
        page.wait_for_url(f"{base_url}/payment.html", timeout=5000)
        print("  ✓ Login successful")

        # Step 2: Navigate to payment page with test_delay parameter
        # This tells the backend to delay for 25 seconds
        print("\nStep 2: Navigating to payment page with test_delay=25...")
        page.goto(f"{base_url}/payment.html?test_delay=25")
        print("  ✓ Payment page loaded with delay parameter")

        # Step 3: Fill payment form
        print("\nStep 3: Filling payment form...")
        page.select_option("#debtor", "123456789")
        page.select_option("#creditor", "987654321")
        page.fill("#amount", "150.00")
        print("  ✓ Form filled")

        # Capture screenshot before submission
        page.screenshot(path=diagnostics_dir / "before_submit.png")
        print("  ✓ Screenshot captured (before submit)")

        # Step 4: Submit payment
        print("\nStep 4: Submitting payment (backend will delay 25s)...")
        submit_time = datetime.now()  # Update to actual submit time
        page.click("#submit-btn")
        print("  ✓ Submit button clicked")

        # Step 5: Wait for success with 20-second timeout
        # This WILL timeout because backend delays 25 seconds
        print("\nStep 5: Waiting for success (20s timeout)...")
        success_msg = page.locator("#success-msg")

        # This will raise TimeoutError after 20 seconds
        expect(success_msg).to_be_visible(timeout=20000)

        # If we reach here, test passed (unexpected!)
        print("  ✓ SUCCESS: Payment completed before timeout")
        assert "Transaction ID:" in success_msg.text_content()

    except Exception as e:
        # TIMEOUT OCCURRED - Capture comprehensive diagnostics

        failure_time = datetime.now()
        duration = (failure_time - submit_time).total_seconds()

        print(f"\n{'='*70}")
        print(f"❌ TIMEOUT OCCURRED (Expected behavior)")
        print(f"{'='*70}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Error: {type(e).__name__}: {str(e)}")
        print(f"Diagnostics location: {diagnostics_dir}")
        print(f"{'='*70}\n")

        # === DIAGNOSTIC COLLECTION ===

        # 1. SCREENSHOT - Current page state at failure
        page.screenshot(path=diagnostics_dir / "failure_screenshot.png", full_page=True)
        print("📸 Screenshot captured (failure state)")

        # 2. PAGE HTML - Full DOM state
        html_content = page.content()
        (diagnostics_dir / "page_content.html").write_text(html_content)
        print("📄 Page HTML captured")

        # 3. CONSOLE LOGS - JavaScript errors and messages
        (diagnostics_dir / "console_logs.json").write_text(
            json.dumps(console_logs, indent=2)
        )
        print(f"📋 Console logs captured ({len(console_logs)} entries)")

        # 4. NETWORK LOGS - All HTTP requests and responses
        (diagnostics_dir / "network_requests.json").write_text(
            json.dumps(requests_log, indent=2)
        )
        (diagnostics_dir / "network_responses.json").write_text(
            json.dumps(responses_log, indent=2)
        )
        print(f"🌐 Network logs captured ({len(requests_log)} requests)")

        # 5. BROWSER COOKIES - Session state
        cookies = page.context.cookies()
        (diagnostics_dir / "cookies.json").write_text(
            json.dumps(cookies, indent=2)
        )
        print("🍪 Cookies captured")

        # 6. ELEMENT STATES - UI component visibility
        element_states = {
            "success_msg_visible": page.locator("#success-msg").is_visible(),
            "success_msg_text": page.locator("#success-msg").text_content() or "",
            "error_msg_visible": page.locator("#error-msg").is_visible(),
            "error_msg_text": page.locator("#error-msg").text_content() or "",
            "submit_btn_enabled": page.locator("#submit-btn").is_enabled(),
            "submit_btn_text": page.locator("#submit-btn").text_content(),
        }
        (diagnostics_dir / "element_states.json").write_text(
            json.dumps(element_states, indent=2)
        )
        print("🎯 Element states captured")

        # 7. DATABASE STATE - Check transaction creation
        import sqlite3
        db_path = Path(__file__).parent.parent / "database" / "transactions.db"

        if db_path.exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Get recent transactions
            cursor.execute("""
                SELECT transaction_id, debtor_account_id, creditor_account_id,
                       amount, created_at, status
                FROM transactions
                ORDER BY created_at DESC
                LIMIT 5
            """)
            recent_transactions = cursor.fetchall()

            # Get total transaction count
            cursor.execute("SELECT COUNT(*) FROM transactions")
            total_count = cursor.fetchone()[0]

            db_state = {
                "total_transactions": total_count,
                "recent_transactions": [
                    {
                        "transaction_id": row[0],
                        "debtor_account_id": row[1],
                        "creditor_account_id": row[2],
                        "amount": float(row[3]),
                        "created_at": row[4],
                        "status": row[5]
                    }
                    for row in recent_transactions
                ]
            }
            conn.close()

            (diagnostics_dir / "database_state.json").write_text(
                json.dumps(db_state, indent=2)
            )
            print(f"💾 Database state captured ({total_count} total transactions)")

        # 8. FAILURE SUMMARY - Consolidated information
        failure_summary = {
            "test_name": "test_payment_timeout_with_diagnostics",
            "timestamp": failure_time.isoformat(),
            "duration_seconds": duration,
            "expected_timeout_seconds": 20,
            "backend_delay_seconds": 25,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "browser": "chromium",
            "current_url": page.url,
            "element_states": element_states,
            "console_errors": [log for log in console_logs if log["type"] == "error"],
            "failed_requests": [r for r in responses_log if r["status"] >= 400],
            "test_parameters": {
                "debtor": "123456789",
                "creditor": "987654321",
                "amount": 150.00,
                "test_delay": 25
            }
        }

        (diagnostics_dir / "failure_summary.json").write_text(
            json.dumps(failure_summary, indent=2)
        )
        print("📊 Failure summary created")

        # 9. HTML REPORT - Human-readable summary
        console_errors_html = json.dumps(
            [log for log in console_logs if log["type"] == "error"],
            indent=2
        ) or "[]"

        failed_requests_html = json.dumps(
            [r for r in responses_log if r["status"] >= 400],
            indent=2
        ) or "[]"

        db_state_html = json.dumps(db_state, indent=2) if db_path.exists() else "{}"

        html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Payment Timeout Test Report - {timestamp}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #c33;
            border-bottom: 3px solid #c33;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
            border-left: 4px solid #667eea;
            padding-left: 15px;
        }}
        .section {{
            margin: 20px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 6px;
            border-left: 4px solid #ddd;
        }}
        .error {{
            background: #fee;
            border-left: 4px solid #c33;
        }}
        .success {{
            background: #efe;
            border-left: 4px solid #363;
        }}
        .info {{
            background: #eef;
            border-left: 4px solid #36c;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            overflow-x: auto;
            border-radius: 4px;
            font-size: 13px;
        }}
        img {{
            max-width: 100%;
            border: 2px solid #ddd;
            border-radius: 4px;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }}
        .badge-error {{ background: #c33; color: white; }}
        .badge-success {{ background: #363; color: white; }}
        .badge-info {{ background: #36c; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⏱️ Payment Timeout Test Failure Report</h1>

        <div class="section info">
            <h2>Test Summary</h2>
            <table>
                <tr><th>Property</th><th>Value</th></tr>
                <tr><td>Test Name</td><td>test_payment_timeout_with_diagnostics</td></tr>
                <tr><td>Timestamp</td><td>{failure_time}</td></tr>
                <tr><td>Duration</td><td><strong>{duration:.2f} seconds</strong></td></tr>
                <tr><td>Expected Timeout</td><td>20 seconds</td></tr>
                <tr><td>Backend Delay</td><td>25 seconds</td></tr>
                <tr><td>Result</td><td><span class="badge badge-error">TIMEOUT (Expected)</span></td></tr>
            </table>
        </div>

        <div class="section error">
            <h2>Error Details</h2>
            <p><strong>Type:</strong> {type(e).__name__}</p>
            <pre>{str(e)}</pre>
        </div>

        <div class="section">
            <h2>Test Parameters</h2>
            <table>
                <tr><th>Parameter</th><th>Value</th></tr>
                <tr><td>Debtor Account</td><td>123456789 (Vernor Vinge)</td></tr>
                <tr><td>Creditor Account</td><td>987654321 (Issac Asimov)</td></tr>
                <tr><td>Amount</td><td>$150.00</td></tr>
                <tr><td>Test Delay</td><td>25 seconds</td></tr>
            </table>
        </div>

        <div class="section">
            <h2>Screenshots</h2>
            <h3>Before Submit</h3>
            <img src="before_submit.png" alt="Before Submit">
            <h3>At Failure (20s timeout)</h3>
            <img src="failure_screenshot.png" alt="Failure Screenshot">
        </div>

        <div class="section">
            <h2>Element States at Failure</h2>
            <pre>{json.dumps(element_states, indent=2)}</pre>
        </div>

        <div class="section">
            <h2>Console Errors</h2>
            <pre>{console_errors_html}</pre>
        </div>

        <div class="section">
            <h2>Failed HTTP Requests</h2>
            <pre>{failed_requests_html}</pre>
        </div>

        <div class="section">
            <h2>Database State</h2>
            <p>Total Transactions: {db_state.get('total_transactions', 0)}</p>
            <pre>{db_state_html}</pre>
        </div>

        <div class="section info">
            <h2>📁 All Diagnostic Files</h2>
            <ul>
                <li><a href="before_submit.png">📸 Before Submit Screenshot</a></li>
                <li><a href="failure_screenshot.png">📸 Failure Screenshot</a></li>
                <li><a href="page_content.html">📄 Page HTML</a></li>
                <li><a href="console_logs.json">📋 Console Logs</a></li>
                <li><a href="network_requests.json">🌐 Network Requests</a></li>
                <li><a href="network_responses.json">🌐 Network Responses</a></li>
                <li><a href="cookies.json">🍪 Cookies</a></li>
                <li><a href="element_states.json">🎯 Element States</a></li>
                <li><a href="database_state.json">💾 Database State</a></li>
                <li><a href="failure_summary.json">📊 Failure Summary</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
        """

        (diagnostics_dir / "report.html").write_text(html_report)
        print("📋 HTML report generated")

        print(f"\n{'='*70}")
        print(f"📊 Open report in browser:")
        print(f"   file://{diagnostics_dir.absolute()}/report.html")
        print(f"{'='*70}\n")

        # Re-raise the exception so pytest marks test as failed
        raise


def test_payment_with_api_delay_direct():
    """
    Alternative approach: Test using direct API call with delay.

    This bypasses the UI and tests the backend delay directly.
    Useful for verifying the delay mechanism works.
    """
    import requests
    import time

    # Login first to get session
    session = requests.Session()
    login_response = session.post(
        "http://localhost:5001/login",
        json={"username": "demo", "password": "password"}
    )
    assert login_response.status_code == 200

    # Make payment request with 5 second delay
    start_time = time.time()

    payment_response = session.post(
        "http://localhost:5001/payment",
        json={
            "debtor": "123456789",
            "creditor": "987654321",
            "amount": 100.00,
            "test_delay": 5  # 5 second delay
        }
    )

    elapsed_time = time.time() - start_time

    # Verify the delay worked
    assert elapsed_time >= 5.0, f"Expected delay >= 5s, got {elapsed_time:.2f}s"
    assert payment_response.status_code == 200

    data = payment_response.json()
    assert data["status"] == "success"
    assert "transaction_id" in data

    print(f"\n✓ Payment completed after {elapsed_time:.2f}s delay")
