"""
Task 4: Visualizations for Ethiopian Bank Reviews Analysis
Creates 5 plots for the final report
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# Create output directory for plots
import os
os.makedirs('data/processed/plots', exist_ok=True)

# Load data
print("Loading data...")
sentiment_df = pd.read_csv('data/processed/sentiment_results.csv')
cleaned_df = pd.read_csv('data/raw/cleaned_reviews.csv')

# Merge to get bank names
df = sentiment_df.merge(cleaned_df[['review', 'bank', 'rating', 'review_date']], on='review', how='left')
print(f"Loaded {len(df)} reviews")

# ============================================
# PLOT 1: Sentiment Distribution by Bank (Stacked Bar Chart)
# ============================================
print("\n1. Creating sentiment distribution by bank...")

sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'])

fig, ax = plt.subplots(figsize=(10, 6))
sentiment_by_bank.plot(kind='bar', stacked=True, ax=ax, color=['#e74c3c', '#2ecc71'])

ax.set_title('Sentiment Distribution by Bank', fontsize=16, fontweight='bold')
ax.set_xlabel('Bank', fontsize=12)
ax.set_ylabel('Number of Reviews', fontsize=12)
ax.legend(title='Sentiment', bbox_to_anchor=(1.05, 1))
ax.tick_params(axis='x', rotation=45)

for container in ax.containers:
    ax.bar_label(container, label_type='center')

plt.tight_layout()
plt.savefig('data/processed/plots/plot1_sentiment_by_bank.png', dpi=150, bbox_inches='tight')
plt.close()
print("   Saved: plot1_sentiment_by_bank.png")

# ============================================
# PLOT 2: Rating Distribution by Bank (Boxplot)
# ============================================
print("\n2. Creating rating distribution by bank...")

fig, ax = plt.subplots(figsize=(10, 6))
bp = df.boxplot(column='rating', by='bank', ax=ax, grid=True)

ax.set_title('Rating Distribution by Bank', fontsize=16, fontweight='bold')
ax.set_xlabel('Bank', fontsize=12)
ax.set_ylabel('Rating (Stars)', fontsize=12)
ax.set_ylim(0.5, 5.5)

# Add mean values as dots
means = df.groupby('bank')['rating'].mean()
for i, bank in enumerate(means.index):
    ax.scatter(i+1, means[bank], color='red', s=100, zorder=3, label='Mean' if i==0 else '')
    ax.annotate(f'{means[bank]:.2f}', (i+1, means[bank]), 
                xytext=(5, 5), textcoords='offset points', fontweight='bold')

plt.suptitle('')  # Remove default title
plt.tight_layout()
plt.savefig('data/processed/plots/plot2_rating_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("   Saved: plot2_rating_distribution.png")

# ============================================
# PLOT 3: Top Themes per Bank (Horizontal Bar Chart)
# ============================================
print("\n3. Creating top themes per bank...")

# Filter out 'Other' theme
themes_df = df[df['identified_theme'] != 'Other']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, bank in enumerate(df['bank'].unique()):
    bank_themes = themes_df[themes_df['bank'] == bank]['identified_theme'].value_counts().head(5)
    
    axes[idx].barh(bank_themes.index, bank_themes.values, color='skyblue')
    axes[idx].set_title(bank, fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Number of Reviews')
    axes[idx].invert_yaxis()
    
    for i, v in enumerate(bank_themes.values):
        axes[idx].text(v + 1, i, str(v), va='center')

plt.suptitle('Top 5 Themes by Bank (Excluding "Other")', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('data/processed/plots/plot3_top_themes.png', dpi=150, bbox_inches='tight')
plt.close()
print("   Saved: plot3_top_themes.png")

# ============================================
# PLOT 4: Sentiment Trend Over Time
# ============================================
print("\n4. Creating sentiment trend over time...")

# Convert date
df['review_date'] = pd.to_datetime(df['review_date'])

# Group by month and sentiment
df['month'] = df['review_date'].dt.to_period('M')
monthly_sentiment = df.groupby(['month', 'sentiment_label']).size().unstack(fill_value=0)
monthly_sentiment.index = monthly_sentiment.index.astype(str)

fig, ax = plt.subplots(figsize=(12, 6))
monthly_sentiment.plot(kind='line', marker='o', ax=ax, color=['#e74c3c', '#2ecc71'])

ax.set_title('Sentiment Trend Over Time', fontsize=16, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Reviews', fontsize=12)
ax.legend(title='Sentiment')
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('data/processed/plots/plot4_sentiment_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("   Saved: plot4_sentiment_trend.png")

# ============================================
# PLOT 5: Average Rating Comparison (Bar Chart)
# ============================================
print("\n5. Creating average rating comparison...")

avg_ratings = df.groupby('bank')['rating'].mean().sort_values(ascending=False)
colors = ['#2ecc71' if x >= 4 else '#f39c12' if x >= 3.5 else '#e74c3c' for x in avg_ratings.values]

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(avg_ratings.index, avg_ratings.values, color=colors)

ax.set_title('Average Rating by Bank', fontsize=16, fontweight='bold')
ax.set_xlabel('Bank', fontsize=12)
ax.set_ylabel('Average Rating (Stars)', fontsize=12)
ax.set_ylim(0, 5)

# Add value labels on bars
for bar, val in zip(bars, avg_ratings.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'{val:.2f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('data/processed/plots/plot5_avg_rating.png', dpi=150, bbox_inches='tight')
plt.close()
print("   Saved: plot5_avg_rating.png")

# ============================================
# Print Summary Statistics for Report
# ============================================
print("\n" + "="*60)
print("SUMMARY STATISTICS FOR REPORT")
print("="*60)

print("\n📊 Sentiment by Bank:")
sentiment_table = pd.crosstab(df['bank'], df['sentiment_label'])
print(sentiment_table)

print("\n⭐ Average Rating by Bank:")
print(df.groupby('bank')['rating'].mean().round(2))

print("\n🎯 Top 3 Themes by Bank:")
for bank in df['bank'].unique():
    bank_themes = df[(df['bank'] == bank) & (df['identified_theme'] != 'Other')]['identified_theme'].value_counts().head(3)
    print(f"\n   {bank}:")
    for theme, count in bank_themes.items():
        print(f"      - {theme}: {count} reviews")

print("\n✅ All 5 plots saved to: data/processed/plots/")
print("   - plot1_sentiment_by_bank.png")
print("   - plot2_rating_distribution.png")
print("   - plot3_top_themes.png")
print("   - plot4_sentiment_trend.png")
print("   - plot5_avg_rating.png")