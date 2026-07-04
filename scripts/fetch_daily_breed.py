import requests
import random
import json
import os
import time
from datetime import datetime 

def get_breeds_list(max_retries=3):
    """Get breed list from TheDogAPI (more reliable)"""
    if not os.getenv("THEDOGAPI_KEY"):
        raise Exception("THEDOGAPI_KEY is missing!")
    
    headers = {"x-api-key": os.getenv("THEDOGAPI_KEY")}
    url = "https://api.thedogapi.com/v1/breeds"
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            print(f"Attempt {attempt}: TheDogAPI status code: {response.status_code}")
            
            if response.status_code == 200:
                breeds_data = response.json()
                # Extract breed names
                breeds = [breed["name"].lower().replace(" ", "_") for breed in breeds_data]
                return breeds
            else:
                print(f"Status {response.status_code}")
        except Exception as e:
            print(f"Attempt {attempt} error: {e}")
        
        if attempt < max_retries:
            time.sleep(2)
    
    raise Exception("Failed to get breed list from TheDogAPI")

def get_random_image(breed):
    """Get random image from dog.ceo (with fallback)"""
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()["message"]
    except:
        pass
    # Fallback: use a generic dog image if dog.ceo fails
    return "https://images.dog.ceo/breeds/retriever-golden/n02099601_1234.jpg"

def get_breed_details(breed_name, api_key):
    headers = {"x-api-key": api_key}
    search_name = breed_name.replace("_", " ")
    url = f"https://api.thedogapi.com/v1/breeds/search?q={search_name}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
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
    print("Fetching daily dog breed using TheDogAPI...")
    
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