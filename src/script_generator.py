import anthropic
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_highlight_script(match, description):
    """
    Uses Claude to generate a punchy TikTok narration script
    based on the match data and description
    """

    prompt = f"""You are an energetic sports commentator creating a short TikTok voiceover script.

Here is today's highlight match:
- Match: {match['home_team']} vs {match['away_team']}
- Score: {match['score_str']}
- League: {match['league']} ({match['country']})
- Why it's exciting: {description['reason']}

Write a TikTok voiceover script that is:
- Exactly 4-5 sentences long
- Energetic and hype — like you can't believe what just happened
- Starts with a shocking hook to grab attention
- Ends with a question or call to action to boost engagement
- Uses simple punchy language, no complex words
- Sounds natural when spoken out loud

Only return the script text, nothing else."""

    print("🤖 Asking Claude to write the script...")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    script = message.content[0].text
    print("✅ Script generated!")
    return script

# Test it
if __name__ == "__main__":
    # Simulate a match and description
    test_match = {
        "home_team": "Porto Velho EC",
        "away_team": "Humaita SC",
        "score_str": "13 - 0",
        "league": "Serie D",
        "country": "BRA",
        "home_score": 13,
        "away_score": 0,
        "total_goals": 13
    }

    test_description = {
        "headline": "Porto Velho EC destroy Humaita SC 13 - 0",
        "reason": "massive 13-goal thrashing + goal fest with 13 goals",
        "league": "Serie D",
        "country": "BRA",
        "excitement_score": 160
    }

    script = generate_highlight_script(test_match, test_description)

    print("\n🎙️ GENERATED SCRIPT:")
    print("-" * 40)
    print(script)
    print("-" * 40)