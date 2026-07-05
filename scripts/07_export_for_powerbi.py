import sqlite3
import pandas as pd

conn = sqlite3.connect('cyberpunk_analysis.db')

# Export all three tables as CSVs for Power BI
pd.read_sql_query("SELECT * FROM monthly_summary", conn).to_csv('powerbi_monthly_summary.csv', index=False)
pd.read_sql_query("SELECT * FROM reddit_posts", conn).to_csv('powerbi_reddit_posts.csv', index=False)
pd.read_sql_query("SELECT * FROM steam_players", conn).to_csv('powerbi_steam_players.csv', index=False)

conn.close()
print("Done — 3 CSVs exported for Power BI")