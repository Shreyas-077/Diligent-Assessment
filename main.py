"""
E-commerce Data Pipeline - Main Script
Orchestrates the complete pipeline: data generation, database loading, and queries.
"""

import os
import sys
from data_generator import generate_data
from database_loader import load_to_sqlite
from queries import run_queries


def main():
    """Main pipeline execution."""
    print("=" * 70)
    print("E-COMMERCE DATA PIPELINE")
    print("=" * 70)
    
    try:
        # Step 1: Create data directory
        os.makedirs('data', exist_ok=True)
        
        # Step 2: Generate synthetic data
        generate_data()
        
        # Step 3: Load data into SQLite
        load_to_sqlite('ecommerce.db')
        
        # Step 4: Run queries
        run_queries('ecommerce.db')
        
        print("\n✅ Pipeline completed successfully!")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure all required files are present.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

