"""
Google Play Store Scraper for Ethiopian Bank Reviews
CORRECTED with actual package names from search
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import time
from datetime import datetime


BANKS = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.apollo",
    "Dashen Bank": "com.dashen.dashensuperapp"
}
def scrape_bank_reviews(bank_name, package_name, count=500):
    """
    Scrape reviews for a single bank
    """
    print(f"\n{'='*50}")
    print(f"Scraping: {bank_name}")
    print(f"Package: {package_name}")
    print(f"Target: {count} reviews")
    print(f"{'='*50}")
    
    try:
        # Scrape reviews
        result, continuation_token = reviews(
            package_name,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count
        )
        
        print(f"✅ Found {len(result)} reviews")
        
        if len(result) == 0:
            print(f"⚠️ No reviews found for {bank_name}")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(result)
        
        # Print column names to debug
        print(f"📋 Columns found: {list(df.columns)}")
        
        # Map columns (using correct names from the library)
        # The library returns: 'content', 'score', 'at', 'reviewId', etc.
        df = df.rename(columns={
            'content': 'review_text',
            'score': 'rating',
            'at': 'review_date',
            'reviewId': 'review_id'
        })
        
        # Select only needed columns
        df = df[['review_text', 'rating', 'review_date', 'review_id']]
        
        # Clean the data
        df['review_text'] = df['review_text'].fillna('')
        df['rating'] = df['rating']
        df['review_date'] = pd.to_datetime(df['review_date']).dt.strftime('%Y-%m-%d')
        
        # Add bank name and source
        df['bank'] = bank_name
        df['source'] = 'Google Play'
        
        print(f"✅ Successfully processed {len(df)} reviews for {bank_name}")
        
        return df[['review_text', 'rating', 'review_date', 'bank', 'source']]
        
    except Exception as e:
        print(f"❌ Error scraping {bank_name}: {e}")
        return pd.DataFrame()

def main():
    """
    Main function to scrape all banks
    """
    print("🚀 Starting Google Play Store Scraper for Ethiopian Banks")
    print(f"Start time: {datetime.now()}")
    
    all_reviews = []
    
    # Scrape each bank
    for bank_name, package_name in BANKS.items():
        df = scrape_bank_reviews(bank_name, package_name, count=500)
        
        if not df.empty:
            all_reviews.append(df)
            print(f"📊 {bank_name}: {len(df)} reviews collected")
        else:
            print(f"⚠️ WARNING: Could not scrape {bank_name}")
        
        # Wait between banks to avoid rate limiting
        print("⏳ Waiting 3 seconds...")
        time.sleep(3)
    
    # Combine all reviews
    if all_reviews:
        final_df = pd.concat(all_reviews, ignore_index=True)
        
        print(f"\n{'='*50}")
        print(f"📊 SUMMARY")
        print(f"{'='*50}")
        print(f"Total reviews collected: {len(final_df)}")
        print(f"\nReviews per bank:")
        print(final_df['bank'].value_counts())
        print(f"\nAverage rating per bank:")
        print(final_df.groupby('bank')['rating'].mean().round(2))
        
        # Save to CSV
        output_file = 'data/raw/raw_reviews.csv'
        final_df.to_csv(output_file, index=False)
        print(f"\n✅ Raw data saved to: {output_file}")
        
        # Show sample
        print(f"\n📝 Sample reviews:")
        print(final_df[['bank', 'review_text', 'rating', 'review_date']].head(10))
        
    else:
        print("❌ No reviews were collected from any bank!")
    
    print(f"\nEnd time: {datetime.now()}")
    print("🎉 Scraping complete!")

if __name__ == "__main__":
    main()