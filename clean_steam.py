import pandas as pd

#Load raw data into DataFrame
steam_df = pd.read_csv('cyberpunk_players_count.csv')

# Convert 'Month' to proper dates; anything unparseable becomes NaT
steam_df['Month'] = pd.to_datetime(steam_df['Month'], errors='coerce')

# Fill the 'Last 30 days' row with today's date
today = pd.Timestamp.now().normalize()
steam_df['Month'] = steam_df['Month'].fillna(today)

# Added a Year-Month key to join steam and reddit data
steam_df['Year_Month'] = steam_df['Month'].dt.to_period('M')

# Remove the '%' symbol so it can be converted to a number
steam_df['% Gain'] = steam_df['% Gain'].str.replace('%', '', regex=False)

# Convert both gain columns to numeric; invalid values become NaN
steam_df["Gain"] = pd.to_numeric(steam_df["Gain"], errors="coerce")
steam_df["% Gain"] = pd.to_numeric(steam_df["% Gain"], errors="coerce")

# Fill missing gain values (e.g. the game's launch month) with 0
steam_df[['Gain', '% Gain']] = steam_df[['Gain', '% Gain']].fillna(0)

# Check for missing values
print(steam_df.isna().sum())

# Export clean data to csv
steam_df.to_csv('staging_steam_players.csv', index=False)
