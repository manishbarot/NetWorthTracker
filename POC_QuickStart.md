# NetWorth Tracker POC - Quick Start Guide

## 🚀 Get the POC Running in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Step 1: Clone and Setup
```bash
# Clone the repository (after you create it on GitHub)
git clone https://github.com/manishbarot/NetWorthTracker.git
cd NetWorthTracker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install POC dependencies
pip install -r poc_requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (optional for POC)
# You can leave most settings as default for the POC
```

### Step 3: Run the POC Application
```bash
# Run the POC Flask app
python poc_app.py
```

The application will be available at: `http://127.0.0.1:5000`

## 🎯 POC Demo Flow

### 1. Landing Page
- Visit `http://127.0.0.1:5000`
- Review the features and Canadian focus
- Click "Create Free Account"

### 2. User Registration
- Fill in your details (use any email for POC)
- Password: minimum 6 characters
- System automatically creates 3 default accounts:
  - RRSP Account (TD Direct)
  - TFSA Account (Questrade)
  - Non-registered (Interactive Brokers)

### 3. Add Your First Assets
- Go to "Assets" page
- Click "Add Asset" 
- Try these sample stocks:
  - **AAPL** (Apple Inc.) - US stock
  - **SHOP.TO** (Shopify) - Canadian stock
  - **VGRO.TO** (Vanguard Growth ETF) - Canadian ETF
  - **VTI** (Vanguard Total Stock Market) - US ETF

### 4. Add Sample Liabilities
- Go to "Liabilities" page
- Add a mortgage: $300,000 at 3.5%
- Add a credit card: $5,000 at 19.9%

### 5. View Dashboard
- Return to Dashboard to see your net worth
- View account breakdown by type (RRSP, TFSA, Non-registered)
- See real-time asset values

## 📊 Sample Data for Testing

### Sample Assets to Add:
```
Stock: AAPL
Name: Apple Inc.
Quantity: 100
Purchase Price: $140.00
Account: Non-registered
Date: 2024-01-15

Stock: SHOP.TO  
Name: Shopify Inc.
Quantity: 50
Purchase Price: $75.00
Account: TFSA
Date: 2024-02-01

ETF: VGRO.TO
Name: Vanguard Growth ETF
Quantity: 1000
Purchase Price: $24.50
Account: RRSP
Date: 2024-03-01
```

### Sample Liabilities:
```
Mortgage:
Name: Primary Residence Mortgage
Balance: $350,000
Interest Rate: 3.25%
Type: Mortgage

Credit Card:
Name: RBC Visa
Balance: $3,500
Interest Rate: 19.99%
Type: Credit Card
```

## 🔧 POC Features to Test

### ✅ Core Functionality
- [ ] User registration and login
- [ ] Add stocks and ETFs
- [ ] View real-time prices (or mock prices)
- [ ] Calculate net worth automatically
- [ ] Classify assets by account type
- [ ] Add and track liabilities
- [ ] Responsive mobile design

### ✅ Canadian Features
- [ ] RRSP account classification
- [ ] TFSA account classification
- [ ] Canadian stock symbols (*.TO)
- [ ] CAD currency display
- [ ] Account type organization

### ✅ User Experience
- [ ] Intuitive navigation
- [ ] Clear value proposition
- [ ] Professional design
- [ ] Fast loading times
- [ ] Error handling

## 🐛 Troubleshooting

### Common Issues:

**1. "Module not found" errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r poc_requirements.txt
```

**2. Database errors:**
```bash
# Delete the database and restart
rm poc_networth.db
python poc_app.py
```

**3. API rate limiting:**
- The POC uses mock prices by default
- To use real prices, get a free Alpha Vantage API key
- Add it to your .env file: `ALPHA_VANTAGE_API_KEY=your_key_here`

**4. Port already in use:**
```bash
# Kill any existing Flask processes
pkill -f flask
# Or use a different port
export FLASK_RUN_PORT=5001
python poc_app.py
```

## 📱 Mobile Testing

Test the responsive design:
1. Open browser developer tools (F12)
2. Toggle device toolbar
3. Test on different screen sizes:
   - iPhone (375px width)
   - iPad (768px width)
   - Desktop (1200px+ width)

## 🎯 Demo Script (5 minutes)

**Minute 1: Landing Page**
- "Built specifically for Canadian investors"
- "RRSP/TFSA account tracking"
- "Real-time market data"

**Minute 2: Registration**
- Quick account creation
- Automatic account setup

**Minute 3: Add Assets**
- Add Canadian stock (SHOP.TO)
- Add US stock (AAPL)
- Show account classification

**Minute 4: Dashboard**
- Real-time net worth calculation
- Account breakdown
- Asset performance

**Minute 5: Mobile View**
- Show responsive design
- Mobile-optimized interface

## 🚀 Next Steps After POC

### Immediate Feedback Collection:
1. **User Experience**: How intuitive is the interface?
2. **Value Proposition**: Is the Canadian focus compelling?
3. **Feature Priorities**: What features are most important?
4. **Technical Performance**: Any bugs or issues?

### POC Success Metrics:
- [ ] Users can complete registration in < 2 minutes
- [ ] Users can add assets and see net worth in < 5 minutes
- [ ] No critical bugs during demo
- [ ] Positive feedback on Canadian features
- [ ] Clear understanding of value proposition

### Deployment Options:
- **Heroku**: Easy deployment for demos
- **Railway**: Modern alternative to Heroku
- **DigitalOcean**: More control and customization
- **Local Demo**: Run on laptop for presentations

This POC provides a solid foundation to validate the concept and gather user feedback before investing in full development!
