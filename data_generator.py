"""
Synthetic E-commerce Data Generator
Generates realistic data for users, products, orders, order_items, and reviews.
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

fake = Faker()
Faker.seed(42)  # For reproducibility
random.seed(42)


def generate_users(num_users=100):
    """Generate synthetic user data."""
    users = []
    for i in range(1, num_users + 1):
        signup_date = fake.date_between(start_date='-2y', end_date='today')
        users.append({
            'id': i,
            'name': fake.name(),
            'email': fake.email(),
            'signup_date': signup_date.strftime('%Y-%m-%d')
        })
    return pd.DataFrame(users)


def generate_products(num_products=50):
    """Generate synthetic product data."""
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 
                  'Sports', 'Toys', 'Beauty', 'Food & Beverages']
    products = []
    for i in range(1, num_products + 1):
        products.append({
            'id': i,
            'name': fake.catch_phrase(),
            'category': random.choice(categories),
            'price': round(random.uniform(10.0, 500.0), 2)
        })
    return pd.DataFrame(products)


def generate_orders(users_df, num_orders=200):
    """Generate synthetic order data."""
    orders = []
    user_ids = users_df['id'].tolist()
    
    for i in range(1, num_orders + 1):
        user_id = random.choice(user_ids)
        # Order date should be after user signup date
        user_signup = datetime.strptime(
            users_df[users_df['id'] == user_id]['signup_date'].values[0], 
            '%Y-%m-%d'
        )
        order_date = fake.date_between(
            start_date=user_signup, 
            end_date='today'
        )
        # Total amount will be calculated from order_items, but we'll estimate here
        total_amount = round(random.uniform(25.0, 1000.0), 2)
        
        orders.append({
            'id': i,
            'user_id': user_id,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'total_amount': total_amount
        })
    return pd.DataFrame(orders)


def generate_order_items(orders_df, products_df, num_items_per_order_range=(1, 5)):
    """Generate synthetic order items data."""
    order_items = []
    product_ids = products_df['id'].tolist()
    item_id = 1
    
    for _, order in orders_df.iterrows():
        num_items = random.randint(*num_items_per_order_range)
        selected_products = random.sample(product_ids, min(num_items, len(product_ids)))
        
        order_total = 0
        for product_id in selected_products:
            product = products_df[products_df['id'] == product_id].iloc[0]
            quantity = random.randint(1, 5)
            subtotal = round(product['price'] * quantity, 2)
            order_total += subtotal
            
            order_items.append({
                'id': item_id,
                'order_id': order['id'],
                'product_id': product_id,
                'quantity': quantity,
                'subtotal': subtotal
            })
            item_id += 1
        
        # Update order total_amount to match actual order_items
        orders_df.loc[orders_df['id'] == order['id'], 'total_amount'] = round(order_total, 2)
    
    return pd.DataFrame(order_items), orders_df


def generate_reviews(users_df, products_df, orders_df, order_items_df, num_reviews=150):
    """Generate synthetic review data."""
    reviews = []
    user_ids = users_df['id'].tolist()
    product_ids = products_df['id'].tolist()
    
    # Get products that were actually ordered
    ordered_products = set(order_items_df['product_id'].unique())
    ordered_users = set(orders_df['user_id'].unique())
    
    for i in range(1, num_reviews + 1):
        user_id = random.choice(list(ordered_users))
        product_id = random.choice(list(ordered_products))
        
        # Review date should be after order date if user ordered this product
        user_orders = orders_df[orders_df['user_id'] == user_id]
        if not user_orders.empty:
            latest_order_date = datetime.strptime(
                user_orders['order_date'].max(), 
                '%Y-%m-%d'
            )
            review_date = fake.date_between(
                start_date=latest_order_date, 
                end_date='today'
            )
        else:
            review_date = fake.date_between(start_date='-1y', end_date='today')
        
        reviews.append({
            'id': i,
            'user_id': user_id,
            'product_id': product_id,
            'rating': random.randint(1, 5),
            'review_text': fake.text(max_nb_chars=200),
            'review_date': review_date.strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(reviews)


def save_to_csv(df, filename):
    """Save DataFrame to CSV file."""
    df.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f"✓ Saved {len(df)} records to {filename}")


def generate_data():
    """
    Main function to generate all synthetic e-commerce data.
    Returns dictionary of DataFrames.
    """
    print("Generating synthetic e-commerce data...")
    print("-" * 50)
    
    # Generate base data
    print("1. Generating users...")
    users_df = generate_users(num_users=100)
    
    print("2. Generating products...")
    products_df = generate_products(num_products=50)
    
    print("3. Generating orders...")
    orders_df = generate_orders(users_df, num_orders=200)
    
    print("4. Generating order items...")
    order_items_df, orders_df = generate_order_items(orders_df, products_df)
    
    print("5. Generating reviews...")
    reviews_df = generate_reviews(users_df, products_df, orders_df, order_items_df, num_reviews=150)
    
    # Save to CSV files
    print("\nSaving data to CSV files...")
    print("-" * 50)
    save_to_csv(users_df, 'data/users.csv')
    save_to_csv(products_df, 'data/products.csv')
    save_to_csv(orders_df, 'data/orders.csv')
    save_to_csv(order_items_df, 'data/order_items.csv')
    save_to_csv(reviews_df, 'data/reviews.csv')
    
    print("\n✓ Data generation complete!")
    print("-" * 50)
    
    return {
        'users': users_df,
        'products': products_df,
        'orders': orders_df,
        'order_items': order_items_df,
        'reviews': reviews_df
    }


if __name__ == "__main__":
    import os
    os.makedirs('data', exist_ok=True)
    generate_data()

