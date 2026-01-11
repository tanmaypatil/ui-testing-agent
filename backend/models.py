from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(50), unique=True, nullable=False)
    account_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Account {self.account_id} - {self.account_name}>'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    debtor_account_id = db.Column(db.String(50), db.ForeignKey('accounts.account_id'), nullable=False)
    creditor_account_id = db.Column(db.String(50), db.ForeignKey('accounts.account_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')

    # Relationships
    debtor = db.relationship('Account', foreign_keys=[debtor_account_id])
    creditor = db.relationship('Account', foreign_keys=[creditor_account_id])

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'
