"""
NetWorth Tracker - POC Application
Simplified Flask application for Proof of Concept demonstration.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import requests
from decouple import config
import time
from models import db, User, Account, Asset, Liability, AssetType, LiabilityType

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY', default='poc-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poc_networth.db' # config('DATABASE_URL', default='sqlite:///poc_networth.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# API Configuration
app.config['ALPHA_VANTAGE_API_KEY'] = config('ALPHA_VANTAGE_API_KEY', default='')

# Simple in-memory cache for symbol lookup
symbol_cache = {}
CACHE_DURATION = timedelta(hours=24)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    print(f"DEBUG: load_user called with user_id: {user_id} (type: {type(user_id)})")
    user = User.query.get(str(user_id))
    print(f"DEBUG: User query result: {user}")
    return user

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

        try:
            # Create new user
            user = User(email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"DEBUG: User created with ID: {user.id}")

            # Single implicit portfolio - no need to create portfolio or assign accounts to portfolios
            # Create default accounts without portfolio assignment
            accounts = [
                Account(user_id=user.id, account_type_id=1, name='RRSP Account', institution='TD Direct'),
                Account(user_id=user.id, account_type_id=2, name='TFSA Account', institution='Questrade'),
                Account(user_id=user.id, account_type_id=3, name='Non-registered', institution='Interactive Brokers')
            ]
            for account in accounts:
                db.session.add(account)
            db.session.commit()
            print("DEBUG: Accounts created")

            login_user(user)
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"ERROR in register: {e}")
            db.session.rollback()
            flash(f"Registration failed: {e}")
            return redirect(url_for('register'))

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
    # Aggregate view (all user data in single implicit portfolio)
    total_assets = calculate_total_assets(current_user.id)
    total_liabilities = calculate_total_liabilities(current_user.id)
    net_worth = total_assets - total_liabilities

    # Get recent assets across all user data
    recent_assets = Asset.query.filter_by(user_id=current_user.id).order_by(Asset.id.desc()).limit(5).all()

    # Get account summary across all user data
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    account_summary = {}
    for account in accounts:
        account_assets = Asset.query.filter_by(user_id=current_user.id, account_id=account.id).all()
        account_value = sum((get_current_price(asset.symbol) or 0) * float(asset.quantity) for asset in account_assets)
        account_summary[account.account_type] = account_summary.get(account.account_type, 0) + account_value

    return render_template('poc_dashboard.html',
                           net_worth=net_worth,
                           total_assets=total_assets,
                           total_liabilities=total_liabilities,
                           recent_assets=recent_assets,
                           account_summary=account_summary,
                           portfolio=None,
                           portfolios=None)

@app.route('/assets')
@login_required
def assets():
    # All assets (single implicit portfolio for user)
    user_assets = Asset.query.filter_by(user_id=current_user.id).all()
    accounts = Account.query.filter_by(user_id=current_user.id).all()

    # Add current prices and values
    assets_with_prices = []
    for asset in user_assets:
        current_price = get_current_price(asset.symbol)
        current_value = current_price * float(asset.quantity) if current_price else 0
        gain_loss = current_value - (float(asset.purchase_price) * float(asset.quantity))

        assets_with_prices.append({
            'asset': asset,
            'current_price': current_price,
            'current_value': current_value,
            'gain_loss': gain_loss,
            'gain_loss_percent': (gain_loss / (float(asset.purchase_price) * float(asset.quantity))) * 100 if asset.purchase_price > 0 else 0
        })

    return render_template('poc_assets.html',
                           assets=assets_with_prices,
                           accounts=accounts,
                           portfolio=None,
                           portfolios=None)

@app.route('/add_asset', methods=['POST'])
@login_required
def add_asset():
    symbol = request.form['symbol'].upper()
    name = request.form['name']
    quantity = float(request.form['quantity'])
    purchase_price = float(request.form['purchase_price'])
    purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date()
    account_id = int(request.form['account_id'])
    asset_type_name = request.form.get('asset_type', 'Stock')

    # Single implicit portfolio for user - no portfolio assignment needed
    asset = Asset(
        user_id=current_user.id,
        account_id=account_id,
        asset_type_id=get_asset_type_id(asset_type_name),
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
    # All liabilities (single implicit portfolio for user)
    user_liabilities = Liability.query.filter_by(user_id=current_user.id).all()

    return render_template('poc_liabilities.html',
                           liabilities=user_liabilities,
                           portfolio=None,
                           portfolios=None)

@app.route('/add_liability', methods=['POST'])
@login_required
def add_liability():
    name = request.form['name']
    institution = request.form['institution'].strip()
    balance = float(request.form['balance'])
    interest_rate = float(request.form['interest_rate']) if request.form['interest_rate'] else 0
    liability_type = request.form['liability_type']

    # Single implicit portfolio for user - no portfolio assignment needed
    liability = Liability(
        user_id=current_user.id,
        name=name,
        institution=institution,
        balance=balance,
        interest_rate=interest_rate,
        liability_type_id=get_liability_type_id(liability_type)
    )

    db.session.add(liability)
    db.session.commit()

    flash(f'Added {liability_type}: {name} successfully!')
    return redirect(url_for('liabilities'))

@app.route('/api/symbol_search')
def api_symbol_search():
    query = request.args.get('q', '').strip()
    if not query or len(query) < 1:
        return jsonify([])

    results = search_symbols(query)
    return jsonify(results)

@app.route('/api/price/<symbol>')
def api_get_price(symbol):
    price = get_current_price(symbol)
    return jsonify({'symbol': symbol, 'price': price})

# Helper Functions
ASSET_CATEGORY_MAP = {
    'Stock': 'equity', 'ETF': 'equity', 'Mutual Fund': 'equity',
    'Bond': 'fixed_income', 'Crypto': 'crypto', 'Other': 'other',
}

LIABILITY_CATEGORY_MAP = {
    'Mortgage': 'mortgage', 'Credit Card': 'credit_card', 'Auto Loan': 'loan',
    'Personal Loan': 'loan', 'Line of Credit': 'loan', 'Student Loan': 'loan',
    'Other': 'other',
}

def get_asset_type_id(name):
    """Resolve an AssetType id by name, creating the type if it doesn't exist."""
    asset_type = AssetType.query.filter_by(name=name).first()
    if asset_type:
        return asset_type.id
    asset_type = AssetType(name=name, category=ASSET_CATEGORY_MAP.get(name, 'other'))
    db.session.add(asset_type)
    db.session.flush()
    return asset_type.id

