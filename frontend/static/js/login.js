document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginBtn = document.getElementById('login-btn');
    const errorMsg = document.getElementById('error-msg');

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Clear previous errors
        errorMsg.style.display = 'none';
        errorMsg.textContent = '';

        // Get form values
        const username = usernameInput.value.trim();
        const password = passwordInput.value;

        // Validate inputs
        if (!username || !password) {
            showError('Please enter both username and password');
            return;
        }

        // Disable button during request
        loginBtn.disabled = true;
        loginBtn.textContent = 'Logging in...';

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                // Redirect to payment page on success
                window.location.href = '/payment.html';
            } else {
                // Show error message
                showError(data.message || 'Login failed');
                loginBtn.disabled = false;
                loginBtn.textContent = 'Login';
            }
        } catch (error) {
            showError('Network error. Please try again.');
            loginBtn.disabled = false;
            loginBtn.textContent = 'Login';
        }
    });

    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.style.display = 'block';
    }
});
