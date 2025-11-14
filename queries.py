"""
SQL Queries Module
Contains optimized SQL queries for e-commerce analytics.
"""

import sqlite3
import pandas as pd


def get_top_users_by_spending(db_name='ecommerce.db', limit=5):
    """
    Query to get top N users by total spending.
    Joins users, orders, and order_items tables.
    
    Returns:
        DataFrame with columns: user_name, email, total_orders, total_spent
    """
    query = """
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
        LIMIT ?
    """
    
    conn = sqlite3.connect(db_name)
    try:
        df = pd.read_sql_query(query, conn, params=(limit,))
        return df
    finally:
        conn.close()


def get_product_sales_summary(db_name='ecommerce.db'):
    """
    Additional query: Get product sales summary with category.
    """
    query = """
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
    """
    
    conn = sqlite3.connect(db_name)
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()


def get_average_rating_by_category(db_name='ecommerce.db'):
    """
    Additional query: Get average rating by product category.
    """
    query = """
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
    """
    
    conn = sqlite3.connect(db_name)
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()


def run_queries(db_name='ecommerce.db'):
    """
    Main function to execute and display all queries.
    """
    print("\n" + "=" * 70)
    print("EXECUTING SQL QUERIES")
    print("=" * 70)
    
    # Query 1: Top users by spending
    print("\n📊 QUERY 1: Top 5 Users by Total Spending")
    print("-" * 70)
    top_users = get_top_users_by_spending(db_name, limit=5)
    print(top_users.to_string(index=False))
    
    # Query 2: Product sales summary
    print("\n\n📊 QUERY 2: Top 10 Products by Revenue")
    print("-" * 70)
    product_sales = get_product_sales_summary(db_name)
    print(product_sales.to_string(index=False))
    
    # Query 3: Average rating by category
    print("\n\n📊 QUERY 3: Average Rating by Product Category")
    print("-" * 70)
    category_ratings = get_average_rating_by_category(db_name)
    print(category_ratings.to_string(index=False))
    
    print("\n" + "=" * 70)
    print("✓ All queries executed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    run_queries()

