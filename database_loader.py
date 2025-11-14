"""
SQLite Database Loader
Ingests CSV files into SQLite database with proper schema and constraints.
"""

import sqlite3
import pandas as pd
import os


def create_schema(cursor):
    """Create database schema with proper relationships."""
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            signup_date DATE NOT NULL
        )
    """)
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL CHECK(price > 0)
        )
    """)
    
    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_amount REAL NOT NULL CHECK(total_amount >= 0),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Order items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            subtotal REAL NOT NULL CHECK(subtotal >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # Reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            review_text TEXT,
            review_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    print("✓ Database schema created")


def load_csv_to_table(cursor, csv_file, table_name, conn):
    """Load CSV file into SQLite table."""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    
    df = pd.read_csv(csv_file)
    
    # Clear existing data if any
    cursor.execute(f"DELETE FROM {table_name}")
    
    # Insert data
    df.to_sql(table_name, conn, if_exists='append', index=False)
    
    # Verify count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"✓ Loaded {count} records into {table_name}")
    
    return count


def create_indexes(cursor):
    """Create indexes for better query performance."""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id)",
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    print("✓ Indexes created for optimized queries")


def load_to_sqlite(db_name='ecommerce.db'):
    """
    Main function to load all CSV files into SQLite database.
    """
    print("\nLoading data into SQLite database...")
    print("-" * 50)
    
    # Remove existing database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"✓ Removed existing {db_name}")
    
    # Connect to database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Create schema
        create_schema(cursor)
        
        # Load data in correct order (respecting foreign keys)
        load_csv_to_table(cursor, 'data/users.csv', 'users', conn)
        load_csv_to_table(cursor, 'data/products.csv', 'products', conn)
        load_csv_to_table(cursor, 'data/orders.csv', 'orders', conn)
        load_csv_to_table(cursor, 'data/order_items.csv', 'order_items', conn)
        load_csv_to_table(cursor, 'data/reviews.csv', 'reviews', conn)
        
        # Create indexes
        create_indexes(cursor)
        
        # Commit changes
        conn.commit()
        
        print("\n✓ Database loading complete!")
        print(f"✓ Database saved as {db_name}")
        print("-" * 50)
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


if __name__ == "__main__":
    load_to_sqlite()

