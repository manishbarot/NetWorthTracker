# NetWorth Tracker - Personal Net Worth Tracking Application

A comprehensive web application for tracking personal net worth with Canadian-specific features, built with Flask and modern web technologies.

## 🎯 Project Overview

NetWorth Tracker is designed specifically for Canadian investors and individuals who want to track their complete financial picture, including:

- **Comprehensive Asset Tracking**: Stocks, ETFs, mutual funds, real estate, physical assets (bullion), and cash holdings
- **Canadian Account Classification**: RRSP, TFSA, RESP, and non-registered accounts with contribution room tracking
- **Liability Management**: Mortgages, loans, credit cards with amortization schedules
- **Real-time Market Data**: Automatic price updates via financial APIs
- **Advanced Analytics**: Performance tracking, asset allocation, and tax optimization
- **Privacy-First Design**: Local data storage with optional cloud sync

## 🚀 Key Features

### Core Asset Tracking
- ✅ Individual stocks with ticker symbols and real-time prices
- ✅ ETFs and mutual funds with NAV tracking
- ✅ Physical assets (gold, silver, platinum) with spot price integration
- ✅ Cash holdings across multiple institutions
- ✅ Real estate properties with automated valuation
- ✅ Alternative investments (crypto, private equity, collectibles)

### Canadian-Specific Features
- 🍁 RRSP contribution room tracking and optimization
- 🍁 TFSA contribution limit monitoring
- 🍁 RESP education savings tracking
- 🍁 Canadian tax-loss harvesting alerts
- 🍁 CAD/USD currency conversion
- 🍁 Integration with Canadian financial institutions

### Advanced Analytics
- 📊 Real-time net worth calculation and trending
- 📊 Asset allocation analysis and rebalancing suggestions
- 📊 Performance attribution and benchmark comparison
- 📊 Risk assessment and portfolio optimization
- 📊 Goal-based financial planning
- 📊 Tax optimization recommendations

### User Experience
- 📱 Mobile-responsive Progressive Web App (PWA)
- 🔒 Bank-level security with encryption
- 🎨 Modern, intuitive interface
- 📈 Interactive charts and visualizations
- 📄 Comprehensive reporting and export capabilities
- 👨‍👩‍👧‍👦 Family account management with privacy controls

## 🛠 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-Login with JWT tokens
- **Background Tasks**: Celery with Redis
- **APIs**: Alpha Vantage, Yahoo Finance, Bank of Canada

### Frontend
- **Framework**: React.js with TypeScript
- **UI Library**: Material-UI (MUI)
- **Charts**: Chart.js with react-chartjs-2
- **State Management**: Redux Toolkit
- **Build Tool**: Vite

### Infrastructure
- **Cloud**: AWS (EC2, RDS, S3, CloudWatch)
- **Caching**: Redis
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry for error tracking

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/NetWorthTracker.git
cd NetWorthTracker
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb networth_tracker

# Run migrations
flask db upgrade

# Seed initial data (optional)
python seed_data.py
```

### 4. Start Services
```bash
# Start Redis (in separate terminal)
redis-server

# Start Celery worker (in separate terminal)
celery -A app.celery worker --loglevel=info

# Start Flask application
python app.py
```

### 5. Frontend Setup (if using React frontend)
```bash
cd frontend
npm install
npm start
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/networth_tracker

# API Keys
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
YAHOO_FINANCE_ENABLED=true

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### API Keys Setup

1. **Alpha Vantage** (Primary market data):
   - Sign up at [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
   - Free tier: 5 API requests per minute, 500 per day

2. **Yahoo Finance** (Backup data):
   - No API key required
   - Rate limited but free

## 📊 Usage Guide

### Adding Your First Assets

1. **Navigate to Assets Page**: Click "Assets" in the main navigation
2. **Add Stock Holdings**: 
   - Click "Add Asset" button
   - Select "Stock" as asset type
   - Enter ticker symbol (e.g., "AAPL", "SHOP.TO")
   - Input quantity and purchase price
   - Assign to appropriate account (RRSP, TFSA, etc.)

3. **Add Real Estate**:
   - Select "Real Estate" asset type
   - Enter property address and purchase details
   - System will attempt automatic valuation

4. **Add Physical Assets**:
   - Select "Physical Asset" type
   - Choose subcategory (Gold, Silver, etc.)
   - Enter weight, purity, and purchase details

### Setting Up Canadian Accounts

1. **Create Account Types**:
   - RRSP accounts for retirement savings
   - TFSA accounts for tax-free growth
   - Non-registered for taxable investments

2. **Track Contribution Rooms**:
   - System calculates remaining RRSP/TFSA room
   - Provides optimization suggestions
   - Alerts for contribution deadlines

### Viewing Reports

1. **Dashboard Overview**: Real-time net worth and key metrics
2. **Performance Reports**: Historical returns and benchmarking
3. **Asset Allocation**: Current allocation vs. target
4. **Tax Reports**: Capital gains, dividend income, tax-loss harvesting

## 🔒 Security Features

- **Data Encryption**: All sensitive data encrypted at rest
- **Secure Authentication**: Password hashing with bcrypt
- **API Security**: Rate limiting and request validation
- **Privacy Controls**: Local data storage options
- **Audit Logging**: Track all data access and modifications

## 🧪 Testing

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=app

# Run integration tests
pytest tests/integration/

# Run frontend tests
cd frontend && npm test
```

## 📈 Development Roadmap

### Phase 1 (MVP - Completed)
- ✅ Basic asset and liability tracking
- ✅ User authentication and profiles
- ✅ Simple net worth calculation
- ✅ Manual data entry

### Phase 2 (Current)
- 🔄 Real-time market data integration
- 🔄 Canadian account classification
- 🔄 Advanced charting and visualization
- 🔄 Mobile optimization

### Phase 3 (Planned)
- 📅 AI-powered insights and recommendations
- 📅 Advanced scenario planning
- 📅 Tax optimization features
- 📅 Family account management

### Phase 4 (Future)
- 📅 Bank integration (Open Banking)
- 📅 Professional advisor portal
- 📅 Advanced estate planning
- 📅 Mobile native apps

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- Python: Follow PEP 8, use Black for formatting
- JavaScript: Use ESLint and Prettier
- Commit messages: Follow conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/yourusername/NetWorthTracker/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/NetWorthTracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/NetWorthTracker/discussions)
- **Email**: support@networthtracker.ca

## 🙏 Acknowledgments

- **Financial Data**: Alpha Vantage, Yahoo Finance
- **Canadian Data**: Bank of Canada, Statistics Canada
- **UI Components**: Material-UI, Chart.js
- **Infrastructure**: AWS, PostgreSQL, Redis

## 📊 Project Status

- **Current Version**: 0.1.0 (MVP)
- **Development Status**: Active
- **Production Ready**: No (Development phase)
- **Last Updated**: December 2024

---

**Built with ❤️ for Canadian investors and financial enthusiasts**
