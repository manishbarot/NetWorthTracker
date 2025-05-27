"""
NetWorth Tracker - POC Application
Simplified Flask application for Proof of Concept demonstration.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import requests
from decouple import config

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY', default='poc-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL', default='sqlite:///poc_networth.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# API Configuration
app.config['ALPHA_VANTAGE_API_KEY'] = config('ALPHA_VANTAGE_API_KEY', default='')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# POC Models (Simplified)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)  # RRSP, TFSA, Non-registered
    institution = db.Column(db.String(100), nullable=False)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    symbol = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)

class Liability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float)
    liability_type = db.Column(db.String(50), nullable=False)  # Mortgage, Credit Card, etc.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('poc_landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Create default accounts
        accounts = [
            Account(user_id=user.id, name='RRSP Account', account_type='RRSP', institution='TD Direct'),
            Account(user_id=user.id, name='TFSA Account', account_type='TFSA', institution='Questrade'),
            Account(user_id=user.id, name='Non-registered', account_type='Non-registered', institution='Interactive Brokers')
        ]
        for account in accounts:
            db.session.add(account)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('poc_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('poc_login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Calculate net worth
    total_assets = calculate_total_assets(current_user.id)
    total_liabilities = calculate_total_liabilities(current_user.id)
    net_worth = total_assets - total_liabilities
    
    # Get recent assets
    recent_assets = Asset.query.filter_by(user_id=current_user.id).order_by(Asset.id.desc()).limit(5).all()
    
    # Get account summary
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    account_summary = {}
    for account in accounts:
        account_assets = Asset.query.filter_by(user_id=current_user.id, account_id=account.id).all()
        account_value = sum(get_current_price(asset.symbol) * asset.quantity for asset in account_assets)
        account_summary[account.account_type] = account_summary.get(account.account_type, 0) + account_value
    
    return render_template('poc_dashboard.html',
                         net_worth=net_worth,
                         total_assets=total_assets,
                         total_liabilities=total_liabilities,
                         recent_assets=recent_assets,
                         account_summary=account_summary)

@app.route('/assets')
@login_required
def assets():
    user_assets = Asset.query.filter_by(user_id=current_user.id).all()
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    
    # Add current prices and values
    assets_with_prices = []
    for asset in user_assets:
        current_price = get_current_price(asset.symbol)
        current_value = current_price * asset.quantity if current_price else 0
        gain_loss = current_value - (asset.purchase_price * asset.quantity)
        
        assets_with_prices.append({
            'asset': asset,
            'current_price': current_price,
            'current_value': current_value,
            'gain_loss': gain_loss,
            'gain_loss_percent': (gain_loss / (asset.purchase_price * asset.quantity)) * 100 if asset.purchase_price > 0 else 0
        })
    
    return render_template('poc_assets.html', assets=assets_with_prices, accounts=accounts)

@app.route('/add_asset', methods=['POST'])
@login_required
def add_asset():
    symbol = request.form['symbol'].upper()
    name = request.form['name']
    quantity = float(request.form['quantity'])
    purchase_price = float(request.form['purchase_price'])
    purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date()
    account_id = int(request.form['account_id'])
    
    asset = Asset(
        user_id=current_user.id,
        account_id=account_id,
        symbol=symbol,
        name=name,
        quantity=quantity,
        purchase_price=purchase_price,
        purchase_date=purchase_date
    )
    
    db.session.add(asset)
    db.session.commit()
    
    flash(f'Added {quantity} shares of {symbol} successfully!')
    return redirect(url_for('assets'))

@app.route('/liabilities')
@login_required
def liabilities():
    user_liabilities = Liability.query.filter_by(user_id=current_user.id).all()
    return render_template('poc_liabilities.html', liabilities=user_liabilities)

@app.route('/add_liability', methods=['POST'])
@login_required
def add_liability():
    name = request.form['name']
    balance = float(request.form['balance'])
    interest_rate = float(request.form['interest_rate']) if request.form['interest_rate'] else 0
    liability_type = request.form['liability_type']
    
    liability = Liability(
        user_id=current_user.id,
        name=name,
        balance=balance,
        interest_rate=interest_rate,
        liability_type=liability_type
    )
    
    db.session.add(liability)
    db.session.commit()
    
    flash(f'Added {liability_type}: {name} successfully!')
    return redirect(url_for('liabilities'))

@app.route('/api/price/<symbol>')
def api_get_price(symbol):
    price = get_current_price(symbol)
    return jsonify({'symbol': symbol, 'price': price})

# Helper Functions
def calculate_total_assets(user_id):
    assets = Asset.query.filter_by(user_id=user_id).all()
    total = 0
    for asset in assets:
        current_price = get_current_price(asset.symbol)
        if current_price:
            total += asset.quantity * current_price
        else:
            total += asset.quantity * asset.purchase_price
    return total

def calculate_total_liabilities(user_id):
    liabilities = Liability.query.filter_by(user_id=user_id).all()
    return sum(liability.balance for liability in liabilities)

def get_current_price(symbol):
    """Get current price from Alpha Vantage API."""
    try:
        if not app.config['ALPHA_VANTAGE_API_KEY']:
            # Return mock price for demo
            mock_prices = {
                'AAPL': 150.00, 'GOOGL': 2500.00, 'MSFT': 300.00, 'TSLA': 800.00,
                'SHOP.TO': 80.00, 'RY.TO': 120.00, 'VGRO.TO': 25.50, 'VTI': 220.00
            }
            return mock_prices.get(symbol, 100.00)
        
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': app.config['ALPHA_VANTAGE_API_KEY']
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'Global Quote' in data:
            return float(data['Global Quote']['05. price'])
        
    except Exception as e:
        app.logger.error(f"Error fetching price for {symbol}: {e}")
    
    return None

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
