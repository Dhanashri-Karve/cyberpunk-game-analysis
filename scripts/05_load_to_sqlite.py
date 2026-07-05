import pandas as pd
import sqlite3

# Load CSVs into DataFrame
steam_df = pd.read_csv('data/staging/staging_steam_players.csv')
reddit_df = pd.read_csv('data/staging/staging_reddit_with_sentiment.csv')

# Connect to SQLite
conn = sqlite3.connect('database/cyberpunk_analysis.db')

# Load steam data into table
steam_df.to_sql('steam_players', conn, if_exists='replace', index=False)
print(f"steam_players tables created: {len(steam_df)} rows")

# Load reddit data into table
reddit_df.to_sql('reddit_posts', conn, if_exists='replace', index=False)
print(f"reddit_posts tables created: {len(reddit_df)} rows")

# Joining two tables as monthly summary
monthly_summary_query = """
CREATE TABLE IF NOT EXISTS monthly_summary AS
SELECT
  s.Year_Month,
  s.Snapshot_Date,
  s."Avg. Players" AS avg_players,
  s."Peak Players" AS peak_players,
  s.Gain AS player_gain,
  s."% Gain" AS pct_gain,
  COUNT(r.Title) AS reddit_post_count,
  SUM(r.Upvotes) AS total_upvotes,
  ROUND(AVG(r.Upvotes), 0) AS avg_upvotes,
  SUM(r.Total_Comments) AS total_comments
FROM steam_players AS s
LEFT JOIN reddit_posts AS r 
ON s.Year_Month = r.Year_Month
GROUP BY s.Year_Month
ORDER BY s.Year_Month ASC;
"""

# Drop if exists and recreates
conn.execute("DROP TABLE IF EXISTS monthly_summary")
conn.execute(monthly_summary_query)
conn.commit()

# Verify 3 tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
tables = cursor.fetchall()
print(f"\nTables in Database: {[t[0] for t in tables]}")

# Row count check
for table in [t[0] for t in tables]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"  {table}: {cursor.fetchone()[0]} rows")

conn.close()
print("\nDatabase ready: cyberpunk_analysis.db")

import sqlite3

conn = sqlite3.connect('database/cyberpunk_analysis.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", [t[0] for t in tables])

# Check row counts and column names for each
for table in [t[0] for t in tables]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [c[1] for c in cursor.fetchall()]
    print(f"\n{table}: {count} rows")
    print(f"  Columns: {cols}")

conn.close()