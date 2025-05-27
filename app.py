"""
NetWorth Tracker - Personal Net Worth Tracking Application
A comprehensive web application for tracking personal net worth with Canadian-specific features.
"""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd
import requests
from decouple import config

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = config('SECRET_KEY', default='dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL', default='sqlite:///networth.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# API Keys
app.config['ALPHA_VANTAGE_API_KEY'] = config('ALPHA_VANTAGE_API_KEY', default='')
app.config['YAHOO_FINANCE_ENABLED'] = config('YAHOO_FINANCE_ENABLED', default=True, cast=bool)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
CORS(app)

# Import models
from models import User, Asset, Liability, Account, AssetPrice, Transaction

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Main dashboard showing net worth overview."""
    if not current_user.is_authenticated:
        return render_template('landing.html')
    
    # Calculate net worth
    total_assets = calculate_total_assets(current_user.id)
    total_liabilities = calculate_total_liabilities(current_user.id)
    net_worth = total_assets - total_liabilities
    
    # Get recent transactions
    recent_transactions = get_recent_transactions(current_user.id, limit=5)
    
    # Get asset allocation
    asset_allocation = get_asset_allocation(current_user.id)
    
    # Get net worth history
    net_worth_history = get_net_worth_history(current_user.id, days=365)
    
    return render_template('dashboard.html',
                         net_worth=net_worth,
                         total_assets=total_assets,
                         total_liabilities=total_liabilities,
                         recent_transactions=recent_transactions,
                         asset_allocation=asset_allocation,
                         net_worth_history=net_worth_history)

@app.route('/assets')
@login_required
def assets():
    """Assets portfolio view."""
    user_assets = Asset.query.filter_by(user_id=current_user.id).all()
    
    # Group assets by type
    assets_by_type = {}
    for asset in user_assets:
        asset_type = asset.asset_type
        if asset_type not in assets_by_type:
            assets_by_type[asset_type] = []
        
        # Get current price
        current_price = get_current_price(asset.symbol)
        current_value = asset.quantity * current_price if current_price else 0
        gain_loss = current_value - (asset.quantity * asset.purchase_price)
        gain_loss_percent = (gain_loss / (asset.quantity * asset.purchase_price)) * 100 if asset.purchase_price > 0 else 0
        
        asset_data = {
            'asset': asset,
            'current_price': current_price,
            'current_value': current_value,
            'gain_loss': gain_loss,
            'gain_loss_percent': gain_loss_percent
        }
        assets_by_type[asset_type].append(asset_data)
    
    return render_template('assets.html', assets_by_type=assets_by_type)

@app.route('/liabilities')
@login_required
def liabilities():
    """Liabilities and debt overview."""
    user_liabilities = Liability.query.filter_by(user_id=current_user.id).all()
    
    # Group liabilities by type
    liabilities_by_type = {}
    for liability in user_liabilities:
        liability_type = liability.liability_type
        if liability_type not in liabilities_by_type:
            liabilities_by_type[liability_type] = []
        liabilities_by_type[liability_type].append(liability)
    
    return render_template('liabilities.html', liabilities_by_type=liabilities_by_type)

@app.route('/accounts')
@login_required
def accounts():
    """Canadian account classification view."""
    user_accounts = Account.query.filter_by(user_id=current_user.id).all()
    
    # Group accounts by type
    accounts_by_type = {}
    for account in user_accounts:
        account_type = account.account_type
        if account_type not in accounts_by_type:
            accounts_by_type[account_type] = []
        accounts_by_type[account_type].append(account)
    
    # Calculate contribution room for RRSP and TFSA
    rrsp_contribution_room = calculate_rrsp_contribution_room(current_user.id)
    tfsa_contribution_room = calculate_tfsa_contribution_room(current_user.id)
    
    return render_template('accounts.html',
                         accounts_by_type=accounts_by_type,
                         rrsp_contribution_room=rrsp_contribution_room,
                         tfsa_contribution_room=tfsa_contribution_room)

@app.route('/reports')
@login_required
def reports():
    """Reports and analytics view."""
    # Generate various reports
    performance_report = generate_performance_report(current_user.id)
    allocation_report = generate_allocation_report(current_user.id)
    tax_report = generate_tax_report(current_user.id)
    
    return render_template('reports.html',
                         performance_report=performance_report,
                         allocation_report=allocation_report,
                         tax_report=tax_report)

# API Routes
@app.route('/api/assets', methods=['GET', 'POST'])
@login_required
def api_assets():
    """API endpoint for asset management."""
    if request.method == 'POST':
        data = request.get_json()
        
        # Create new asset
        asset = Asset(
            user_id=current_user.id,
            asset_type=data['asset_type'],
            symbol=data['symbol'],
            name=data['name'],
            quantity=data['quantity'],
            purchase_price=data['purchase_price'],
            purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d').date(),
            account_id=data.get('account_id')
        )
        
        db.session.add(asset)
        db.session.commit()
        
        return jsonify({'success': True, 'asset_id': asset.id})
    
    # GET request - return user's assets
    assets = Asset.query.filter_by(user_id=current_user.id).all()
    assets_data = []
    
    for asset in assets:
        current_price = get_current_price(asset.symbol)
        assets_data.append({
            'id': asset.id,
            'asset_type': asset.asset_type,
            'symbol': asset.symbol,
            'name': asset.name,
            'quantity': asset.quantity,
            'purchase_price': asset.purchase_price,
            'current_price': current_price,
            'current_value': asset.quantity * current_price if current_price else 0,
            'purchase_date': asset.purchase_date.isoformat()
        })
    
    return jsonify(assets_data)

@app.route('/api/market/price/<symbol>')
def api_get_price(symbol):
    """API endpoint to get current market price for a symbol."""
    price = get_current_price(symbol)
    return jsonify({'symbol': symbol, 'price': price})

@app.route('/api/networth/history')
@login_required
def api_networth_history():
    """API endpoint for net worth historical data."""
    days = request.args.get('days', 365, type=int)
    history = get_net_worth_history(current_user.id, days)
    return jsonify(history)

# Helper Functions
def calculate_total_assets(user_id):
    """Calculate total asset value for a user."""
    assets = Asset.query.filter_by(user_id=user_id).all()
    total = 0
    
    for asset in assets:
        current_price = get_current_price(asset.symbol)
        if current_price:
            total += asset.quantity * current_price
        else:
            # Fallback to purchase price if current price unavailable
            total += asset.quantity * asset.purchase_price
    
    return total

def calculate_total_liabilities(user_id):
    """Calculate total liability value for a user."""
    liabilities = Liability.query.filter_by(user_id=user_id).all()
    return sum(liability.balance for liability in liabilities)

def get_current_price(symbol):
    """Get current market price for a symbol."""
    try:
        # Try Alpha Vantage first
        if app.config['ALPHA_VANTAGE_API_KEY']:
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
        
        # Fallback to Yahoo Finance
        if app.config['YAHOO_FINANCE_ENABLED']:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info.get('currentPrice') or info.get('regularMarketPrice')
    
    except Exception as e:
        app.logger.error(f"Error fetching price for {symbol}: {e}")
    
    return None

def get_recent_transactions(user_id, limit=10):
    """Get recent transactions for a user."""
    transactions = Transaction.query.filter_by(user_id=user_id)\
                                  .order_by(Transaction.date.desc())\
                                  .limit(limit).all()
    return transactions

def get_asset_allocation(user_id):
    """Calculate asset allocation breakdown."""
    assets = Asset.query.filter_by(user_id=user_id).all()
    allocation = {}
    total_value = 0
    
    for asset in assets:
        current_price = get_current_price(asset.symbol)
        if current_price:
            value = asset.quantity * current_price
            total_value += value
            
            if asset.asset_type not in allocation:
                allocation[asset.asset_type] = 0
            allocation[asset.asset_type] += value
    
    # Convert to percentages
    if total_value > 0:
        for asset_type in allocation:
            allocation[asset_type] = (allocation[asset_type] / total_value) * 100
    
    return allocation

def get_net_worth_history(user_id, days=365):
    """Get historical net worth data."""
    # This is a simplified version - in production, you'd store historical snapshots
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # For now, return mock data - implement proper historical tracking
    history = []
    current_net_worth = calculate_total_assets(user_id) - calculate_total_liabilities(user_id)
    
    for i in range(days):
        date = start_date + timedelta(days=i)
        # Mock historical data with some variation
        variation = (i / days) * 0.1 + 0.95  # Gradual growth
        net_worth = current_net_worth * variation
        history.append({
            'date': date.isoformat(),
            'net_worth': net_worth
        })
    
    return history

def calculate_rrsp_contribution_room(user_id):
    """Calculate RRSP contribution room (simplified)."""
    # This would integrate with CRA data in production
    return 25000  # Mock value

def calculate_tfsa_contribution_room(user_id):
    """Calculate TFSA contribution room (simplified)."""
    # This would integrate with CRA data in production
    return 6500  # Mock value

def generate_performance_report(user_id):
    """Generate performance analytics report."""
    # Implement performance calculations
    return {'ytd_return': 12.5, 'total_return': 45.2}

def generate_allocation_report(user_id):
    """Generate asset allocation report."""
    return get_asset_allocation(user_id)

def generate_tax_report(user_id):
    """Generate tax optimization report."""
    # Implement tax analysis
    return {'tax_loss_harvesting': 2500, 'dividend_income': 1200}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