def get_liability_type_id(name):
    """Resolve a LiabilityType id by name, creating the type if it doesn't exist."""
    liability_type = LiabilityType.query.filter_by(name=name).first()
    if liability_type:
        return liability_type.id
    liability_type = LiabilityType(name=name, category=LIABILITY_CATEGORY_MAP.get(name, 'other'))
    db.session.add(liability_type)
    db.session.flush()
    return liability_type.id

def calculate_total_assets(user_id):
    assets = Asset.query.filter_by(user_id=user_id).all()
    total = 0
    for asset in assets:
        current_price = get_current_price(asset.symbol)
        if current_price:
            total += float(asset.quantity) * current_price
        else:
            total += float(asset.quantity) * float(asset.purchase_price)
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

def search_symbols(query):
    """Search for stock symbols and company names using Alpha Vantage SYMBOL_SEARCH."""
    # Check cache first
    cache_key = query.upper()
    current_time = datetime.utcnow()

    if cache_key in symbol_cache:
        cached_result, cached_time = symbol_cache[cache_key]
        if current_time - cached_time < CACHE_DURATION:
            return cached_result

    try:
        if not app.config['ALPHA_VANTAGE_API_KEY']:
            # Return mock results for demo
            mock_results = [
                {'symbol': 'AAPL', 'name': 'Apple Inc.'},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
                {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
                {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
                {'symbol': 'SHOP.TO', 'name': 'Shopify Inc.'},
                {'symbol': 'RY.TO', 'name': 'Royal Bank of Canada'},
                {'symbol': 'VGRO.TO', 'name': 'Vanguard Growth ETF Portfolio'},
                {'symbol': 'VTI', 'name': 'Vanguard Total Stock Market ETF'}
            ]
            # Filter mock results based on query
            filtered_results = [
                result for result in mock_results
                if query.upper() in result['symbol'] or query.upper() in result['name'].upper()
            ][:5]  # Limit to 5 results
            symbol_cache[cache_key] = (filtered_results, current_time)
            return filtered_results

        # Rate limiting: wait 1 second between API calls
        time.sleep(1)

        url = "https://www.alphavantage.co/query"
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': query,
            'apikey': app.config['ALPHA_VANTAGE_API_KEY']
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if 'bestMatches' in data and data['bestMatches']:
            results = []
            for match in data['bestMatches'][:5]:  # Limit to 5 results
                results.append({
                    'symbol': match.get('1. symbol', ''),
                    'name': match.get('2. name', '')
                })

            # Cache the results
            symbol_cache[cache_key] = (results, current_time)
            return results

    except Exception as e:
        app.logger.error(f"Error searching symbols for '{query}': {e}")

    # Return empty list on error (fallback to manual entry)
    return []

if __name__ == '__main__':
    # For POC, skip table creation and just run
    app.run(debug=True, port=5001)
