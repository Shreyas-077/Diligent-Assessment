# E-Commerce Data Pipeline

A complete Python-based data pipeline that generates synthetic e-commerce data, loads it into SQLite, and performs analytical queries.

## 📋 Project Overview

This project demonstrates a full data pipeline workflow:
1. **Data Generation**: Creates realistic synthetic e-commerce data using Faker
2. **Data Storage**: Saves data to CSV files and loads into SQLite database
3. **Data Analysis**: Executes optimized SQL queries with joins across multiple tables

## 🏗️ Project Structure

```
Diligent-ASLDC/
│
├── data/                      # Generated CSV files (created at runtime)
│   ├── users.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── reviews.csv
│
├── data_generator.py          # Synthetic data generation module
├── database_loader.py         # SQLite database ingestion module
├── queries.py                 # SQL query execution module
├── main.py                    # Main pipeline orchestrator
├── dashboard.py               # Streamlit dashboard frontend
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── README.md                 # This file
└── ecommerce.db              # SQLite database (created at runtime)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Pipeline

**Option 1: Run the complete pipeline (recommended)**
```bash
python main.py
```

**Option 2: Run individual modules**

1. Generate data:
   ```bash
   python data_generator.py
   ```

2. Load to database:
   ```bash
   python database_loader.py
   ```

3. Run queries:
   ```bash
   python queries.py
   ```

**Option 3: Launch the Interactive Dashboard**
```bash
streamlit run dashboard.py
```
This will open a browser-based dashboard showing all query results in an interactive format.

## 📊 Database Schema

The SQLite database contains 5 tables with the following relationships:

- **users**: Customer information
  - `id` (PK), `name`, `email`, `signup_date`

- **products**: Product catalog
  - `id` (PK), `name`, `category`, `price`

- **orders**: Customer orders
  - `id` (PK), `user_id` (FK → users), `order_date`, `total_amount`

- **order_items**: Individual items in each order
  - `id` (PK), `order_id` (FK → orders), `product_id` (FK → products), `quantity`, `subtotal`

- **reviews**: Product reviews by users
  - `id` (PK), `user_id` (FK → users), `product_id` (FK → products), `rating`, `review_text`, `review_date`

## 🔍 Sample Query Output

### Query 1: Top 5 Users by Total Spending

This query joins `users`, `orders`, and `order_items` tables to identify the highest-spending customers:

```sql
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
```

**Sample Output:**
```
user_name              email                    total_orders  total_spent
---------------------  -----------------------  ------------  -----------
John Smith             john.smith@email.com     8             4523.45
Jane Doe               jane.doe@email.com       6             3891.23
Bob Johnson            bob.johnson@email.com    7             3456.78
Alice Williams         alice.w@email.com        5             3123.45
Charlie Brown          charlie.b@email.com      4             2890.12
```

### Additional Queries

The pipeline also includes:
- **Top 10 Products by Revenue**: Shows best-selling products with revenue totals
- **Average Rating by Category**: Displays average customer ratings grouped by product category

## ⚡ Performance

- **Data Generation**: ~2-3 seconds (100 users, 50 products, 200 orders)
- **Database Loading**: ~1-2 seconds
- **Query Execution**: <1 second (with indexes)
- **Total Pipeline Time**: ~5-10 seconds

## 🛠️ Technical Details

### Dependencies

- **Faker** (v24.0.0): Generates realistic synthetic data
- **Pandas** (v2.1.4): Data manipulation and CSV handling
- **Streamlit** (v1.29.0): Interactive web dashboard framework

### Features

- ✅ Realistic synthetic data generation with proper relationships
- ✅ Foreign key constraints and data validation
- ✅ Optimized SQL queries with indexes
- ✅ Modular, maintainable code structure
- ✅ Comprehensive error handling
- ✅ Clean console output formatting

### Data Volume

By default, the pipeline generates:
- 100 users
- 50 products
- 200 orders
- ~400-600 order items
- 150 reviews

You can modify these values in `data_generator.py` if needed.

## 🎨 Interactive Dashboard

The project includes a Streamlit-based dashboard (`dashboard.py`) that provides a clean, interactive interface to visualize query results.

### Features:
- **Top Customers Tab**: Displays top 10 customers by spending with summary metrics
- **Product Sales Tab**: Shows best-selling products with revenue breakdown
- **Category Ratings Tab**: Displays average ratings grouped by product category
- **Refresh Button**: Reload data from the database
- **CSV Export**: Download any table as CSV
- **Summary Metrics**: Key statistics displayed at the top of each tab

### Running the Dashboard:
```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`.

## 📝 Notes

- The database file (`ecommerce.db`) is recreated each run
- CSV files in the `data/` directory are overwritten on each generation
- All random data uses a seed (42) for reproducibility
- Foreign key relationships ensure data integrity
- The dashboard requires the database to exist (run `python main.py` first)

## 🤝 Contributing

Feel free to extend this pipeline with:
- Additional data tables
- More complex analytical queries
- Data visualization
- API endpoints
- Docker containerization

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

**Developed with Cursor IDE** 🚀

