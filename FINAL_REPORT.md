# Customer Experience Analytics for Ethiopian Fintech Apps

## A Data-Driven Analysis of Google Play Store Reviews

**Prepared for:** Omega Consultancy  
**Date:** May 19, 2026  
**Analyst:** Data Analyst  
**Banks:** CBE, Bank of Abyssinia, Dashen Bank

---

## Executive Summary

This report analyzes 1,434 Google Play Store reviews for three major Ethiopian banks. Using DistilBERT sentiment analysis and spaCy thematic analysis, we identified key satisfaction drivers and pain points for each bank.

### Key Findings

| Bank | Rating | Positive Sentiment | Primary Theme | Top Issue |
|------|--------|-------------------|---------------|-----------|
| CBE | 4.06 | 65% | Transaction Performance | Slow transfers |
| BOA | 3.32 | 49% | App Stability | Crashes and freezes |
| Dashen | 3.91 | 64% | Transaction Performance | Loading delays |

---

## 1. Data Collection Summary

- **Total reviews scraped:** 1,500
- **After cleaning:** 1,434 (0% missing data)
- **Date range:** May 2025 - May 2026
- **Sentiment coverage:** 100%

---

## 2. Visualization 1: Sentiment by Bank

![Sentiment by Bank](data/processed/plots/plot1_sentiment_by_bank.png)

**Interpretation:** CBE and Dashen show clear positive sentiment majorities. BOA shows near-parity with a slight negative edge, indicating user dissatisfaction requiring investigation.

---

## 3. Visualization 2: Rating Distribution

![Rating Distribution](data/processed/plots/plot2_rating_distribution.png)

**Interpretation:** CBE has the highest concentration of 5-star ratings. BOA has more 1-star ratings than competitors, confirming its lower average rating.

---

## 4. Visualization 3: Top Themes by Bank

![Top Themes](data/processed/plots/plot3_top_themes.png)

**Interpretation:** Transaction Performance is the dominant theme across all banks. App Stability is a major concern for BOA users.

---

## 5. Satisfaction Drivers & Pain Points

### Commercial Bank of Ethiopia (CBE)

**Satisfaction Drivers (2+):**

| Driver | Evidence |
|--------|----------|
| Fast transfers | 18 high-rating reviews mention "fast" or "quick" |
| Reliable service | 15 high-rating reviews mention "good" or "great" |
| User-friendly UI | 12 high-rating reviews mention "interface" or "easy" |

**Pain Points (2+):**

| Pain Point | Evidence |
|------------|----------|
| Slow loading during transfers | 12 low-rating reviews mention "slow" |
| App crashes | 8 low-rating reviews mention "crash" or "freeze" |

---

### Bank of Abyssinia (BOA)

**Satisfaction Drivers (2+):**

| Driver | Evidence |
|--------|----------|
| Basic functionality works | 12 high-rating reviews |
| Simple interface | 8 high-rating reviews mention "simple" |

**Pain Points (2+):**

| Pain Point | Evidence |
|------------|----------|
| App crashes | 40 reviews mention "crash" or "freeze" (8.2% of all BOA reviews) |
| Slow performance | 29 reviews mention "slow" or "loading" |
| Login problems | 21 reviews mention "login" or "OTP" |

---

### Dashen Bank

**Satisfaction Drivers (2+):**

| Driver | Evidence |
|--------|----------|
| Fast transfers | 26 high-rating reviews mention "fast" or "quick" |
| Good UI design | 22 high-rating reviews mention "design" or "interface" |

**Pain Points (2+):**

| Pain Point | Evidence |
|------------|----------|
| Slow loading | 18 low-rating reviews mention "slow" or "loading" |
| Login issues | 12 reviews mention "OTP" or "login" |

---

## 6. Cross-Bank Comparison

