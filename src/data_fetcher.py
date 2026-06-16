import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

def format_date(date_str):
    """
    Converts "2026-06-15" to "20260615" which the API needs
    """
    return date_str.replace("-", "")

def get_matches_by_date(date):
    """
    Fetches all finished football matches for a given date
    date format: "YYYY-MM-DD"
    """
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-matches-by-date-and-league"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }

    params = {
        "date": format_date(date)
    }

    print(f"🔄 Fetching matches for {date}...")

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        if data["status"] != "success":
            print("❌ API returned failure")
            return None

        all_matches = []

        # Loop through each league and collect all matches
        for league in data["response"]:
            league_name = league["name"]
            country = league["ccode"]
            for match in league["matches"]:
                # Only include finished matches
                if match["status"]["finished"]:
                    home_score = match["home"]["score"]
                    away_score = match["away"]["score"]
                    total_goals = home_score + away_score

                    all_matches.append({
                        "league": league_name,
                        "country": country,
                        "home_team": match["home"]["name"],
                        "away_team": match["away"]["name"],
                        "home_score": home_score,
                        "away_score": away_score,
                        "score_str": match["status"]["scoreStr"],
                        "total_goals": total_goals,
                        "match_id": match["id"]
                    })

        print(f"✅ Found {len(all_matches)} finished matches!")
        return all_matches

    else:
        print(f"❌ Error: {response.status_code}")
        return None

# Test it
if __name__ == "__main__":
    matches = get_matches_by_date("2026-06-15")

    if matches:
        print("\n📋 Top 5 highest scoring matches:")
        # Sort by total goals, highest first
        sorted_matches = sorted(matches, key=lambda x: x["total_goals"], reverse=True)
        for match in sorted_matches[:5]:
            print(f"  ⚽ {match['league']} ({match['country']}): {match['home_team']} {match['score_str']} {match['away_team']} — {match['total_goals']} goals")