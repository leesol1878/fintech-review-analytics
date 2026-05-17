"""
Data Preprocessing for Google Play Store Reviews
Cleans the raw scraped data for analysis
"""

import pandas as pd
import numpy as np

def preprocess_reviews(input_path, output_path):
    """
    Clean and preprocess the raw reviews data
    
    Parameters:
    - input_path: Path to raw CSV file
    - output_path: Path to save cleaned CSV file
    """
    
    print("="*60)
    print("📊 DATA PREPROCESSING PIPELINE")
    print("="*60)
    
    # Step 1: Load data
    print("\n1️⃣ Loading raw data...")
    df = pd.read_csv(input_path)
    print(f"   ✅ Loaded {len(df)} reviews")
    
    # Step 2: Check for duplicates
    print("\n2️⃣ Checking for duplicates...")
    initial_count = len(df)
    
    # Check duplicates by review_id (if exists) or full text
    if 'review_id' in df.columns:
        df = df.drop_duplicates(subset=['review_id'])
        print(f"   ✅ Removed {initial_count - len(df)} duplicate reviews by ID")
    else:
        df = df.drop_duplicates(subset=['review_text', 'rating', 'bank', 'review_date'])
        print(f"   ✅ Removed {initial_count - len(df)} duplicate reviews by content")
    
    # Step 3: Handle missing values
    print("\n3️⃣ Handling missing values...")
    missing_before = df.isnull().sum().sum()
    
    # Drop rows missing review_text or rating
    df = df.dropna(subset=['review_text', 'rating'])
    
    # Fill other missing values with empty string or default
    df['review_text'] = df['review_text'].fillna('')
    df['review_date'] = df['review_date'].fillna('2026-01-01')
    
    missing_after = df.isnull().sum().sum()
    print(f"   ✅ Removed {missing_before - missing_after} missing values")
    
    # Step 4: Clean review text
    print("\n4️⃣ Cleaning review text...")
    # Remove extremely short reviews (less than 3 characters)
    df = df[df['review_text'].str.len() >= 3]
    print(f"   ✅ Removed {len(df[df['review_text'].str.len() < 3])} very short reviews")
    
    # Step 5: Ensure correct data types
    print("\n5️⃣ Validating data types...")
    df['rating'] = df['rating'].astype(int)
    df['review_date'] = pd.to_datetime(df['review_date']).dt.strftime('%Y-%m-%d')
    print(f"   ✅ Ratings: {df['rating'].min()} to {df['rating'].max()} stars")
    print(f"   ✅ Date range: {df['review_date'].min()} to {df['review_date'].max()}")
    
    # Step 6: Select required columns (matching task specification)
    print("\n6️⃣ Selecting required columns...")
    required_columns = ['review_text', 'rating', 'review_date', 'bank', 'source']
    df = df[required_columns]
    
    # Rename 'review_text' to 'review' as per task
    df = df.rename(columns={'review_text': 'review'})
    
    print(f"   ✅ Final columns: {list(df.columns)}")
    
    # Step 7: Save cleaned data
    print("\n7️⃣ Saving cleaned data...")
    df.to_csv(output_path, index=False)
    print(f"   ✅ Saved to: {output_path}")
    
    # Step 8: Summary statistics
    print("\n" + "="*60)
    print("📊 CLEANING SUMMARY")
    print("="*60)
    print(f"\nFinal review count: {len(df)}")
    print(f"\nReviews per bank:")
    print(df['bank'].value_counts())
    print(f"\nRating distribution per bank:")
    print(df.groupby('bank')['rating'].mean().round(2))
    print(f"\nMissing data percentage: {df.isnull().sum().sum() / len(df) * 100:.2f}%")
    
    return df

if __name__ == "__main__":
    # Run preprocessing
    cleaned_df = preprocess_reviews(
        input_path='data/raw/raw_reviews.csv',
        output_path='data/raw/cleaned_reviews.csv'
    )
    
    print("\n✅ Preprocessing complete! Ready for Task 2 (Sentiment Analysis)")