import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# Configure the Streamlit page
st.set_page_config(
    page_title="Personal Finance Analyzer",
    page_icon="💰",
    layout="wide"
)

# App Title
st.title("💰 Personal Finance Analyzer")
st.markdown("Analyze your bank statements and visualize where your money is going!")

# Category mapping function
def categorize_expense(description):
    """
    Automatically categorize expenses based on description keywords
    """
    description = description.lower()
    
    categories = {
        'Food & Dining': ['zomato', 'swiggy', 'restaurant', 'food', 'pizza', 'burger', 'coffee', 'starbucks', 'mcdonald', 'dominos', 'kfc', 'subway', 'cafe'],
        'Rent & Housing': ['rent', 'house', 'apartment', 'housing', 'maintenance'],
        'Transportation': ['uber', 'ola', 'taxi', 'petrol', 'fuel', 'metro', 'bus', 'train', 'flight', 'car', 'vehicle'],
        'Groceries': ['grocery', 'supermarket', 'bigbasket', 'reliance', 'dmart', 'fresh', 'vegetables'],
        'Entertainment': ['movie', 'cinema', 'pvr', 'inox', 'netflix', 'amazon prime', 'spotify', 'game'],
        'Utilities': ['electricity', 'gas', 'water', 'internet', 'wifi', 'mobile', 'phone', 'recharge'],
        'Shopping': ['shopping', 'amazon', 'flipkart', 'myntra', 'clothes', 'fashion', 'electronics'],
        'Health & Medical': ['medical', 'doctor', 'hospital', 'pharmacy', 'medicine', 'health', 'gym', 'fitness'],
        'Education': ['course', 'udemy', 'book', 'education', 'learning', 'school', 'college'],
        'Travel': ['travel', 'hotel', 'vacation', 'trip', 'booking', 'flight', 'train booking'],
        'Income': ['salary', 'credit', 'income', 'deposit', 'refund'],
        'Others': []
    }
    
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
    
    return 'Others'

# File upload section
st.header("📤 Upload Your Bank Statement")
uploaded_file = st.file_uploader(
    "Choose a CSV file", 
    type="csv",
    help="Upload your bank statement in CSV format. The file should contain Date, Description, Amount, and Type columns."
)

# Sample file creation for download (create in memory)
sample_data = """Date,Description,Amount,Type
2024-01-05,Zomato Food Delivery,450,Debit
2024-01-03,Monthly Rent Payment,15000,Debit
2024-01-04,Uber Ride,300,Debit
2024-01-06,Grocery Shopping - BigBasket,1200,Debit
2024-01-08,Movie Tickets - PVR,800,Debit
2024-01-10,Electricity Bill,2500,Debit
2024-01-12,McDonald's,350,Debit
2024-01-15,Flight Booking - Indigo,8500,Debit
2024-01-18,Salary Credit,50000,Credit
2024-01-20,Swiggy Order,600,Debit
2024-01-22,Internet Bill,1500,Debit
2024-01-25,Shopping - Amazon,2200,Debit
2024-01-28,Petrol,3000,Debit"""

