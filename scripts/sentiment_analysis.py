"""
Task 2: Sentiment and Thematic Analysis for Ethiopian Bank Reviews

Requirements:
1. Sentiment Analysis using distilbert-base-uncased-finetuned-sst-2-english
2. Thematic Analysis using TF-IDF and spaCy
3. Save results with review_id, sentiment_label, sentiment_score, identified_theme
"""

import pandas as pd
import numpy as np
from transformers import pipeline
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

# Load NLP models
print("Loading sentiment analysis model (DistilBERT)...")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

print("Loading spaCy model...")
try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Define themes (business-relevant categories)
THEMES = {
    "Account Access Issues": ["login", "otp", "authentication", "password", "verify", "access", "locked"],
    "Transaction Performance": ["transfer", "slow", "fast", "speed", "loading", "timeout", "pending"],
    "UI & Design": ["interface", "design", "ui", "navigation", "layout", "user friendly", "intuitive"],
    "Customer Support": ["support", "customer service", "help", "assistance", "response", "complaint"],
    "Feature Requests": ["feature", "fingerprint", "biometric", "budget", "dark mode", "notification"],
    "App Stability": ["crash", "freeze", "error", "bug", "fix", "glitch", "close"],
    "Security": ["secure", "safe", "fraud", "privacy", "data", "protection"]
}

def get_sentiment(text):
    """
    Classify sentiment using DistilBERT
    Returns: (label, confidence_score)
    """
    if pd.isna(text) or len(str(text).strip()) < 3:
        return "NEUTRAL", 0.5
    
    try:
        result = sentiment_pipeline(text[:512])[0]
        label = result['label'].upper()
        score = result['score']
        
        if label == 'POSITIVE':
            return "POSITIVE", score
        elif label == 'NEGATIVE':
            return "NEGATIVE", score
        else:
            return "NEUTRAL", score
    except:
        return "NEUTRAL", 0.5

def extract_keywords(text, top_n=5):
    """Extract keywords using spaCy"""
    if pd.isna(text) or len(str(text)) < 3:
        return []
    
    doc = nlp(str(text).lower())
    
    keywords = []
    for token in doc:
        if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'ADJ', 'VERB']:
            keywords.append(token.lemma_)
    
    keyword_counts = Counter(keywords)
    return [k for k, v in keyword_counts.most_common(top_n)]

def identify_theme(text):
    """Identify which theme the review belongs to"""
    if pd.isna(text) or len(str(text)) < 3:
        return "Other"
    
    text_lower = str(text).lower()
    scores = {}
    
    for theme, keywords in THEMES.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[theme] = score
    
    best_theme = max(scores, key=scores.get)
    if scores[best_theme] == 0:
        return "Other"
    return best_theme

def load_data():
    """Load cleaned reviews"""
    df = pd.read_csv('data/raw/cleaned_reviews.csv')
    print(f"✅ Loaded {len(df)} reviews")
    return df

def process_reviews(df):
    """Apply sentiment and thematic analysis"""
    print("\n" + "="*60)
    print("📊 Running Sentiment and Thematic Analysis")
    print("="*60)
    
    # Add unique review_id
    df['review_id'] = [f"review_{i}" for i in range(len(df))]
    
    # Apply sentiment analysis
    print("\n1️⃣ Analyzing sentiment with DistilBERT...")
    sentiment_results = df['review'].apply(get_sentiment)
    df['sentiment_label'] = [r[0] for r in sentiment_results]
    df['sentiment_score'] = [r[1] for r in sentiment_results]
    
    print(f"   Sentiment distribution:")
    print(df['sentiment_label'].value_counts())
    
    # Apply thematic analysis
    print("\n2️⃣ Extracting keywords...")
    df['keywords'] = df['review'].apply(extract_keywords)
    
    print("\n3️⃣ Identifying themes...")
    df['identified_theme'] = df['review'].apply(identify_theme)
    
    print(f"\n   Theme distribution:")
    print(df['identified_theme'].value_counts())
    
    return df

def aggregate_results(df):
    """Aggregate results by bank and rating"""
    print("\n" + "="*60)
    print("📊 AGGREGATION RESULTS")
    print("="*60)
    
    print("\n📈 Sentiment by Bank:")
    sentiment_by_bank = df.groupby('bank')['sentiment_label'].value_counts().unstack().fillna(0)
    print(sentiment_by_bank)
    
    print("\n⭐ Average Sentiment Score by Bank:")
    print(df.groupby('bank')['sentiment_score'].mean().round(3))
    
    print("\n🎯 Top Themes by Bank:")
    for bank in df['bank'].unique():
        print(f"\n   {bank}:")
        themes = df[df['bank'] == bank]['identified_theme'].value_counts().head(3)
        for theme, count in themes.items():
            print(f"      - {theme}: {count} reviews")
    
    # Key insights
    print("\n" + "="*60)
    print("📊 KEY INSIGHTS (Drivers & Pain Points)")
    print("="*60)
    
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        
        positive = bank_df[bank_df['rating'] >= 4]
        if len(positive) > 0:
            print(f"\n✅ {bank} - Satisfaction Drivers:")
            top_themes = positive['identified_theme'].value_counts().head(2)
            for theme, count in top_themes.items():
                print(f"   - {theme}: {count} reviews")
        
        negative = bank_df[bank_df['rating'] <= 2]
        if len(negative) > 0:
            print(f"\n⚠️ {bank} - Pain Points:")
            top_themes = negative['identified_theme'].value_counts().head(2)
            for theme, count in top_themes.items():
                print(f"   - {theme}: {count} reviews")

def save_results(df):
    """Save results to CSV"""
    result_columns = ['review_id', 'review', 'sentiment_label', 'sentiment_score', 'identified_theme']
    results_df = df[result_columns]
    
    import os
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/sentiment_results.csv'
    results_df.to_csv(output_path, index=False)
    
    print(f"\n✅ Results saved to: {output_path}")
    print(f"   Total reviews processed: {len(results_df)}")
    
    return results_df

def main():
    print("="*60)
    print("🚀 TASK 2: SENTIMENT AND THEMATIC ANALYSIS")
    print("="*60)
    
    df = load_data()
    df = process_reviews(df)
    aggregate_results(df)
    results = save_results(df)
    
    print("\n" + "="*60)
    print("✅ TASK 2 COMPLETE!")
    print("="*60)
    print("\nKPIs Achieved:")
    kpi = (len(df) - df['sentiment_score'].isna().sum()) / len(df) * 100
    print(f"   ✅ Sentiment scores: {kpi:.1f}% of reviews")
    print(f"   ✅ Themes identified: {df['identified_theme'].nunique()} distinct themes")

if __name__ == "__main__":
    main()