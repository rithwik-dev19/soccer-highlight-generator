from PIL import Image, ImageDraw, ImageFont
import os
import json

def create_stat_card(match, output_path="output/stat_card.png"):
    """
    Creates a clean visual stat card for the highlight match
    """
    print("🎨 Creating stat card...")

    # Canvas size — vertical TikTok format (1080x1920)
    width = 1080
    height = 1920

    # Colors
    BG_COLOR = (15, 15, 25)          # Dark navy background
    ACCENT_COLOR = (0, 200, 100)      # Green accent
    WHITE = (255, 255, 255)
    GRAY = (150, 150, 150)
    YELLOW = (255, 200, 0)

    # Create blank canvas
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw top accent bar
    draw.rectangle([0, 0, width, 12], fill=ACCENT_COLOR)
    draw.rectangle([0, height-12, width, height], fill=ACCENT_COLOR)

    # Draw center card background
    card_margin = 60
    card_top = 600
    card_bottom = 1300
    draw.rounded_rectangle(
        [card_margin, card_top, width-card_margin, card_bottom],
        radius=40,
        fill=(25, 25, 40)
    )

    # --- TEXT SECTION ---
    # We use default font since custom fonts need installation
    # Title: HIGHLIGHTS
    draw.text((width//2, 480),
              "HIGHLIGHTS",
              fill=ACCENT_COLOR,
              anchor="mm",
              font=ImageFont.load_default(size=60))

    # League name
    draw.text((width//2, 660),
              f"{match['league']} • {match['country']}",
              fill=GRAY,
              anchor="mm",
              font=ImageFont.load_default(size=35))

    # Home team name
    draw.text((width//2, 820),
              match['home_team'],
              fill=WHITE,
              anchor="mm",
              font=ImageFont.load_default(size=55))

    # Score
    draw.text((width//2, 980),
              match['score_str'],
              fill=YELLOW,
              anchor="mm",
              font=ImageFont.load_default(size=130))

    # Away team name
    draw.text((width//2, 1140),
              match['away_team'],
              fill=WHITE,
              anchor="mm",
              font=ImageFont.load_default(size=55))

    # Total goals line
    draw.text((width//2, 1250),
              f"{match['total_goals']} GOALS SCORED",
              fill=ACCENT_COLOR,
              anchor="mm",
              font=ImageFont.load_default(size=40))

    # Bottom watermark
    draw.text((width//2, 1700),
              "github.com/rithwik-dev19",
              fill=GRAY,
              anchor="mm",
              font=ImageFont.load_default(size=30))

    # Save the image
    os.makedirs("output", exist_ok=True)
    img.save(output_path)
    print(f"✅ Stat card saved to {output_path}")
    return output_path

def run_card_generator():
    """
    Reads best match from data/best_match.json
    Creates stat card and saves to output/stat_card.png
    """
    with open("data/best_match.json", "r") as f:
        best_match = json.load(f)

    print(f"📂 Loaded match: {best_match['home_team']} vs {best_match['away_team']}")

    output_path = create_stat_card(best_match)

    print(f"\n🖼️ Stat card ready: {output_path}")
    return output_path

if __name__ == "__main__":
    run_card_generator()