"""
Database models for NetWorth Tracker application.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    timezone = db.Column(db.String(50), default='America/Toronto')
    currency_preference = db.Column(db.String(3), default='CAD')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    assets = db.relationship('Asset', backref='user', lazy=True, cascade='all, delete-orphan')
    liabilities = db.relationship('Liability', backref='user', lazy=True, cascade='all, delete-orphan')
    accounts = db.relationship('Account', backref='user', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class AccountType(db.Model):
    """Account type classification (RRSP, TFSA, Non-registered, etc.)."""
    __tablename__ = 'account_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # registered, non-registered, etc.
    description = db.Column(db.Text)
    tax_advantaged = db.Column(db.Boolean, default=False)
    contribution_limit = db.Column(db.Boolean, default=False)
    
    # Relationships
    accounts = db.relationship('Account', backref='type', lazy=True)

class Account(db.Model):
    """Financial accounts (bank accounts, investment accounts, etc.)."""
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_type_id = db.Column(db.Integer, db.ForeignKey('account_types.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    account_number_encrypted = db.Column(db.String(255))  # Encrypted account number
    balance = db.Column(db.Numeric(15, 2), default=0)
    currency = db.Column(db.String(3), default='CAD')
    interest_rate = db.Column(db.Numeric(5, 4))  # Annual interest rate
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    assets = db.relationship('Asset', backref='account', lazy=True)
    transactions = db.relationship('Transaction', backref='account', lazy=True)
    
    @property
    def account_type(self):
        """Get account type name."""
        return self.type.name if self.type else None

class AssetType(db.Model):
    """Asset type classification."""
    __tablename__ = 'asset_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # equity, fixed_income, real_estate, etc.
    description = db.Column(db.Text)
    
    # Relationships
    assets = db.relationship('Asset', backref='type', lazy=True)

class Asset(db.Model):
    """Investment assets (stocks, ETFs, mutual funds, real estate, etc.)."""
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    asset_type_id = db.Column(db.Integer, db.ForeignKey('asset_types.id'), nullable=False)
    symbol = db.Column(db.String(20))  # Stock ticker, mutual fund code, etc.
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Numeric(15, 6), nullable=False)
    purchase_price = db.Column(db.Numeric(15, 4), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    currency = db.Column(db.String(3), default='CAD')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    @property
    def asset_type(self):
        """Get asset type name."""
        return self.type.name if self.type else None
    
    @property
    def total_cost(self):
        """Calculate total cost basis."""
        return float(self.quantity * self.purchase_price)

class AssetPrice(db.Model):
    """Historical and current asset prices."""
    __tablename__ = 'asset_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False, index=True)
    price = db.Column(db.Numeric(15, 4), nullable=False)
    currency = db.Column(db.String(3), default='CAD')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    source = db.Column(db.String(50))  # alpha_vantage, yahoo_finance, etc.
    
    __table_args__ = (
        db.Index('idx_symbol_timestamp', 'symbol', 'timestamp'),
    )

class LiabilityType(db.Model):
    """Liability type classification."""
    __tablename__ = 'liability_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # mortgage, credit_card, loan, etc.
    description = db.Column(db.Text)
    
    # Relationships
    liabilities = db.relationship('Liability', backref='type', lazy=True)

class Liability(db.Model):
    """Debts and liabilities (mortgages, loans, credit cards, etc.)."""
    __tablename__ = 'liabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    liability_type_id = db.Column(db.Integer, db.ForeignKey('liability_types.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Numeric(15, 2), nullable=False)
    original_amount = db.Column(db.Numeric(15, 2))
    interest_rate = db.Column(db.Numeric(5, 4), nullable=False)  # Annual interest rate
    minimum_payment = db.Column(db.Numeric(10, 2))
    payment_frequency = db.Column(db.String(20))  # monthly, bi-weekly, etc.
    term_months = db.Column(db.Integer)  # Total term in months
    start_date = db.Column(db.Date)
    maturity_date = db.Column(db.Date)
    currency = db.Column(db.String(3), default='CAD')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    @property
    def liability_type(self):
        """Get liability type name."""
        return self.type.name if self.type else None

class Property(db.Model):
    """Real estate properties."""
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(10))
    property_type = db.Column(db.String(50), nullable=False)  # primary, rental, commercial
    purchase_price = db.Column(db.Numeric(15, 2), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    current_value = db.Column(db.Numeric(15, 2))
    last_valuation_date = db.Column(db.Date)
    square_footage = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Numeric(3, 1))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    valuations = db.relationship('PropertyValuation', backref='property', lazy=True)

class PropertyValuation(db.Model):
    """Property valuation history."""
    __tablename__ = 'property_valuations'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    valuation = db.Column(db.Numeric(15, 2), nullable=False)
    valuation_date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100))  # appraisal, assessment, estimate
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PhysicalAsset(db.Model):
    """Physical assets (bullion, collectibles, etc.)."""
    __tablename__ = 'physical_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # gold, silver, art, etc.
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(15, 6), nullable=False)
    unit = db.Column(db.String(20))  # oz, grams, pieces, etc.
    purity = db.Column(db.Numeric(5, 4))  # For precious metals
    purchase_price = db.Column(db.Numeric(15, 2), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    current_value = db.Column(db.Numeric(15, 2))
    storage_location = db.Column(db.String(255))
    insurance_value = db.Column(db.Numeric(15, 2))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Transaction(db.Model):
    """Financial transactions and cash flows."""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # buy, sell, dividend, etc.
    category = db.Column(db.String(100))
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    currency = db.Column(db.String(3), default='CAD')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_user_date', 'user_id', 'date'),
    )

class NetWorthSnapshot(db.Model):
    """Historical net worth snapshots for tracking over time."""
    __tablename__ = 'networth_snapshots'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    snapshot_date = db.Column(db.Date, nullable=False)
    total_assets = db.Column(db.Numeric(15, 2), nullable=False)
    total_liabilities = db.Column(db.Numeric(15, 2), nullable=False)
    net_worth = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_user_snapshot_date', 'user_id', 'snapshot_date'),
        db.UniqueConstraint('user_id', 'snapshot_date', name='unique_user_snapshot_date'),
    )
