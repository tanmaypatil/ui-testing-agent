document.addEventListener('DOMContentLoaded', function() {
    const paymentForm = document.getElementById('payment-form');
    const debtorSelect = document.getElementById('debtor');
    const creditorSelect = document.getElementById('creditor');
    const amountInput = document.getElementById('amount');
    const submitBtn = document.getElementById('submit-btn');
    const errorMsg = document.getElementById('error-msg');
    const successMsg = document.getElementById('success-msg');

    paymentForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Clear previous messages
        errorMsg.style.display = 'none';
        successMsg.style.display = 'none';
        errorMsg.textContent = '';
        successMsg.textContent = '';

        // Get form values
        const debtor = debtorSelect.value;
        const creditor = creditorSelect.value;
        const amount = amountInput.value;

        // Validate inputs
        if (!debtor || !creditor || !amount) {
            showError('Please fill in all fields');
            return;
        }

        if (parseFloat(amount) <= 0) {
            showError('Amount must be greater than 0');
            return;
        }

        if (debtor === creditor) {
            showError('Debtor and creditor must be different accounts');
            return;
        }

        // Disable button during request
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';

        try {
            const response = await fetch('/payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    debtor: debtor,
                    creditor: creditor,
                    amount: parseFloat(amount)
                })
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                // Show success message with transaction ID
                showSuccess(`Payment successful! Transaction ID: ${data.transaction_id}`);

                // Reset form
                paymentForm.reset();
            } else {
                // Show error message
                if (response.status === 401) {
                    // Redirect to login if not authenticated
                    showError('Session expired. Redirecting to login...');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                } else {
                    showError(data.message || 'Payment failed');
                }
            }
        } catch (error) {
            showError('Network error. Please try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Payment';
        }
    });

    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.style.display = 'block';
    }

    function showSuccess(message) {
        successMsg.textContent = message;
        successMsg.style.display = 'block';
    }
});
