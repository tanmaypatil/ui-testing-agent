#!/usr/bin/env python3
"""
Flask application for transaction processing.
"""

import os
from flask import Flask, render_template
from flask_cors import CORS
from database import init_db
from routes import api


def create_app():
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder='../frontend/templates',
        static_folder='../frontend/static'
    )

    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Enable CORS
    CORS(app)

    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(api)

    # Routes for serving HTML pages
    @app.route('/')
    def index():
        """Serve login page."""
        return render_template('login.html')

    @app.route('/payment.html')
    def payment_page():
        """Serve payment page."""
        return render_template('payment.html')

    return app


if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("Transaction Processing Application Started")
    print("="*60)
    print("Access the application at: http://localhost:5001")
    print("Login credentials: username='demo', password='password'")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
