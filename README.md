\# Fintech Review Analytics



Analyzing Google Play Store reviews for Ethiopian banks: CBE, Bank of Abyssinia, and Dashen Bank.



\## Project Overview

This project scrapes, analyzes, and visualizes user reviews to provide actionable insights for bank product teams.



\## Project Structure
fintech-review-analytics/

├── .github/workflows/ # CI/CD automation

├── data/raw/ # Scraped review data (gitignored)

├── notebooks/ # Jupyter notebooks for exploration

├── src/ # Source code modules

├── tests/ # Unit tests

├── scripts/ # Execution scripts

├── .gitignore # Files ignored by git

├── requirements.txt # Python dependencies

└── README.md # This file





\## Setup Instructions



\### 1. Clone the repository

```bash

git clone https://github.com/your-username/fintech-review-analytics.git

cd fintech-review-analytics

## Data Collection Methodology

### Scraping Approach
- **Tool:** google-play-scraper (Python library)
- **Date range:** May 2025 - May 2026 (1 year of reviews)
- **Target:** 500 reviews per bank
- **Actual collected:** 1,500 total (500 each for CBE, BOA, Dashen)

### Package Names Used
| Bank | Package Name |
|------|-------------|
| CBE | com.combanketh.mobilebanking |
| BOA | com.boa.apollo |
| Dashen | com.dashen.dashensuperapp |

### Data Quality
- Total raw reviews: 1,500
- After cleaning: 1,434 (22 duplicates removed)
- Missing data: 0%
- Final columns: review, rating, date, bank, source

### Limitations
- CBE app required multiple attempts to find correct package name
- Reviews limited to English language only
- Date range limited by API availability

