-- =====================================================
-- Database: bank_reviews
-- Schema for Ethiopian Bank Reviews Analysis
-- Task 3: PostgreSQL Database Setup
-- =====================================================

-- Create banks table
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(10) NOT NULL CHECK (sentiment_label IN ('POSITIVE', 'NEGATIVE', 'NEUTRAL')),
    sentiment_score DECIMAL(5,4) NOT NULL CHECK (sentiment_score >= 0 AND sentiment_score <= 1),
    identified_theme VARCHAR(50),
    source VARCHAR(50) DEFAULT 'Google Play',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label);

-- Insert bank data
INSERT INTO banks (bank_name, app_name) VALUES
    ('Commercial Bank of Ethiopia', 'CBE Mobile Banking'),
    ('Bank of Abyssinia', 'BOA Apollo'),
    ('Dashen Bank', 'Dashen Super App')
ON CONFLICT (bank_name) DO NOTHING;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Query 1: Count reviews per bank
SELECT 
    b.bank_name,
    COUNT(r.review_id) AS total_reviews
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY total_reviews DESC;

-- Query 2: Average rating per bank
SELECT 
    b.bank_name,
    ROUND(AVG(r.rating)::numeric, 2) AS avg_rating
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY avg_rating DESC;

-- Query 3: Sentiment distribution by bank
SELECT 
    b.bank_name,
    r.sentiment_label,
    COUNT(*) AS count
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name, r.sentiment_label
ORDER BY b.bank_name, r.sentiment_label;

-- Query 4: Theme distribution by bank
SELECT 
    b.bank_name,
    r.identified_theme,
    COUNT(*) AS count
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
WHERE r.identified_theme != 'Other'
GROUP BY b.bank_name, r.identified_theme
ORDER BY b.bank_name, count DESC;