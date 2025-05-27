# NetWorth Tracker - UI/UX Design Specification

## 1. Design Philosophy and Principles

### 1.1 Core Design Principles
**Clarity First**: Financial data must be immediately understandable
**Trust and Security**: Visual design should convey reliability and security
**Canadian Context**: Design elements that resonate with Canadian users
**Mobile-First**: Responsive design optimized for mobile usage
**Accessibility**: WCAG 2.1 AA compliance for inclusive design

### 1.2 Visual Design Language
**Color Palette**:
- Primary: #1B365D (Deep Blue - trust, stability)
- Secondary: #FF6B35 (Orange - energy, growth)
- Success: #28A745 (Green - positive gains)
- Warning: #FFC107 (Yellow - alerts, attention)
- Danger: #DC3545 (Red - losses, critical alerts)
- Neutral: #6C757D (Gray - secondary information)
- Background: #F8F9FA (Light gray - clean, professional)

**Typography**:
- Primary: Inter (clean, modern, excellent readability)
- Secondary: Source Code Pro (for financial figures)
- Font Sizes: 12px, 14px, 16px, 18px, 24px, 32px, 48px

**Spacing System**: 4px base unit (4, 8, 12, 16, 24, 32, 48, 64px)

## 2. Key Screen Wireframes

### 2.1 Dashboard - Main Overview
```
┌─────────────────────────────────────────────────────────────┐
│ [Logo] NetWorth Tracker    [Search] [Notifications] [User] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │   Net Worth     │ │   This Month    │ │   YTD Change    │ │
│ │   $1,234,567    │ │   +$12,345      │ │   +15.2%        │ │
│ │   ↗ +2.3%       │ │   ↗ +2.1%       │ │   ↗ Positive    │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │              Net Worth Trend (12 months)               │ │
│ │  $1.4M ┌─────────────────────────────────────────────┐ │ │
│ │        │                                    ╭─╮      │ │ │
│ │  $1.2M │                              ╭─╮  ╱   ╲     │ │ │
│ │        │                        ╭─╮  ╱   ╲╱     ╲    │ │ │
│ │  $1.0M │                  ╭─╮  ╱   ╲╱             ╲   │ │ │
│ │        │            ╭─╮  ╱   ╲╱                    ╲  │ │ │
│ │  $0.8M │      ╭─╮  ╱   ╲╱                           ╲ │ │ │
│ │        └─────────────────────────────────────────────┘ │ │
│ │         Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────┐ ┌─────────────────────────────────────┐ │
│ │ Asset Allocation│ │         Recent Activity             │ │
│ │                 │ │ • AAPL +100 shares    $15,234      │ │
│ │   ◉ Stocks 45%  │ │ • Mortgage payment    -$2,100      │ │
│ │   ◉ Bonds  25%  │ │ • VGRO dividend       +$234        │ │
│ │   ◉ Cash   20%  │ │ • Property value ↑    +$5,000      │ │
│ │   ◉ RE     10%  │ │ • Credit card         -$1,234      │ │
│ └─────────────────┘ └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Assets Portfolio View
```
┌─────────────────────────────────────────────────────────────┐
│ Assets Portfolio                           [+ Add Asset]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─ Equities ($567,890) ──────────────────────────────────┐  │
│ │ Symbol │ Shares │ Price  │ Value    │ Gain/Loss │ %    │  │
│ │ AAPL   │ 100    │ $150   │ $15,000  │ +$2,500   │+20%  │  │
│ │ SHOP.TO│ 50     │ $80    │ $4,000   │ -$500     │-11%  │  │
│ │ VTI    │ 200    │ $220   │ $44,000  │ +$4,000   │+10%  │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                             │
│ ┌─ ETFs & Mutual Funds ($234,567) ───────────────────────┐  │
│ │ Symbol │ Units  │ NAV    │ Value    │ Gain/Loss │ %    │  │
│ │ VGRO   │ 1000   │ $25.50 │ $25,500  │ +$1,500   │+6.3% │  │
│ │ TDB902 │ 500    │ $45.20 │ $22,600  │ +$2,100   │+10%  │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                             │
│ ┌─ Cash & Cash Equivalents ($89,123) ────────────────────┐  │
│ │ Account        │ Institution │ Balance  │ Rate │ Type  │  │
│ │ Chequing       │ RBC         │ $5,000   │ 0.1% │ TFSA  │  │
│ │ High Interest  │ Tangerine   │ $25,000  │ 2.5% │ TFSA  │  │
│ │ GIC 1-Year     │ TD          │ $50,000  │ 4.2% │ RRSP  │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                             │
│ ┌─ Real Estate ($456,789) ────────────────────────────────┐  │
│ │ Property       │ Type        │ Value    │ Equity   │ %  │  │
│ │ 123 Main St    │ Primary     │ $650,000 │ $456,789 │70% │  │
│ │ 456 Oak Ave    │ Rental      │ $400,000 │ $280,000 │70% │  │
│ └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Liabilities Overview
```
┌─────────────────────────────────────────────────────────────┐
│ Liabilities & Debt                        [+ Add Liability] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─ Mortgages ($387,654) ──────────────────────────────────┐  │
│ │ Property       │ Balance  │ Rate │ Payment │ Term Left │  │
│ │ 123 Main St    │ $193,211 │ 3.2% │ $1,850  │ 18y 4m   │  │
│ │ 456 Oak Ave    │ $120,000 │ 4.1% │ $1,200  │ 12y 8m   │  │
│ │                │          │      │         │          │  │
│ │ ┌─ Amortization Schedule ─────────────────────────────┐ │  │
│ │ │ Year │ Principal │ Interest │ Balance              │ │  │
│ │ │ 2024 │ $12,450   │ $9,750   │ $180,761             │ │  │
│ │ │ 2025 │ $12,890   │ $9,310   │ $167,871             │ │  │
│ │ └─────────────────────────────────────────────────────┘ │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                             │
│ ┌─ Credit Cards ($12,345) ────────────────────────────────┐  │
│ │ Card           │ Balance │ Limit   │ Rate  │ Min Pay   │  │
│ │ RBC Visa       │ $3,456  │ $15,000 │ 19.9% │ $103      │  │
│ │ Amex Gold      │ $8,889  │ No Limit│ 19.9% │ $267      │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                             │
│ ┌─ Other Loans ($45,678) ─────────────────────────────────┐  │
│ │ Loan Type      │ Balance │ Rate │ Payment │ Term Left  │  │
│ │ Auto Loan      │ $23,456 │ 5.2% │ $450    │ 3y 2m     │  │
│ │ Line of Credit │ $22,222 │ 6.5% │ $200    │ Revolving │  │
│ └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 Canadian Account Classification
```
┌─────────────────────────────────────────────────────────────┐
│ Account Types & Tax Planning              [Optimize] [Help] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─ RRSP Accounts ($234,567) ──────────────────────────────┐  │
│ │ Institution    │ Balance  │ Contribution Room │ 2024    │  │
│ │ TD Direct      │ $156,789 │ $12,345          │ Used    │  │
│ │ Questrade      │ $77,778  │                  │         │  │
│ │                                                         │  │
│ │ ⚠ Contribution Room: $12,345 remaining for 2024        │  │
│ │ 💡 Recommendation: Max out RRSP before year-end        │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                             │
│ ┌─ TFSA Accounts ($89,123) ───────────────────────────────┐  │
│ │ Institution    │ Balance  │ Contribution Room │ 2024    │  │
│ │ RBC Direct     │ $45,000  │ $6,500           │ Used    │  │
│ │ Tangerine      │ $44,123  │                  │         │  │
│ │                                                         │  │
│ │ ✅ Contribution Room: $6,500 remaining for 2024        │  │
│ │ 💡 Recommendation: Consider TFSA for emergency fund    │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                             │
│ ┌─ Non-Registered ($345,678) ─────────────────────────────┐  │
│ │ Institution    │ Balance  │ Tax Implications │ Actions  │  │
│ │ Interactive    │ $200,000 │ Capital gains    │ Harvest  │  │
│ │ Questrade      │ $145,678 │ Dividend income  │ Track    │  │
│ │                                                         │  │
│ │ 📊 Tax-Loss Harvesting: $2,345 potential savings       │  │
│ │ 💡 Consider moving growth stocks to TFSA               │  │
│ └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.5 Mobile Dashboard Design
```
┌─────────────────────┐
│ ☰ NetWorth    🔔 👤 │
├─────────────────────┤
│                     │
│   Net Worth         │
│   $1,234,567        │
│   ↗ +2.3% ($28,456) │
│                     │
├─────────────────────┤
│ ┌─────┐ ┌─────┐     │
│ │Assets│ │Debts│     │
│ │$890K │ │$123K│     │
│ │ +5%  │ │ -2% │     │
│ └─────┘ └─────┘     │
├─────────────────────┤
│                     │
│ [Chart: 3-month     │
│  net worth trend]   │
│                     │
├─────────────────────┤
│ Quick Actions       │
│ [Add Asset]         │
│ [Record Payment]    │
│ [View Reports]      │
│                     │
├─────────────────────┤
│ Recent Activity     │
│ • AAPL +$1,234      │
│ • Mortgage -$2,100  │
│ • Dividend +$234    │
│                     │
└─────────────────────┘
```

