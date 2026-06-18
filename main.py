import sys
import os
from datetime import datetime, timedelta

# Add src folder to path so we can import our modules
sys.path.append("src")

from data_fetcher import get_matches_by_date
from highlight_selector import pick_best_match, describe_match, run_highlight_selector
from script_generator import generate_highlight_script, run_script_generator
from voiceover_generator import generate_voiceover, run_voiceover_generator
from video_assembler import assemble_video, run_video_assembler
from card_generator import create_stat_card

def run_pipeline(date=None):
    """
    Runs the full soccer highlight generator pipeline:
    1. Fetch matches for given date
    2. Pick most exciting match
    3. Generate Claude script
    4. Generate voiceover
    5. Assemble final video
    """

    # Use yesterday's date by default (most matches are finished)
    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print("=" * 50)
    print("⚽ SOCCER HIGHLIGHT GENERATOR")
    print(f"📅 Date: {date}")
    print("=" * 50)

    # ── STEP 1: Fetch matches ──────────────────────
    print("\n📡 STEP 1: Fetching matches...")
    matches = get_matches_by_date(date)

    if not matches:
        print("❌ No matches found for this date. Try a different date.")
        return None

    # ── STEP 2: Pick best match ────────────────────
    print("\n🏆 STEP 2: Selecting best match...")
    best_match = pick_best_match(matches)
    description = describe_match(best_match)
    best_match["description"] = description

    # Save best match
    import json
    os.makedirs("data", exist_ok=True)
    with open("data/best_match.json", "w") as f:
        json.dump(best_match, f, indent=2)

    print(f"✅ Selected: {best_match['home_team']} {best_match['score_str']} {best_match['away_team']}")
    print(f"   Reason: {description['reason']}")

    # ── STEP 3: Generate Claude script ────────────
    print("\n🤖 STEP 3: Generating script with Claude...")
    script = generate_highlight_script(best_match, description)
    print(f"✅ Script ready!")

   # ── STEP 4: Generate stat card ─────────────────
    print("\n🎨 STEP 4: Generating stat card...")
    from card_generator import create_stat_card
    create_stat_card(best_match)
    print(f"✅ Stat card ready!")

    # ── STEP 5: Generate voiceover ─────────────────
    print("\n🎙️ STEP 5: Generating voiceover...")
    voiceover_path = generate_voiceover(script)
    print(f"✅ Voiceover ready!")

    # ── STEP 6: Assemble video ─────────────────────
    print("\n🎬 STEP 6: Assembling final video...")
    video_path = assemble_video()
    print(f"✅ Video ready!")

    # ── DONE ───────────────────────────────────────
    print("\n" + "=" * 50)
    print("🎉 PIPELINE COMPLETE!")
    print(f"📹 Your highlight video: {video_path}")
    print(f"🏆 Match: {best_match['home_team']} {best_match['score_str']} {best_match['away_team']}")
    print(f"📝 Script: data/script.txt")
    print(f"🎵 Voiceover: output/voiceover.mp3")
    print("=" * 50)

    return video_path

if __name__ == "__main__":
    # Allow passing a date as command line argument
    # Example: python main.py 2026-06-15
    # Or just: python main.py (uses yesterday's date)
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = None

    run_pipeline(date)