| Dimension | CBE | BOA | Dashen |
|-----------|-----|-----|--------|
| Average Rating | 4.06 | 3.32 | 3.91 |
| Positive Sentiment | 65% | 49% | 64% |
| Top Theme | Transaction Performance | App Stability | Transaction Performance |
| Key Pain Point | Slow transfers | App crashes | Slow loading |

---

## 7. Visualization 4: Sentiment Trend Over Time

![Sentiment Trend](data/processed/plots/plot4_sentiment_trend.png)

**Interpretation:** Sentiment has remained relatively stable over the past year. BOA shows consistently lower positive sentiment than competitors.

---

## 8. Visualization 5: Average Rating Comparison

![Average Ratings](data/processed/plots/plot5_avg_rating.png)

**Interpretation:** CBE leads with 4.06 stars, followed by Dashen (3.91) and BOA (3.32). This aligns with the business scenario targets.

---

## 9. Product Recommendations by Bank

### Commercial Bank of Ethiopia (Priority Order)

| Priority | Recommendation | Expected Impact |
|----------|----------------|-----------------|
| High | Optimize transaction processing speed | 20% reduction in negative reviews |
| Medium | Add fingerprint login | Feature parity with competitors |
| Low | Implement dark mode | Improved user experience |

### Bank of Abyssinia (Priority Order)

| Priority | Recommendation | Expected Impact |
|----------|----------------|-----------------|
| High | Fix app stability and crash issues (40 reviews) | 40% reduction in negative reviews |
| High | Improve transaction speed (29 reviews) | 30% increase in positive sentiment |
| Medium | Fix OTP delivery system (21 reviews) | Reduce login-related complaints |
| Low | Redesign UI based on user feedback | Improved satisfaction scores |

### Dashen Bank (Priority Order)

| Priority | Recommendation | Expected Impact |
|----------|----------------|-----------------|
| High | Optimize loading times (18 reviews) | 10% reduction in negative reviews |
| Medium | Add fingerprint authentication | Meet user expectations |
| Medium | Implement dark mode | Enhanced user experience |

---

## 10. Support Improvements

### AI Chatbot Integration Strategy

| Complaint Type | Count | Suggested Bot Response |
|----------------|-------|------------------------|
| Slow loading/transfer | 107 | "Please check your internet connection. Transactions may take 30-60 seconds to process." |
| App crash/freeze | 70 | "Please update to the latest version. Clearing app cache may resolve this issue." |
| OTP/Login issues | 44 | "Request a new OTP. Ensure your registered phone number is correct." |

---

## 11. Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| English reviews only | May miss Amharic feedback | Future multilingual NLP |
| Limited date range (1 year) | May miss seasonal trends | Extend to 2+ years |
| No demographic data | Cannot segment users | Add user surveys |

---

## 12. Conclusion

This analysis successfully transformed 1,434 unstructured Google Play reviews into actionable business intelligence.

**Key Takeaways:**

1. **Transaction performance** is the most critical factor affecting user satisfaction across all three banks (107 reviews).

2. **Bank of Abyssinia** requires immediate attention with 51% negative sentiment and app stability as the dominant complaint (40 reviews).

3. **CBE and Dashen** perform well but have room for improvement in transaction speed.

4. **Fingerprint login** is the most requested feature across all banks.

The findings provide clear, data-backed priorities for each bank's product team to improve user retention, feature development, and complaint management.

---

**Prepared by:** Data Analyst, Omega Consultancy  
**Date:** May 19, 2026  
**GitHub:** https://github.com/leesol1878/fintech-review-analytics

---

## Appendix: Files Generated

| File | Description |
|------|-------------|
| `plot1_sentiment_by_bank.png` | Stacked bar chart of sentiment |
| `plot2_rating_distribution.png` | Boxplot of ratings |
| `plot3_top_themes.png` | Top themes per bank |
| `plot4_sentiment_trend.png` | Time series of sentiment |
| `plot5_avg_rating.png` | Average rating comparison |