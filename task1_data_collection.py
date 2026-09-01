import time
import json
import os
from datetime import datetime
import requests

def get_top_story_ids():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"

    try:
        response = requests.get(url, timeout=10) #Using the requests library to fetch the top story ID
        top_ids = response.json()[:500]  #only keep the first 500
        return top_ids
    except requests.exceptions.RequestException as e:
      # if the request fails , return empty list
        print(f"Failed to get top story IDs: {e}")
        return []
# Fetches the full details for each story ID
def get_story_details(story_id):
  headers = {"User-Agent": "TrendPulse/1.0"}
  url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
  try:
    response = requests.get(url, headers=headers, timeout=10)
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"{story_id} failed")
    return None

# Checks if a story title belongs to a category
# by checking any of that category's keywords inside the title
def title_matches_category(title, keywords):
    title_lower = title.lower()
    for keyword in keywords:
        if keyword.lower() in title_lower:
            return True
    return False

# Keyword list for each category
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}
def collect_category(category_name, keywords, story_ids, limit=25):
  collected = []
  for story_id in story_ids:
        if len(collected) >= limit:
            break  # # Stop when we hit 25 stories for this category

        details = get_story_details(story_id)

        if details is None or "title" not in details:
            continue  # If the request fails skip this id , move to next id

#If the keyword matches, with required fields make it a record
        if title_matches_category(details["title"], keywords):
            record = {
                "post_id": details["id"],
                "title": details["title"],
                "category": category_name,
                "score": details.get("score", 0),
                "num_comments":details.get("descendants", 0),   # Hackernews calls this "descendants"
                "author": details.get("by"),
                "collected_at": datetime.now().isoformat()
				}
            collected.append(record)

#Wait 2 seconds before moving to the next category
  time.sleep(2)
  return collected

all_stories = []
for category_name, keywords in CATEGORIES.items():
    stories = collect_category(category_name, keywords, ids, limit=25)
    all_stories.extend(stories)
    print(f"{category_name}: collected {len(stories)} stories")

print(f"Total collected: {len(all_stories)}")

os.makedirs("data", exist_ok=True)

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

#save lisrt to file
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_stories, f, indent=2)

print(f"Collected {len(all_stories)} stories. Saved to {filename}")

from google.colab import drive
drive.mount('/content/drive')

ids = get_top_story_ids()
print(len(ids))
print(ids[:5])
story = get_story_details(49520022)
print(story)
print(title_matches_category("New AI model beats humans at chess", CATEGORIES["technology"]))
print(title_matches_category("Local bakery wins award", CATEGORIES["technology"]))
tech_stories = collect_category("technology", CATEGORIES["technology"], ids, limit=25)
print(len(tech_stories))
print(tech_stories[0])
