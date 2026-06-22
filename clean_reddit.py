import pandas as pd

# Load raw Reddit data into DataFrame
reddit_df = pd.read_csv('cyberpunk_reddit_data.csv')

# Convert 'Date' to proper dates; anything unparseable becomes NaT
reddit_df['Post_Date'] = pd.to_datetime(reddit_df['Post_Date'], errors='coerce')

# Added a Year-Month key to join steam and reddit data
reddit_df['Year_Month'] = reddit_df['Post_Date'].dt.to_period('M')


def convert_upvotes(value):
  """Convert upvote text like '1.2k' or '3.4m' into a plain integer."""
  value = str(value).strip().lower()

  if 'k' in value:
    return int(float(value.replace('k', '')) * 1000)
  elif 'm' in value:
    return int(float(value.replace('m', '')) * 1000000)
  else:
    return int(float(value))

# Apply the conversion to every row in the Upvotes column
reddit_df['Upvotes'] = reddit_df['Upvotes'].apply(convert_upvotes)

# Remove accidental leading/trailing spaces from post titles
reddit_df["Title"] = reddit_df["Title"].str.strip()

# Check for missing values
print(reddit_df.isna().sum())

# Export the data to csv
reddit_df.to_csv('staging_reddit_community.csv', index=False)