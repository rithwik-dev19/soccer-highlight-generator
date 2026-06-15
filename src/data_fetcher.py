import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

def get_popular_leagues():
    """
    Fetches popular football leagues
    """
    url = "https://free-api-live-football-data.p.rapidapi.com/football-popular-leagues"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }

    print("🔄 Fetching popular leagues...")

    response = requests.get(url, headers=headers)

    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        leagues = data["response"]["popular"]
        print("✅ Success! Here are the leagues:")
        for league in leagues:
            print(f"  - {league['name']} (ID: {league['id']}, Country: {league['ccode']})")
        return leagues
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

# Test it
if __name__ == "__main__":
    get_popular_leagues()