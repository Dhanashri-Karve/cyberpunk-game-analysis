import pandas as pd
import sqlite3
import re

conn = sqlite3.connect('cyberpunk_analysis.db')

# Load all reddit posts
reddit_df = pd.read_sql_query('SELECT * FROM reddit_posts',conn)

# Keyword lists built from actual posts title
negative_keywords = [
    'fix', 'bug', 'glitch', 'unplayable', 'broken', 'disaster',
    'unfinished', 'terrible', 'underdelivers', 'refund', 'removed',
    'misleading', 'tanks', 'crash', 'trailer vs reality',
    'marketing vs reality', 'another year of dev', 'backlash',
    'called out', 'missing features', 'not the game we were promised',
    'devs please', 'please fix', 'won 0 awards', 'below average'
]

positive_keywords = [
    'love', 'amazing', 'best', 'perfect', 'immersive', 'brilliant',
    'edgerunners', 'masterpiece', 'incredible', 'overwhelmingly positive',
    'worth it', 'redeemed', 'bar to top', 'infinite', 'they did it',
    'massive patch', 'runs great', 'cyberpunk 2', 'goosebumps',
    'appreciation', 'amazing work', 'most well written'
]

def tag_sentiment(title):
  """
  Checks title against keyword lists.
  Negative takes priority over positive when both match.
  Defaults to Neutral if no keywords match.
  """
  title_lower = title.lower()

  # Checks negative first, negative overrides positive on conflict
  for keyword in negative_keywords:
   if re.search(r'\b' + re.escape(keyword) + r'\b', title_lower):
      return "Negative"
    
  # Check positive
  for keyword in positive_keywords:
    if re.search(r'\b' + re.escape(keyword) + r'\b', title_lower):
      return "Positive"
    
  # Default - Cosplay, memes, fan arts, lore questions, etc
  return "Neutral"

# Applying function to every row in Title column
reddit_df['Sentiment'] = reddit_df['Title'].apply(tag_sentiment)

# Check how many post fell into each category
print("Sentiment distribution:")
print(reddit_df['Sentiment'].value_counts())
print(f"\nTotal posts tagged: {len(reddit_df)}")

# Preview sample
for sentiment in ['Negative', 'Positive', 'Neutral']:
    print(f"\n--- Sample {sentiment} posts ---")
    sample = reddit_df[reddit_df['Sentiment'] == sentiment][['Year_Month','Title']].head(5)
    print(sample.to_string())

# Save tagged data back to SQLite
reddit_df.to_sql('reddit_posts', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
print("Sentiment tags saved to database successfully")

# Also export to CSV for reference
reddit_df.to_csv('staging_reddit_with_sentiment.csv', index=False)
print("Exported: staging_reddit_with_sentiment.csv")