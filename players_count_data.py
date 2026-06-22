import pandas as pd
import requests
from io import StringIO

# SteamCharts page for Cyberpunk 2077 player statistics
url = "https://steamcharts.com/app/1091500"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

#Get request to the webpage
response = requests.get(url, headers=headers)

#Checks if request was successful
if response.status_code == 200:
  
  #Extract all HTML tables from the page into a list of DataFrames
  tables = pd.read_html(StringIO(response.text))
  player_history_df = tables[0]
  
  #Save DataFrame as a CSV File
  with open('cyberpunk_players_count.csv', mode='w', encoding='utf-8', newline="") as file:
    player_history_df.to_csv(file, index=False)

  print("Successfully created cyberpunk_players_count.csv")
else:
  #Prints error code if request fails
  print(f"Failed to reach website. Status code : {response.status_code} ")
