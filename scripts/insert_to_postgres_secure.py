"""
Task 3: PostgreSQL Data Insertion Script (FIXED - No Duplicates)
"""

import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': 'localhost',
    'port': 5434,
    'database': 'bank_reviews',
    'user': 'postgres',
    'password': os.getenv('DB_PASSWORD')
}

def test_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Database connection successful")
        conn.close()
        return True
    except OperationalError as e:
        print(f"❌ Connection failed: {e}")
        return False

def clear_existing_data():
    """Clear existing reviews before inserting fresh data"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reviews;")
        conn.commit()
        print("✅ Cleared existing reviews from database")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ Could not clear data: {e}")

def insert_data():
    try:
        # Load sentiment results
        sentiment_df = pd.read_csv('data/processed/sentiment_results.csv')
        print(f"✅ Loaded {len(sentiment_df)} sentiment results")
        
        # Load cleaned reviews
        cleaned_df = pd.read_csv('data/raw/cleaned_reviews.csv')
        print(f"✅ Loaded {len(cleaned_df)} cleaned reviews")
        
        # Add a unique row index to cleaned_df for proper merging
        cleaned_df['row_id'] = range(len(cleaned_df))
        
        # Merge on review text - but keep only first match
        df = sentiment_df.merge(cleaned_df, on='review', how='left')
        
        # Remove duplicates by keeping first occurrence
        df = df.drop_duplicates(subset=['review_id'])
        
        print(f"✅ Merged: {len(df)} unique reviews")
        
        # Bank name to ID mapping
        bank_mapping = {
            'Commercial Bank of Ethiopia': 1,
            'Bank of Abyssinia': 2,
            'Dashen Bank': 3
        }
        
        df['bank_id'] = df['bank'].map(bank_mapping)
        df = df.dropna(subset=['bank_id'])
        
        print(f"✅ Final rows to insert: {len(df)}")
        
        # Clear existing data first
        clear_existing_data()
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        inserted_count = 0
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO reviews (bank_id, review_text, rating, review_date, 
                                    sentiment_label, sentiment_score, identified_theme, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(row['bank_id']),
                str(row['review'])[:2000],
                int(row['rating']),
                str(row['review_date']),
                str(row['sentiment_label']),
                float(row['sentiment_score']),
                str(row['identified_theme']),
                'Google Play'
            ))
            inserted_count += 1
            
            if inserted_count % 200 == 0:
                print(f"   Inserted {inserted_count} reviews...")
        
        conn.commit()
        print(f"✅ Inserted {inserted_count} reviews into database")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def run_verification():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n" + "="*60)
        print("VERIFICATION RESULTS")
        print("="*60)
        
        cursor.execute("""
            SELECT b.bank_name, COUNT(r.review_id) AS total_reviews
            FROM banks b
            LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY total_reviews DESC
        """)
        print("\n📊 Reviews per bank:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} reviews")
        
        cursor.execute("""
            SELECT b.bank_name, ROUND(AVG(r.rating)::numeric, 2) AS avg_rating
            FROM banks b
            LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY avg_rating DESC
        """)
        print("\n⭐ Average rating per bank:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} stars")
        
        # Total count check
        cursor.execute("SELECT COUNT(*) FROM reviews")
        total = cursor.fetchone()[0]
        print(f"\n📊 Total reviews in database: {total}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Verification error: {e}")

def main():
    print("="*60)
    print("🚀 TASK 3: POSTGRESQL DATA INSERTION (FIXED)")
    print("="*60)
    
    if not test_connection():
        return
    
    insert_data()
    run_verification()
    
    print("\n" + "="*60)
    print("✅ TASK 3 COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()