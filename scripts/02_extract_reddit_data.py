import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# Reddit url to get the Top posts of all time from 'r/cyberpunkgame'
base_url = "https://old.reddit.com/r/cyberpunkgame/top/?t=all&limit=100"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

posts = []
after = None  # tracks pagination - tells reddit "give me posts after this one"

while len(posts) < 500:

    # Build the url - add 'after' param if we're past page 1
    url = base_url if after is None else f"{base_url}&after={after}"

    # Get request to the webpage
    response = requests.get(url, headers=headers)

    # Checks if request was successful
    if response.status_code == 200:
        # BeautifulSoup Object to parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all reddit posts on this page
        posts_on_page = soup.find_all("div", class_="thing")

        # Stop if reddit returns no more posts
        if not posts_on_page:
            print("No more posts found, stopping")
            break

        for post in posts_on_page:
            title = post.find("a", class_="title")
            score = post.find("div", class_="score unvoted")
            comments = post.find("a", class_="comments")
            time_tag = post.find("time")

            # Extract data and append it to posts list
            posts.append({
                "Post_Date": time_tag["datetime"][:10] if time_tag else "",
                "Title": title.text.strip() if title else "",
                "Upvotes": score.text.strip() if score else "0",
                "Total_Comments": comments.text.split()[0] if comments else "0"
            })

        print(f"Collected so far: {len(posts)} posts")

        # Get the 'after' token from the last post on this page, for the next loop
        after = posts_on_page[-1].get("data-fullname")

        if after is None:
            print("No 'after' token found, stopping")
            break

        time.sleep(2)  # pause between requests so reddit doesn't block us

    else:
        # Prints error code if request fails
        print(f"Failed: {response.status_code}")
        break

# Trim to exactly 500 in case the last page overshoots
posts = posts[:500]

# Convert list of dictionaries into pandas DataFrame
reddit_df = pd.DataFrame(posts)

# Save DataFrame as a CSV File
with open('cyberpunk_reddit_data_500.csv', mode='w', encoding='utf-8', newline="") as file:
    reddit_df.to_csv(file, index=False)

# Prints number of posts saved
print(f"Saved {len(reddit_df)} posts!")
  