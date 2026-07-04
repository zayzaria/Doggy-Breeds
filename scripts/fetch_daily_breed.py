import requests
import random
import json
import os
from datetime import datetime

def get_breeds_list():
    """Get all main breeds from Dog CEO API"""
    url = "https://dog.ceo/api/breeds/list/all"
    response = requests.get(url, timeout=15)
    
    print(f"Breeds list status code: {response.status_code}")
    
    if response.status_code != 200:
        print("ERROR: Failed to get breeds list")
        print("Response text:", response.text[:500])  # Print first 500 chars for debugging
        raise Exception("Failed to fetch breeds from Dog CEO API")
    
    data = response.json()
    breeds = list(data["message"].keys())
    return breeds

def get_random_image(breed):
    """Get a random image for a specific breed"""
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    response = requests.get(url, timeout=15)
    
    if response.status_code != 200:
        print(f"ERROR getting image for {breed}")
        print("Response:", response.text[:300])
        raise Exception("Failed to get image")
    
    return response.json()["message"]

def get_breed_details(breed_name, api_key):
    """Get detailed info from The Dog API"""
    if not api_key:
        print("No THEDOGAPI_KEY found - skipping detailed stats")
        return None
    
    headers = {"x-api-key": api_key}
    search_name = breed_name.replace("_", " ")
    url = f"https://api.thedogapi.com/v1/breeds/search?q={search_name}"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200 and response.json():
            breed = response.json()[0]
            return {
                "name": breed.get("name"),
                "temperament": breed.get("temperament", "N/A"),
                "life_span": breed.get("life_span", "N/A"),
                "weight": breed.get("weight", {}),
                "height": breed.get("height", {}),
                "bred_for": breed.get("bred_for", "N/A"),
                "origin": breed.get("origin", "N/A"),
            }
    except Exception as e:
        print(f"Error fetching details: {e}")
    return None

if __name__ == "__main__":
    api_key = os.getenv("THEDOGAPI_KEY")
    
    print("Fetching daily dog breed...")
    
    breeds = get_breeds_list()
    random_breed = random.choice(breeds)
    
    image_url = get_random_image(random_breed)
    breed_display = random_breed.replace("_", " ").title()
    
    details = get_breed_details(random_breed, api_key)
    
    daily_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "breed": breed_display,
        "image_url": image_url,
        "synopsis": f"A beautiful {breed_display}! " + (details.get("temperament", "") if details else ""),
        "stats": details if details else {
            "note": "Basic info only (add TheDogAPI key for full stats)"
        }
    }
    
    with open("daily_breed.json", "w", encoding="utf-8") as f:
        json.dump(daily_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully updated daily breed to: {breed_display}")