st.download_button(
    label="📥 Download Sample CSV Format",
    data=sample_data,
    file_name="sample_statement.csv",
    mime="text/csv"
)

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display raw data preview
        st.subheader("📋 Data Preview")
        st.write("First 5 rows of your data:")
        st.dataframe(df.head())
        
        # Data validation and cleaning
        required_columns = ['Date', 'Description', 'Amount', 'Type']
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ Missing required columns. Your CSV should have: {', '.join(required_columns)}")
            st.stop()
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Remove rows with invalid dates
        df = df.dropna(subset=['Date'])
        
        # Add Month-Year column for analysis
        df['Month_Year'] = df['Date'].dt.to_period('M')
        
        # Categorize expenses
        df['Category'] = df['Description'].apply(categorize_expense)
        
        # Separate debits and credits
        expenses_df = df[df['Type'].str.lower() == 'debit'].copy()
        income_df = df[df['Type'].str.lower() == 'credit'].copy()
        
        # Summary Statistics
        st.header("📊 Financial Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_expenses = expenses_df['Amount'].sum()
            st.metric("💸 Total Expenses", f"₹{total_expenses:,.0f}")
        
        with col2:
            total_income = income_df['Amount'].sum()
            st.metric("💰 Total Income", f"₹{total_income:,.0f}")
        
        with col3:
            net_savings = total_income - total_expenses
            st.metric("💳 Net Savings", f"₹{net_savings:,.0f}")
        
        with col4:
            avg_expense = expenses_df['Amount'].mean()
            st.metric("📈 Avg Transaction", f"₹{avg_expense:,.0f}")
        
        # Category-wise spending analysis
        st.header("📊 Spending by Category")
        
        category_spending = expenses_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for category distribution
            fig_pie = px.pie(
                values=category_spending.values,
                names=category_spending.index,
                title="Expense Distribution by Category"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart for category spending
            fig_bar = px.bar(
                x=category_spending.values,
                y=category_spending.index,
                orientation='h',
                title="Total Spending by Category",
                labels={'x': 'Amount (₹)', 'y': 'Category'}
            )
            fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Category breakdown table
        st.subheader("💳 Category Breakdown")
        category_table = pd.DataFrame({
            'Category': category_spending.index,
            'Total Amount': category_spending.values,
            'Percentage': (category_spending.values / total_expenses * 100).round(1)
        })
        category_table['Total Amount'] = category_table['Total Amount'].apply(lambda x: f"₹{x:,.0f}")
        category_table['Percentage'] = category_table['Percentage'].apply(lambda x: f"{x}%")
        st.dataframe(category_table, use_container_width=True, hide_index=True)
        
        # Monthly trend analysis
        st.header("📆 Monthly Expense Trends")
        
        monthly_expenses = expenses_df.groupby(['Month_Year', 'Category'])['Amount'].sum().reset_index()
        monthly_expenses['Month_Year_Str'] = monthly_expenses['Month_Year'].astype(str)
        
        # Monthly trend line chart
        fig_trend = px.line(
            monthly_expenses,
            x='Month_Year_Str',
            y='Amount',
            color='Category',
            title='Monthly Spending Trends by Category',
            labels={'Month_Year_Str': 'Month', 'Amount': 'Amount (₹)'}
        )
        fig_trend.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Monthly total spending
        monthly_total = expenses_df.groupby('Month_Year')['Amount'].sum().reset_index()
        monthly_total['Month_Year_Str'] = monthly_total['Month_Year'].astype(str)
        
        fig_monthly_total = px.bar(
            monthly_total,
            x='Month_Year_Str',
            y='Amount',
            title='Total Monthly Spending',
            labels={'Month_Year_Str': 'Month', 'Amount': 'Amount (₹)'}
        )
        st.plotly_chart(fig_monthly_total, use_container_width=True)
        
        # Top expenses
        st.header("🏆 Top 10 Highest Expenses")
        top_expenses = expenses_df.nlargest(10, 'Amount')[['Date', 'Description', 'Amount', 'Category']]
        top_expenses['Amount'] = top_expenses['Amount'].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(top_expenses, use_container_width=True, hide_index=True)
        
        # Download processed data
        st.header("📥 Download Processed Data")
        
        # Create downloadable CSV
        processed_df = df[['Date', 'Description', 'Amount', 'Type', 'Category', 'Month_Year']]
        csv = processed_df.to_csv(index=False)
        
        st.download_button(
            label="📁 Download Analyzed Data as CSV",
            data=csv,
            file_name=f"analyzed_expenses_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        # Insights and recommendations
        st.header("💡 Insights & Recommendations")
        
        if not expenses_df.empty:
            top_category = category_spending.index[0]
            top_category_amount = category_spending.iloc[0]
            top_category_percentage = (top_category_amount / total_expenses * 100)
            
            insights = f"""
            **Key Insights from your spending:**
            
            1. 🎯 **Highest Spending Category**: {top_category} (₹{top_category_amount:,.0f} - {top_category_percentage:.1f}% of total expenses)
            
            2. 💰 **Savings Rate**: {((net_savings / total_income) * 100):.1f}% of your income
            
            3. 📊 **Number of Transactions**: {len(expenses_df)} expense transactions analyzed
            
            4. 📅 **Analysis Period**: {df['Date'].min().strftime('%B %Y')} to {df['Date'].max().strftime('%B %Y')}
            """
            
            if top_category_percentage > 40:
                insights += f"\n\n⚠️ **Recommendation**: Your {top_category} spending is quite high ({top_category_percentage:.1f}%). Consider reviewing and optimizing expenses in this category."
            
            if net_savings < 0:
                insights += f"\n\n🚨 **Alert**: Your expenses exceed your income by ₹{abs(net_savings):,.0f}. Consider reducing spending or increasing income."
            elif (net_savings / total_income) < 0.2:
                insights += f"\n\n💡 **Tip**: Try to save at least 20% of your income. Currently saving {((net_savings / total_income) * 100):.1f}%."
            
            st.markdown(insights)
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Please ensure your CSV file has the correct format with columns: Date, Description, Amount, Type")

else:
    st.info("👆 Please upload a CSV file to start analyzing your expenses!")
    
    # Show sample data format
    st.subheader("📝 Expected CSV Format")
    sample_data = pd.DataFrame({
        'Date': ['2024-01-05', '2024-01-03', '2024-01-04'],
        'Description': ['Zomato Food Delivery', 'Monthly Rent Payment', 'Uber Ride'],
        'Amount': [450, 15000, 300],
        'Type': ['Debit', 'Debit', 'Debit']
    })
    st.dataframe(sample_data, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Made with ❤️ by Urja Kohli | Personal Finance Analyzer v1.0
    </div>
    """,
    unsafe_allow_html=True
)
