import requests
import pandas as pd
from bs4 import BeautifulSoup

#Reddit url to get the Top 100 posts of all time from 'r/cyberpunkgame'
url = "https://old.reddit.com/r/cyberpunkgame/top/?t=all&limit=100"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

#Get request to the webpage
response = requests.get(url, headers=headers)

#Checks if request was successful
if response.status_code == 200:
    #BeautifulSoup Object to parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    
    posts = []

    #Find all reddit posts
    for post in soup.find_all("div", class_="thing"):

        title = post.find("a", class_="title")
        score = post.find("div", class_="score unvoted")
        comments = post.find("a", class_="comments")
        time = post.find("time")

        #Extract data and append it to posts list
        posts.append({
            "Post_Date": time["datetime"][:10] if time else "",
            "Title": title.text.strip() if title else "",
            "Upvotes": score.text.strip() if score else "0",
            "Total_Comments": comments.text.split()[0] if comments else "0"
        })
    
    #Convert list of dictionaries into pandas DataFrame
    reddit_df = pd.DataFrame(posts)

    #Save DataFrame as a CSV File
    with open('cyberpunk_reddit_data.csv', mode='w', encoding='utf-8', newline="") as file:
        reddit_df.to_csv(file,index=False)

    #Prints number of posts saved
    print(f"Saved {len(reddit_df)} posts!") 

else:
    #Prints error code if request fails
    print(f"Failed: {response.status_code}")
  