import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="Financial Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .kpi-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .kpi-item {
        text-align: center;
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Data storage functions
@st.cache_data
def load_data():
    """Load or create sample data files"""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Sample transactions data
    transactions_file = os.path.join(data_dir, "transactions.csv")
    if not os.path.exists(transactions_file):
        sample_transactions = pd.DataFrame({
            'Date': ['2024-01-15', '2024-01-20', '2024-01-25', '2024-02-01', '2024-02-05'],
            'Type': ['Income', 'Expense', 'Income', 'Expense', 'Expense'],
            'Category': ['Client Work', 'Software', 'Digital Store', 'Meals', 'Subscriptions'],
            'Amount': [5000, 99, 1200, 45, 29.99],
            'Description': ['Project Alpha', 'Adobe Creative', 'E-book Sales', 'Business Lunch', 'Netflix']
        })
        sample_transactions.to_csv(transactions_file, index=False)
    
    # Sample client data
    clients_file = os.path.join(data_dir, "clients.csv")
    if not os.path.exists(clients_file):
        sample_clients = pd.DataFrame({
            'Client': ['ABC Corp', 'XYZ Inc', 'StartupCo'],
            'Project': ['Website Redesign', 'Mobile App', 'Consulting'],
            'Amount': [8000, 12000, 5000],
            'Invoice_Sent': ['2024-01-10', '2024-01-15', '2024-02-01'],
            'Due_Date': ['2024-02-10', '2024-02-15', '2024-03-01'],
            'Status': ['Paid', 'Due', 'Sent']
        })
        sample_clients.to_csv(clients_file, index=False)
    
    # Sample recurring expenses
    recurring_file = os.path.join(data_dir, "recurring.csv")
    if not os.path.exists(recurring_file):
        sample_recurring = pd.DataFrame({
            'Vendor': ['Adobe', 'Microsoft', 'AWS', 'Insurance'],
            'Frequency': ['Monthly', 'Annual', 'Monthly', 'Annual'],
            'Amount': [99, 1200, 50, 2400],
            'Due_Month': ['January', 'January', 'January', 'January'],
            'Notes': ['Creative Suite', 'Office 365', 'Cloud hosting', 'Business insurance']
        })
        sample_recurring.to_csv(recurring_file, index=False)
    
    return transactions_file, clients_file, recurring_file

def load_transactions(file_path):
    """Load transactions data"""
    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as e:
        st.warning(f"Error loading transactions data: {e}")
        return pd.DataFrame()

def load_clients(file_path):
    """Load clients data"""
    try:
        df = pd.read_csv(file_path)
        df['Invoice_Sent'] = pd.to_datetime(df['Invoice_Sent'])
        df['Due_Date'] = pd.to_datetime(df['Due_Date'])
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as e:
        st.warning(f"Error loading clients data: {e}")
        return pd.DataFrame()

def load_recurring(file_path):
    """Load recurring expenses data"""
    try:
        return pd.read_csv(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        st.warning(f"Error loading recurring expenses data: {e}")
        return pd.DataFrame()

# Main app
def main():
    st.markdown('<h1 class="main-header">💰 Financial Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data files
    transactions_file, clients_file, recurring_file = load_data()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📊 Overview", "💸 Income vs Expenses", "🏷️ Expense Categories", 
         "💰 Income Allocations", "👥 Client Tracking", "🔄 Recurring Expenses", "📝 Data Entry"]
    )
    
    if page == "📊 Overview":
        show_overview(transactions_file, clients_file, recurring_file)
    elif page == "💸 Income vs Expenses":
        show_income_expenses(transactions_file)
    elif page == "🏷️ Expense Categories":
        show_expense_categories(transactions_file)
    elif page == "💰 Income Allocations":
        show_income_allocations(transactions_file)
    elif page == "👥 Client Tracking":
        show_client_tracking(clients_file)
    elif page == "🔄 Recurring Expenses":
        show_recurring_expenses(recurring_file)
    elif page == "📝 Data Entry":
        show_data_entry(transactions_file, clients_file, recurring_file)

