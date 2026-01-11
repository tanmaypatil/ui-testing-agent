import uuid
import time
from flask import Blueprint, request, jsonify, session
from models import db, User, Account, Transaction

api = Blueprint('api', __name__)


@api.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Username and password are required'
        }), 400

    username = data['username']
    password = data['password']

    # Find user
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        # Set session
        session['logged_in'] = True
        session['username'] = username
        return jsonify({
            'status': 'success',
            'message': 'Login successful'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid credentials'
        }), 401


@api.route('/payment', methods=['POST'])
def payment():
    """Handle payment transaction."""
    # Check if user is logged in
    if not session.get('logged_in'):
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized - please login first'
        }), 401

    data = request.get_json()

    if not data or 'debtor' not in data or 'creditor' not in data or 'amount' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Debtor, creditor, and amount are required'
        }), 400

    debtor_id = data['debtor']
    creditor_id = data['creditor']
    amount = data['amount']

    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Invalid amount'
        }), 400

    # Validate accounts exist
    debtor = Account.query.filter_by(account_id=debtor_id).first()
    creditor = Account.query.filter_by(account_id=creditor_id).first()

    if not debtor:
        return jsonify({
            'status': 'error',
            'message': f'Invalid debtor account: {debtor_id}'
        }), 400

    if not creditor:
        return jsonify({
            'status': 'error',
            'message': f'Invalid creditor account: {creditor_id}'
        }), 400

    # TEST SCENARIO: Simulate processing delay
    # Usage: POST /payment with {"test_delay": 25} to simulate 25-second delay
    # This allows testing timeout scenarios without modifying production code
    test_delay = data.get('test_delay', 0)
    if test_delay > 0:
        print(f"[TEST MODE] Simulating {test_delay} second delay...")
        time.sleep(test_delay)

    # Generate transaction ID
    transaction_id = f"txn_{uuid.uuid4().hex[:12]}"

    # Create transaction
    transaction = Transaction(
        transaction_id=transaction_id,
        debtor_account_id=debtor_id,
        creditor_account_id=creditor_id,
        amount=amount,
        status='completed'
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'transaction_id': transaction_id,
        'message': 'Payment processed successfully'
    }), 200


@api.route('/accounts', methods=['GET'])
def get_accounts():
    """Get all accounts (helper endpoint for frontend)."""
    accounts = Account.query.all()
    return jsonify({
        'accounts': [
            {
                'account_id': acc.account_id,
                'account_name': acc.account_name,
                'status': acc.status
            }
            for acc in accounts
        ]
    }), 200
