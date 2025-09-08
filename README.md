# Financial Dashboard

A comprehensive financial tracking web application built with Streamlit that helps you manage income, expenses, client invoices, and recurring costs in one place.

## Features

### 📊 Overview Dashboard
- Key financial metrics at a glance
- Monthly income vs expenses trend
- Expense category breakdown
- Quick KPI overview

### 💸 Income vs Expenses
- Monthly comparison charts
- Profit/loss tracking
- Visual trend analysis
- Monthly summary tables

### 🏷️ Expense Categories
- Categorized expense tracking
- Pie charts and bar charts
- Percentage breakdowns
- Category-wise analysis

### 💰 Income Allocations
- Automatic tax calculations (40%)
- Owner pay tracking ($3,000 every 2 weeks)
- Reinvestment allocation (20%)
- Net cushion calculation
- Income source breakdown

### 👥 Client Payment Tracking
- Invoice status tracking (Sent/Due/Paid/Overdue)
- Client-wise income analysis
- Outstanding payment monitoring
- Payment KPI dashboard

### 🔄 Recurring Expenses
- Monthly and annual recurring costs
- Frequency analysis
- Annual savings suggestions
- Due month tracking

### 📝 Data Entry
- Manual transaction entry with validation
- Client invoice management with date validation
- Recurring expense setup
- CSV data import support with column validation
- Input validation and error handling

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: This project requires Python 3.7+ and is compatible with Python 3.13.2

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Start by adding some sample data in the "Data Entry" tab, or the app will create sample data for demonstration

## Data Structure

The app uses three main CSV files stored in the `data/` directory:

- `transactions.csv`: Date, Type (Income/Expense), Category, Amount, Description
- `clients.csv`: Client, Project, Amount, Invoice Sent, Due Date, Status
- `recurring.csv`: Vendor, Frequency, Amount, Due Month, Notes

## Key Features

- **No Bank Integration**: Manual data entry and CSV import
- **Mobile Friendly**: Responsive design that works on all devices
- **Real-time Updates**: Data updates immediately when you add new entries
- **Visual Analytics**: Interactive charts and graphs
- **Automatic Calculations**: Tax allocations and recurring expense analysis
- **Clean UI**: Simple, intuitive interface focused on usability

## Customization

You can easily modify:
- Tax rates and allocation percentages in the income allocations section
- Owner pay frequency and amounts
- Expense categories
- Chart colors and styling
- Data validation rules

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Plotly
- NumPy

## Recent Improvements

- ✅ **Fixed dependency compatibility** - Updated requirements.txt for Python 3.13.2 compatibility
- ✅ **Enhanced error handling** - Replaced bare except clauses with specific exception handling
- ✅ **Added input validation** - Form validation for all data entry fields
- ✅ **Fixed division by zero** - Protected against division by zero in profit calculations
- ✅ **Added CSV import** - Bulk data import functionality with column validation
- ✅ **Improved data handling** - Better handling of empty datasets
- ✅ **Cache management** - Automatic cache clearing when data is updated

## Support

This is a self-contained application that runs locally on your machine. All data is stored in CSV files in the `data/` directory.
