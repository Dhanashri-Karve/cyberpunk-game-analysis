-- ----------------------------------------------------------
-- Cyberpunk 2077 Analytics - Analysis Queries
-- ----------------------------------------------------------

-- Q1: Launch Impact
-- Steepest player drops in history
SELECT Year_Month, avg_players, peak_players, pct_gain
FROM monthly_summary
ORDER BY pct_gain ASC
LIMIT 10;

-- Launch era Reddit sentiment (Dec 2020 - Jan 2021)
SELECT Post_Date, Title, Upvotes, Total_Comments, Sentiment
FROM reddit_posts
WHERE Year_Month IN ('2020-12', '2021-01')
ORDER BY Upvotes DESC
LIMIT 15;

-- Q2: Turning Point
-- Player count around Edgerunners + Patch 2.0
SELECT Year_Month, avg_players, pct_gain,
       reddit_post_count, total_upvotes
FROM monthly_summary
WHERE Year_Month IN (
    '2022-08','2022-09','2022-10',
    '2023-08','2023-09','2023-10','2023-11'
)
ORDER BY Year_Month;

-- Q2: Reddit posts from turning point windows
SELECT Year_Month, Post_Date, Title, Upvotes, Sentiment
FROM reddit_posts
WHERE Year_Month IN ('2022-09','2022-10','2023-09','2023-10')
ORDER BY Year_Month, Upvotes DESC;

-- Q3: Modern Status
-- Launch era vs today comparison
SELECT Year_Month, avg_players, peak_players, pct_gain,
       reddit_post_count, total_upvotes
FROM monthly_summary
WHERE Year_Month IN ('2020-12','2021-01','2026-05','2026-06')
ORDER BY Year_Month;

-- SENTIMENT DISTRIBUTION by month
-- Used for Power BI stacked bar chart
SELECT Year_Month, Sentiment, COUNT(*) AS post_count
FROM reddit_posts
GROUP BY Year_Month, Sentiment
ORDER BY Year_Month, Sentiment;