## 3. User Experience Flow

### 3.1 Onboarding Flow
1. **Welcome Screen**: Value proposition and key features
2. **Account Creation**: Email, password, basic preferences
3. **Profile Setup**: Name, location, currency preference
4. **Account Type Selection**: Choose primary account types (RRSP, TFSA, etc.)
5. **First Asset Entry**: Guided tutorial for adding first investment
6. **Dashboard Tour**: Interactive walkthrough of main features

### 3.2 Asset Addition Flow
1. **Asset Type Selection**: Dropdown with categories (Stocks, ETFs, Real Estate, etc.)
2. **Symbol/Identifier Entry**: Auto-complete search for stocks/ETFs
3. **Quantity and Cost**: Purchase details and date
4. **Account Assignment**: Which account holds this asset
5. **Confirmation**: Review and save with success feedback

### 3.3 Report Generation Flow
1. **Report Type Selection**: Net worth, performance, tax, custom
2. **Date Range Selection**: Predefined ranges or custom dates
3. **Filter Options**: Account types, asset categories, etc.
4. **Preview**: Live preview of report as options are selected
5. **Export Options**: PDF, CSV, email delivery

## 4. Responsive Design Considerations

### 4.1 Breakpoints
- **Mobile**: 320px - 767px (single column layout)
- **Tablet**: 768px - 1023px (two-column layout)
- **Desktop**: 1024px+ (three-column layout with sidebar)

