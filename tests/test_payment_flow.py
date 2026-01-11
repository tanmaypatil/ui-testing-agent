import re
from playwright.sync_api import Page, expect


def test_complete_payment_flow(page: Page, base_url: str):
    """
    End-to-end test for the complete payment flow.

    Test steps:
    1. Navigate to login page
    2. Fill in credentials (demo/password)
    3. Click login button
    4. Verify redirect to payment page
    5. Fill in payment form (debtor, creditor, amount)
    6. Submit payment
    7. Verify success message with transaction ID
    """

    # Step 1: Navigate to login page
    print("\nStep 1: Navigating to login page...")
    page.goto(base_url)

    # Verify login page loaded
    expect(page).to_have_title("Login - Transaction Processing")

    # Step 2: Fill in login credentials
    print("Step 2: Filling in login credentials...")
    page.fill("#username", "demo")
    page.fill("#password", "password")

    # Step 3: Click login button
    print("Step 3: Clicking login button...")
    page.click("#login-btn")

    # Step 4: Wait for redirect to payment page
    print("Step 4: Waiting for redirect to payment page...")
    page.wait_for_url(f"{base_url}/payment.html", timeout=5000)

    # Verify payment page loaded
    expect(page).to_have_title("Payment - Transaction Processing")
    print("Successfully redirected to payment page!")

    # Step 5: Fill in payment form
    print("Step 5: Filling in payment form...")

    # Select debtor account (Vernor Vinge - 123456789)
    page.select_option("#debtor", "123456789")

    # Select creditor account (Issac Asimov - 987654321)
    page.select_option("#creditor", "987654321")

    # Enter amount
    page.fill("#amount", "150.00")

    # Step 6: Submit payment
    print("Step 6: Submitting payment...")
    page.click("#submit-btn")

    # Step 7: Wait for success message
    print("Step 7: Waiting for success message...")

    # Wait for success message to appear
    success_msg = page.locator("#success-msg")
    expect(success_msg).to_be_visible(timeout=5000)

    # Verify success message contains transaction ID
    success_text = success_msg.text_content()
    print(f"Success message: {success_text}")

    # Check that message contains "Payment successful" and transaction ID pattern
    assert "Payment successful" in success_text
    assert "Transaction ID:" in success_text
    assert re.search(r"txn_[a-f0-9]{12}", success_text), "Transaction ID not found in expected format"

    # Extract and print transaction ID
    match = re.search(r"(txn_[a-f0-9]{12})", success_text)
    if match:
        transaction_id = match.group(1)
        print(f"Transaction ID generated: {transaction_id}")

    print("\n" + "="*60)
    print("TEST PASSED: Complete payment flow successful!")
    print("="*60)
