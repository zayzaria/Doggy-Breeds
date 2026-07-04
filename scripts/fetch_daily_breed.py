import requests
import random
import json
import os
import time
from datetime import datetime

def get_breeds_list(max_retries=3):
    """Get all main breeds from Dog CEO API with retry"""
    url = "https://dog.ceo/api/breeds/list/all"
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=15)
            print(f"Attempt {attempt}: Breeds list status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                breeds = list(data["message"].keys())
                return breeds
            else:
                print(f"Got status {response.status_code}, retrying...")
                
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
        
        if attempt < max_retries:
            time.sleep(2)  # Wait 2 seconds before retrying
    
    raise Exception("Failed to fetch breeds from Dog CEO API after multiple attempts")

def get_random_image(breed, max_retries=3):
    """Get a random image for a specific breed with retry"""
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    
    for attempt in range(1, max_retries + 1):
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()["message"]
        time.sleep(1)
    
    raise Exception(f"Failed to get image for {breed}")

def get_breed_details(breed_name, api_key):
    if not api_key:
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
            }
    except:
        pass
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
        "stats": details if details else {"note": "Basic info only"}
    }
    
    with open("daily_breed.json", "w", encoding="utf-8") as f:
        json.dump(daily_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully updated to: {breed_display}")