### 4.2 Mobile Optimizations
- **Touch-Friendly**: Minimum 44px touch targets
- **Simplified Navigation**: Hamburger menu with clear hierarchy
- **Swipe Gestures**: Swipe between account types, time periods
- **Progressive Disclosure**: Show summary first, details on tap
- **Offline Capability**: Cache recent data for offline viewing

### 4.3 Accessibility Features
- **High Contrast Mode**: Alternative color scheme for visual impairments
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Keyboard Navigation**: Full functionality without mouse
- **Font Scaling**: Support for user font size preferences
- **Color Blind Friendly**: Patterns and icons in addition to colors

## 5. Interactive Elements and Micro-interactions

### 5.1 Data Visualization
- **Hover Effects**: Show detailed tooltips on chart hover
- **Drill-Down**: Click chart segments to view detailed breakdowns
- **Time Range Selection**: Interactive slider for historical data
- **Comparison Mode**: Side-by-side comparison of time periods

### 5.2 Form Interactions
- **Real-time Validation**: Immediate feedback on form inputs
- **Auto-complete**: Smart suggestions for stock symbols, institutions
- **Progressive Enhancement**: Forms work without JavaScript
- **Save States**: Auto-save drafts of partially completed forms

### 5.3 Feedback and Notifications
- **Success Animations**: Subtle celebrations for positive actions
- **Loading States**: Clear progress indicators for data fetching
- **Error Handling**: Friendly error messages with recovery suggestions
- **Push Notifications**: Optional alerts for significant changes

## 6. Design System Components

### 6.1 Core Components
- **Cards**: Consistent styling for data containers
- **Buttons**: Primary, secondary, and tertiary button styles
- **Forms**: Input fields, dropdowns, checkboxes with validation states
- **Tables**: Responsive data tables with sorting and filtering
- **Charts**: Standardized chart components with consistent styling

### 6.2 Financial-Specific Components
- **Currency Display**: Consistent formatting for monetary values
- **Percentage Indicators**: Color-coded gains/losses with arrows
- **Account Badges**: Visual indicators for account types (RRSP, TFSA)
- **Asset Icons**: Recognizable icons for different asset types
- **Progress Bars**: Goal tracking and contribution room visualization

This UI/UX design specification provides a comprehensive foundation for creating an intuitive, accessible, and visually appealing net worth tracking application that specifically addresses the needs of Canadian users while maintaining professional financial application standards.
