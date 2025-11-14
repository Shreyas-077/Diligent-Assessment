"""
E-Commerce Insights Dashboard
A simple Streamlit-based frontend to visualize SQL query results.
"""

import streamlit as st
import pandas as pd
import os
from queries import get_top_users_by_spending, get_product_sales_summary, get_average_rating_by_category
from data_generator import generate_data
from database_loader import load_to_sqlite


# Page configuration
st.set_page_config(
    page_title="E-Commerce Insights Dashboard",
    page_icon="📊",
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
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def load_data(db_name='ecommerce.db'):
    """
    Load all dashboard data from the database.
    Returns a dictionary of DataFrames.
    """
    if not os.path.exists(db_name):
        st.error(f"❌ Database file '{db_name}' not found. Please run `python main.py` first to generate the data.")
        st.stop()
    
    try:
        data = {
            'top_users': get_top_users_by_spending(db_name, limit=10),
            'product_sales': get_product_sales_summary(db_name),
            'category_ratings': get_average_rating_by_category(db_name)
        }
        return data
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()


def format_currency(value):
    """Format number as currency."""
    return f"${value:,.2f}"


def regenerate_all_data():
    """
    Regenerate all synthetic data and reload into database.
    Returns True if successful, False otherwise.
    """
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Generate new data
        generate_data()
        
        # Load into database
        load_to_sqlite('ecommerce.db')
        
        return True
    except Exception as e:
        st.error(f"Error during data regeneration: {str(e)}")
        return False


def main():
    """Main dashboard function."""
    
    # Header
    st.markdown('<div class="main-header">📊 E-Commerce Insights Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Dashboard Controls")
        
        # Refresh button
        if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
            st.rerun()
        
        # Regenerate Data button
        st.markdown("---")
        if st.button("✨ Regenerate All Data", type="secondary", use_container_width=True):
            with st.spinner("🔄 Regenerating data... This may take a few seconds."):
                success = regenerate_all_data()
                if success:
                    st.success("✅ Data regenerated successfully! Refreshing dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Data regeneration failed. Please check the error message above.")
        
        st.markdown("---")
        st.markdown("### 📋 About")
        st.markdown("""
        This dashboard displays insights from the e-commerce database:
        - **Top Customers**: Highest spending users
        - **Product Sales**: Best performing products
        - **Category Ratings**: Average ratings by category
        """)
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        if st.button("📊 View All Queries", use_container_width=True):
            st.info("👆 Navigate to the **'📊 All Queries'** tab above to see all query results!")
    
    # Load data
    with st.spinner("Loading data from database..."):
        data = load_data()
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Top Customers", "🛍️ Product Sales", "⭐ Category Ratings", "📊 All Queries"])
    
    # Tab 1: Top Customers
    with tab1:
        st.header("Top Customers by Total Spending")
        st.markdown("---")
        
        if data['top_users'].empty:
            st.warning("No customer data available.")
        else:
            # Display summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Customers", len(data['top_users']))
            
            with col2:
                total_spent = data['top_users']['total_spent'].sum()
                st.metric("Total Revenue", format_currency(total_spent))
            
            with col3:
                avg_spent = data['top_users']['total_spent'].mean()
                st.metric("Average Spending", format_currency(avg_spent))
            
            with col4:
                max_orders = data['top_users']['total_orders'].max()
                st.metric("Max Orders", int(max_orders))
            
            st.markdown("---")
            
            # Display table with formatting
            df_display = data['top_users'].copy()
            df_display['total_spent'] = df_display['total_spent'].apply(format_currency)
            df_display.columns = ['Name', 'Email', 'Total Orders', 'Total Spent']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Download button
            csv = data['top_users'].to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="top_customers.csv",
                mime="text/csv"
            )
    
    # Tab 2: Product Sales
    with tab2:
        st.header("Top Products by Revenue")
        st.markdown("---")
        
        if data['product_sales'].empty:
            st.warning("No product sales data available.")
        else:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_revenue = data['product_sales']['total_revenue'].sum()
                st.metric("Total Revenue", format_currency(total_revenue))
            
            with col2:
                total_quantity = int(data['product_sales']['total_quantity_sold'].sum())
                st.metric("Total Units Sold", f"{total_quantity:,}")
            
            with col3:
                unique_products = len(data['product_sales'])
                st.metric("Products Listed", unique_products)
            
            st.markdown("---")
            
            # Display table
            df_display = data['product_sales'].copy()
            df_display['total_revenue'] = df_display['total_revenue'].apply(format_currency)
            df_display.columns = ['Product Name', 'Category', 'Times Ordered', 'Quantity Sold', 'Total Revenue']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Download button
            csv = data['product_sales'].to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="product_sales.csv",
                mime="text/csv"
            )
    
    # Tab 3: Category Ratings
    with tab3:
        st.header("Average Ratings by Product Category")
        st.markdown("---")
        
        if data['category_ratings'].empty:
            st.warning("No rating data available.")
        else:
            # Summary metrics
            col1, col2 = st.columns(2)
            
            with col1:
                avg_rating = data['category_ratings']['average_rating'].mean()
                st.metric("Overall Average Rating", f"{avg_rating:.2f} ⭐")
            
            with col2:
                total_reviews = int(data['category_ratings']['review_count'].sum())
                st.metric("Total Reviews", f"{total_reviews:,}")
            
            st.markdown("---")
            
            # Display table
            df_display = data['category_ratings'].copy()
            df_display['average_rating'] = df_display['average_rating'].apply(lambda x: f"{x:.2f} ⭐")
            df_display.columns = ['Category', 'Review Count', 'Average Rating']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Download button
            csv = data['category_ratings'].to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="category_ratings.csv",
                mime="text/csv"
            )
    
    # Tab 4: All Queries (Complete View)
    with tab4:
        st.header("📊 All Query Results")
        st.markdown("Complete view of all analytical queries executed on the e-commerce database.")
        st.markdown("---")
        
        # Query 1: Top 5 Users by Spending
        st.subheader("📊 QUERY 1: Top 5 Users by Total Spending")
        st.markdown("*Joins users and orders tables to identify highest-spending customers.*")
        
        if not data['top_users'].empty:
            top_5_users = get_top_users_by_spending('ecommerce.db', limit=5)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.metric("Total Customers Shown", len(top_5_users))
            with col2:
                total_spent = top_5_users['total_spent'].sum()
                st.metric("Combined Spending", format_currency(total_spent))
            
            # Display table
            df_display = top_5_users.copy()
            df_display['total_spent'] = df_display['total_spent'].apply(format_currency)
            df_display.columns = ['Name', 'Email', 'Total Orders', 'Total Spent']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            # Show SQL query
            with st.expander("🔍 View SQL Query"):
                st.code("""
SELECT 
    u.name AS user_name,
    u.email,
    COUNT(DISTINCT o.id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_spent
FROM 
    users u
INNER JOIN 
    orders o ON u.id = o.user_id
GROUP BY 
    u.id, u.name, u.email
ORDER BY 
    total_spent DESC
LIMIT 5
                """, language="sql")
            
            # Download button
            csv = top_5_users.to_csv(index=False)
            st.download_button(
                label="📥 Download Query 1 Results",
                data=csv,
                file_name="query1_top_users.csv",
                mime="text/csv",
                key="download_q1"
            )
        else:
            st.warning("No customer data available.")
        
        st.markdown("---")
        
        # Query 2: Product Sales Summary
        st.subheader("📊 QUERY 2: Top 10 Products by Revenue")
        st.markdown("*Shows best-selling products with revenue breakdown by category.*")
        
        if not data['product_sales'].empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                total_revenue = data['product_sales']['total_revenue'].sum()
                st.metric("Total Revenue", format_currency(total_revenue))
            with col2:
                total_quantity = int(data['product_sales']['total_quantity_sold'].sum())
                st.metric("Total Units Sold", f"{total_quantity:,}")
            with col3:
                st.metric("Products Listed", len(data['product_sales']))
            
            # Display table
            df_display = data['product_sales'].copy()
            df_display['total_revenue'] = df_display['total_revenue'].apply(format_currency)
            df_display.columns = ['Product Name', 'Category', 'Times Ordered', 'Quantity Sold', 'Total Revenue']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            # Show SQL query
            with st.expander("🔍 View SQL Query"):
                st.code("""
SELECT 
    p.name AS product_name,
    p.category,
    COUNT(oi.id) AS times_ordered,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.subtotal), 2) AS total_revenue
FROM 
    products p
INNER JOIN 
    order_items oi ON p.id = oi.product_id
GROUP BY 
    p.id, p.name, p.category
ORDER BY 
    total_revenue DESC
LIMIT 10
                """, language="sql")
            
            # Download button
            csv = data['product_sales'].to_csv(index=False)
            st.download_button(
                label="📥 Download Query 2 Results",
                data=csv,
                file_name="query2_product_sales.csv",
                mime="text/csv",
                key="download_q2"
            )
        else:
            st.warning("No product sales data available.")
        
        st.markdown("---")
        
        # Query 3: Average Rating by Category
        st.subheader("📊 QUERY 3: Average Rating by Product Category")
        st.markdown("*Displays average customer ratings grouped by product category.*")
        
        if not data['category_ratings'].empty:
            col1, col2 = st.columns(2)
            with col1:
                avg_rating = data['category_ratings']['average_rating'].mean()
                st.metric("Overall Average Rating", f"{avg_rating:.2f} ⭐")
            with col2:
                total_reviews = int(data['category_ratings']['review_count'].sum())
                st.metric("Total Reviews", f"{total_reviews:,}")
            
            # Display table
            df_display = data['category_ratings'].copy()
            df_display['average_rating'] = df_display['average_rating'].apply(lambda x: f"{x:.2f} ⭐")
            df_display.columns = ['Category', 'Review Count', 'Average Rating']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            # Show SQL query
            with st.expander("🔍 View SQL Query"):
                st.code("""
SELECT 
    p.category,
    COUNT(r.id) AS review_count,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM 
    products p
INNER JOIN 
    reviews r ON p.id = r.product_id
GROUP BY 
    p.category
ORDER BY 
    average_rating DESC
                """, language="sql")
            
            # Download button
            csv = data['category_ratings'].to_csv(index=False)
            st.download_button(
                label="📥 Download Query 3 Results",
                data=csv,
                file_name="query3_category_ratings.csv",
                mime="text/csv",
                key="download_q3"
            )
        else:
            st.warning("No rating data available.")
        
        st.markdown("---")
        st.success("✅ All queries executed successfully!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 1rem;'>"
        "📊 E-Commerce Insights Dashboard | Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