def show_overview(transactions_file, clients_file, recurring_file):
    """Show dashboard overview with key metrics"""
    st.header("📊 Dashboard Overview")
    
    # Load data
    transactions = load_transactions(transactions_file)
    clients = load_clients(clients_file)
    recurring = load_recurring(recurring_file)
    
    if transactions.empty:
        st.warning("No transaction data available. Please add some data in the Data Entry page.")
        return
    
    # Calculate key metrics
    current_month = datetime.now().strftime('%Y-%m')
    current_month_data = transactions[transactions['Date'].dt.to_period('M').astype(str) == current_month]
    
    monthly_income = current_month_data[current_month_data['Type'] == 'Income']['Amount'].sum()
    monthly_expenses = current_month_data[current_month_data['Type'] == 'Expense']['Amount'].sum()
    monthly_profit = monthly_income - monthly_expenses
    
    # Client metrics
    total_outstanding = clients[clients['Status'].isin(['Sent', 'Due'])]['Amount'].sum() if not clients.empty else 0
    overdue_count = len(clients[clients['Status'] == 'Overdue']) if not clients.empty else 0
    
    # Recurring expenses
    monthly_recurring = recurring[recurring['Frequency'] == 'Monthly']['Amount'].sum() if not recurring.empty else 0
    annual_recurring = recurring[recurring['Frequency'] == 'Annual']['Amount'].sum() if not recurring.empty else 0
    
    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Income", f"${monthly_income:,.2f}")
    
    with col2:
        st.metric("Monthly Expenses", f"${monthly_expenses:,.2f}")
    
    with col3:
        profit_margin = (monthly_profit/monthly_income*100) if monthly_income > 0 else 0
        st.metric("Monthly Profit", f"${monthly_profit:,.2f}", 
                 delta=f"{profit_margin:.1f}%" if monthly_income > 0 else None)
    
    with col4:
        st.metric("Outstanding Invoices", f"${total_outstanding:,.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly trend
        monthly_summary = transactions.groupby([transactions['Date'].dt.to_period('M'), 'Type'])['Amount'].sum().unstack(fill_value=0)
        if not monthly_summary.empty:
            # Convert Period index to string for JSON serialization
            monthly_summary.index = monthly_summary.index.astype(str)
            fig = px.line(monthly_summary.reset_index(), x='Date', y=['Income', 'Expense'], 
                         title="Monthly Income vs Expenses Trend")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Expense categories
        expense_data = transactions[transactions['Type'] == 'Expense']
        if not expense_data.empty:
            category_summary = expense_data.groupby('Category')['Amount'].sum().sort_values(ascending=False)
            fig = px.pie(values=category_summary.values, names=category_summary.index, 
                        title="Expenses by Category")
            st.plotly_chart(fig, use_container_width=True)

def show_income_expenses(transactions_file):
    """Show income vs expenses analysis"""
    st.header("💸 Income vs Expenses")
    
    transactions = load_transactions(transactions_file)
    
    if transactions.empty:
        st.warning("No transaction data available.")
        return
    
    # Monthly comparison chart
    monthly_data = transactions.groupby([transactions['Date'].dt.to_period('M'), 'Type'])['Amount'].sum().unstack(fill_value=0)
    monthly_data['Profit'] = monthly_data.get('Income', 0) - monthly_data.get('Expense', 0)
    
    # Convert Period index to string for JSON serialization
    monthly_data.index = monthly_data.index.astype(str)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Income', x=monthly_data.index, y=monthly_data.get('Income', 0), marker_color='green'))
    fig.add_trace(go.Bar(name='Expenses', x=monthly_data.index, y=monthly_data.get('Expense', 0), marker_color='red'))
    fig.add_trace(go.Scatter(name='Profit', x=monthly_data.index, y=monthly_data['Profit'], 
                            mode='lines+markers', line=dict(color='blue', width=3)))
    
    fig.update_layout(title="Monthly Income vs Expenses", xaxis_title="Month", yaxis_title="Amount ($)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Profit/Loss table
    st.subheader("Monthly Profit/Loss Summary")
    profit_loss_df = monthly_data.copy()
    # Avoid division by zero
    income_values = profit_loss_df.get('Income', 0)
    profit_loss_df['Profit_Margin'] = np.where(
        income_values > 0, 
        (profit_loss_df['Profit'] / income_values * 100).round(2),
        0
    )
    profit_loss_df = profit_loss_df.round(2)
    st.dataframe(profit_loss_df, use_container_width=True)

def show_expense_categories(transactions_file):
    """Show expense categorization analysis"""
    st.header("🏷️ Expense Categories")
    
    transactions = load_transactions(transactions_file)
    expenses = transactions[transactions['Type'] == 'Expense']
    
    if expenses.empty:
        st.warning("No expense data available.")
        return
    
    # Category breakdown
    category_summary = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    total_expenses = category_summary.sum()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        fig = px.pie(values=category_summary.values, names=category_summary.index, 
                    title="Expenses by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Bar chart
        fig = px.bar(x=category_summary.index, y=category_summary.values, 
                    title="Expenses by Category")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Category table with percentages
    st.subheader("Category Breakdown")
    category_df = pd.DataFrame({
        'Category': category_summary.index,
        'Amount': category_summary.values,
        'Percentage': (category_summary.values / total_expenses * 100).round(2)
    })
    st.dataframe(category_df, use_container_width=True)

def show_income_allocations(transactions_file):
    """Show income breakdown and allocations"""
    st.header("💰 Income Allocations")
    
    transactions = load_transactions(transactions_file)
    income_data = transactions[transactions['Type'] == 'Income']
    
    if income_data.empty:
        st.warning("No income data available.")
        return
    
    # Calculate YTD income
    current_year = datetime.now().year
    ytd_income = income_data[income_data['Date'].dt.year == current_year]['Amount'].sum()
    
    # Allocation rules
    tax_rate = 0.40
    reinvestment_rate = 0.20
    owner_pay_frequency = 14  # days
    owner_pay_amount = 3000
    
    # Calculate allocations
    taxes_set_aside = ytd_income * tax_rate
    reinvestment = ytd_income * reinvestment_rate
    
    # Calculate owner pay (every 2 weeks)
    days_in_year = 365
    pay_periods = days_in_year / owner_pay_frequency
    owner_pay_total = pay_periods * owner_pay_amount
    
    # Net cushion
    net_cushion = ytd_income - taxes_set_aside - reinvestment - owner_pay_total
    
    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Taxes Set Aside", f"${taxes_set_aside:,.2f}", f"{tax_rate*100}%")
    
    with col2:
        st.metric("Owner Pay Total", f"${owner_pay_total:,.2f}")
    
    with col3:
        st.metric("Reinvestment", f"${reinvestment:,.2f}", f"{reinvestment_rate*100}%")
    
    with col4:
        st.metric("Net Cushion", f"${net_cushion:,.2f}")
    
    # Allocation pie chart
    allocation_data = {
        'Taxes': taxes_set_aside,
        'Owner Pay': owner_pay_total,
        'Reinvestment': reinvestment,
        'Net Cushion': net_cushion
    }
    
    fig = px.pie(values=list(allocation_data.values()), names=list(allocation_data.keys()), 
                title="YTD Income Allocations")
    st.plotly_chart(fig, use_container_width=True)
    
    # Income sources breakdown
    st.subheader("Income Sources")
    income_sources = income_data.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    fig = px.bar(x=income_sources.index, y=income_sources.values, 
                title="Income by Source")
    st.plotly_chart(fig, use_container_width=True)

def show_client_tracking(clients_file):
    """Show client payment tracking"""
    st.header("👥 Client Payment Tracking")
    
    clients = load_clients(clients_file)
    
    if clients.empty:
        st.warning("No client data available.")
        return
    
    # KPI counts
    status_counts = clients['Status'].value_counts()
    total_amount = clients['Amount'].sum()
    paid_amount = clients[clients['Status'] == 'Paid']['Amount'].sum()
    outstanding_amount = clients[clients['Status'].isin(['Sent', 'Due'])]['Amount'].sum()
    overdue_amount = clients[clients['Status'] == 'Overdue']['Amount'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Invoices", len(clients), f"${total_amount:,.2f}")
    
    with col2:
        st.metric("Paid", status_counts.get('Paid', 0), f"${paid_amount:,.2f}")
    
    with col3:
        st.metric("Outstanding", status_counts.get('Sent', 0) + status_counts.get('Due', 0), f"${outstanding_amount:,.2f}")
    
    with col4:
        st.metric("Overdue", status_counts.get('Overdue', 0), f"${overdue_amount:,.2f}")
    
    # Client table
    st.subheader("Invoice Tracker")
    st.dataframe(clients, use_container_width=True)
    
    # Income per client chart
    st.subheader("Income per Client YTD")
    client_income = clients[clients['Status'] == 'Paid'].groupby('Client')['Amount'].sum().sort_values(ascending=False)
    if not client_income.empty:
        fig = px.bar(x=client_income.index, y=client_income.values, 
                    title="Paid Income by Client")
        st.plotly_chart(fig, use_container_width=True)

def show_recurring_expenses(recurring_file):
    """Show recurring expense overview"""
    st.header("🔄 Recurring Expenses")
    
    recurring = load_recurring(recurring_file)
    
    if recurring.empty:
        st.warning("No recurring expense data available.")
        return
    
    # Calculate totals
    monthly_total = recurring[recurring['Frequency'] == 'Monthly']['Amount'].sum()
    annual_total = recurring[recurring['Frequency'] == 'Annual']['Amount'].sum()
    annual_equivalent = monthly_total * 12 + annual_total
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Monthly Recurring", f"${monthly_total:,.2f}")
    
    with col2:
        st.metric("Annual Recurring", f"${annual_total:,.2f}")
    
    with col3:
        st.metric("Annual Equivalent", f"${annual_equivalent:,.2f}")
    
    # Recurring expenses table
    st.subheader("All Recurring Expenses")
    st.dataframe(recurring, use_container_width=True)
    
    # Frequency analysis
    st.subheader("Frequency Analysis")
    freq_analysis = recurring.groupby('Frequency')['Amount'].sum()
    fig = px.pie(values=freq_analysis.values, names=freq_analysis.index, 
                title="Recurring Expenses by Frequency")
    st.plotly_chart(fig, use_container_width=True)
    
    # Annual savings suggestion
    monthly_items = recurring[recurring['Frequency'] == 'Monthly']
    if len(monthly_items) > 0:
        st.subheader("💡 Annual Savings Suggestions")
        for _, item in monthly_items.iterrows():
            annual_savings = item['Amount'] * 12 * 0.1  # Assume 10% savings with annual payment
            if annual_savings > 50:  # Only suggest if savings > $50
                st.info(f"Consider annual payment for {item['Vendor']}: Save ~${annual_savings:.2f}/year")

def show_data_entry(transactions_file, clients_file, recurring_file):
    """Show data entry forms"""
    st.header("📝 Data Entry")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Transactions", "Clients", "Recurring Expenses", "CSV Import"])
    
    with tab1:
        st.subheader("Add Transaction")
        with st.form("transaction_form"):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date", datetime.now())
                trans_type = st.selectbox("Type", ["Income", "Expense"])
                amount = st.number_input("Amount", min_value=0.0, step=0.01)
            with col2:
                category = st.text_input("Category")
                description = st.text_input("Description")
            
            if st.form_submit_button("Add Transaction"):
                # Validate input
                if not category.strip():
                    st.error("Category cannot be empty!")
                elif not description.strip():
                    st.error("Description cannot be empty!")
                elif amount <= 0:
                    st.error("Amount must be greater than 0!")
                else:
                    # Add to CSV
                    new_row = pd.DataFrame({
                        'Date': [date],
                        'Type': [trans_type],
                        'Category': [category.strip()],
                        'Amount': [amount],
                        'Description': [description.strip()]
                    })
                    
                    existing_data = load_transactions(transactions_file)
                    updated_data = pd.concat([existing_data, new_row], ignore_index=True)
                    updated_data.to_csv(transactions_file, index=False)
                    st.cache_data.clear()  # Clear cache to refresh data
                    st.success("Transaction added successfully!")
                    st.rerun()
    
    with tab2:
        st.subheader("Add Client Invoice")
        with st.form("client_form"):
            col1, col2 = st.columns(2)
            with col1:
                client = st.text_input("Client Name")
                project = st.text_input("Project")
                amount = st.number_input("Amount", min_value=0.0, step=0.01)
            with col2:
                invoice_sent = st.date_input("Invoice Sent Date", datetime.now())
                due_date = st.date_input("Due Date", datetime.now() + timedelta(days=30))
                status = st.selectbox("Status", ["Sent", "Due", "Paid", "Overdue"])
            
            if st.form_submit_button("Add Client"):
                # Validate input
                if not client.strip():
                    st.error("Client name cannot be empty!")
                elif not project.strip():
                    st.error("Project name cannot be empty!")
                elif amount <= 0:
                    st.error("Amount must be greater than 0!")
                elif due_date <= invoice_sent:
                    st.error("Due date must be after invoice sent date!")
                else:
                    new_row = pd.DataFrame({
                        'Client': [client.strip()],
                        'Project': [project.strip()],
                        'Amount': [amount],
                        'Invoice_Sent': [invoice_sent],
                        'Due_Date': [due_date],
                        'Status': [status]
                    })
                    
                    existing_data = load_clients(clients_file)
                    updated_data = pd.concat([existing_data, new_row], ignore_index=True)
                    updated_data.to_csv(clients_file, index=False)
                    st.cache_data.clear()  # Clear cache to refresh data
                    st.success("Client added successfully!")
                    st.rerun()
    
    with tab3:
        st.subheader("Add Recurring Expense")
        with st.form("recurring_form"):
            col1, col2 = st.columns(2)
            with col1:
                vendor = st.text_input("Vendor")
                frequency = st.selectbox("Frequency", ["Monthly", "Annual"])
                amount = st.number_input("Amount", min_value=0.0, step=0.01)
            with col2:
                due_month = st.selectbox("Due Month", 
                    ["January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"])
                notes = st.text_input("Notes")
            
            if st.form_submit_button("Add Recurring Expense"):
                # Validate input
                if not vendor.strip():
                    st.error("Vendor name cannot be empty!")
                elif amount <= 0:
                    st.error("Amount must be greater than 0!")
                else:
                    new_row = pd.DataFrame({
                        'Vendor': [vendor.strip()],
                        'Frequency': [frequency],
                        'Amount': [amount],
                        'Due_Month': [due_month],
                        'Notes': [notes.strip() if notes else ""]
                    })
                    
                    existing_data = load_recurring(recurring_file)
                    updated_data = pd.concat([existing_data, new_row], ignore_index=True)
                    updated_data.to_csv(recurring_file, index=False)
                    st.cache_data.clear()  # Clear cache to refresh data
                    st.success("Recurring expense added successfully!")
                    st.rerun()
    
    with tab4:
        st.subheader("Import CSV Data")
        st.write("Upload CSV files to import data into the system.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Transactions CSV**")
            st.write("Columns: Date, Type, Category, Amount, Description")
            uploaded_transactions = st.file_uploader("Choose transactions CSV", type="csv", key="transactions_csv")
            if uploaded_transactions is not None:
                try:
                    df = pd.read_csv(uploaded_transactions)
                    # Validate required columns
                    required_cols = ['Date', 'Type', 'Category', 'Amount', 'Description']
                    if all(col in df.columns for col in required_cols):
                        existing_data = load_transactions(transactions_file)
                        updated_data = pd.concat([existing_data, df], ignore_index=True)
                        updated_data.to_csv(transactions_file, index=False)
                        st.cache_data.clear()
                        st.success(f"Successfully imported {len(df)} transactions!")
                    else:
                        st.error(f"CSV must contain columns: {', '.join(required_cols)}")
                except Exception as e:
                    st.error(f"Error importing transactions: {e}")
        
        with col2:
            st.write("**Clients CSV**")
            st.write("Columns: Client, Project, Amount, Invoice_Sent, Due_Date, Status")
            uploaded_clients = st.file_uploader("Choose clients CSV", type="csv", key="clients_csv")
            if uploaded_clients is not None:
                try:
                    df = pd.read_csv(uploaded_clients)
                    # Validate required columns
                    required_cols = ['Client', 'Project', 'Amount', 'Invoice_Sent', 'Due_Date', 'Status']
                    if all(col in df.columns for col in required_cols):
                        existing_data = load_clients(clients_file)
                        updated_data = pd.concat([existing_data, df], ignore_index=True)
                        updated_data.to_csv(clients_file, index=False)
                        st.cache_data.clear()
                        st.success(f"Successfully imported {len(df)} clients!")
                    else:
                        st.error(f"CSV must contain columns: {', '.join(required_cols)}")
                except Exception as e:
                    st.error(f"Error importing clients: {e}")
        
        with col3:
            st.write("**Recurring Expenses CSV**")
            st.write("Columns: Vendor, Frequency, Amount, Due_Month, Notes")
            uploaded_recurring = st.file_uploader("Choose recurring CSV", type="csv", key="recurring_csv")
            if uploaded_recurring is not None:
                try:
                    df = pd.read_csv(uploaded_recurring)
                    # Validate required columns
                    required_cols = ['Vendor', 'Frequency', 'Amount', 'Due_Month']
                    if all(col in df.columns for col in required_cols):
                        existing_data = load_recurring(recurring_file)
                        updated_data = pd.concat([existing_data, df], ignore_index=True)
                        updated_data.to_csv(recurring_file, index=False)
                        st.cache_data.clear()
                        st.success(f"Successfully imported {len(df)} recurring expenses!")
                    else:
                        st.error(f"CSV must contain columns: {', '.join(required_cols)}")
                except Exception as e:
                    st.error(f"Error importing recurring expenses: {e}")

if __name__ == "__main__":
    main()
