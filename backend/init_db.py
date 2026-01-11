#!/usr/bin/env python3
"""
Database initialization script.
Loads accounts from metadata.json and creates the demo user.
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db, User, Account
from database import init_db


def load_metadata():
    """Load account data from metadata.json."""
    metadata_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'metadata.json'
    )

    with open(metadata_path, 'r') as f:
        return json.load(f)


def populate_database():
    """Populate database with initial data."""
    # Create Flask app for database context
    app = Flask(__name__)
    init_db(app)

    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create demo user
        demo_user = User(username='demo', password='password')
        db.session.add(demo_user)
        print("Created demo user: username='demo', password='password'")

        # Load and create accounts from metadata.json
        metadata = load_metadata()
        for account_data in metadata.get('accounts', []):
            account = Account(
                account_id=account_data['account_id'],
                account_name=account_data['account_name'],
                created_at=datetime.fromisoformat(account_data['created_at'].replace('Z', '+00:00')),
                status=account_data['status']
            )
            db.session.add(account)
            print(f"Created account: {account.account_id} - {account.account_name}")

        # Commit all changes
        db.session.commit()
        print("\nDatabase populated successfully!")
        print(f"Total users: {User.query.count()}")
        print(f"Total accounts: {Account.query.count()}")


if __name__ == '__main__':
    populate_database()
