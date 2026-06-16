import anthropic
import os
import json
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

    # ✅ Save script to data folder
    os.makedirs("data", exist_ok=True)
    with open("data/script.txt", "w") as f:
        f.write(script)

    print("✅ Script generated and saved to data/script.txt!")
    return script

def run_script_generator():
    """
    Reads best match from data/best_match.json
    Generates script and saves to data/script.txt
    """
    # Read best match from saved file
    with open("data/best_match.json", "r") as f:
        best_match = json.load(f)

    print(f"📂 Loaded best match: {best_match['home_team']} vs {best_match['away_team']}")

    description = best_match["description"]

    # Generate script
    script = generate_highlight_script(best_match, description)

    print(f"\n🎙️ GENERATED SCRIPT:")
    print("-" * 40)
    print(script)
    print("-" * 40)

    return script

if __name__ == "__main__":
    run_script_generator()