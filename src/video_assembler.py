import os
import json
from moviepy import ImageClip, AudioFileClip, CompositeAudioClip
from moviepy.audio.AudioClip import AudioClip
import numpy as np

def assemble_video(
    stat_card_path="output/stat_card.png",
    voiceover_path="output/voiceover.mp3",
    output_path="output/highlight.mp4"
):
    """
    Assembles the final highlight video by combining:
    - Stat card image (visual)
    - Voiceover audio (Claude script read aloud)
    """
    print("🎬 Assembling final video...")

    # Load voiceover to get its duration
    voiceover = AudioFileClip(voiceover_path)
    duration = voiceover.duration
    print(f"⏱️ Voiceover duration: {duration:.1f} seconds")

    # Load stat card image — display for the duration of the voiceover
    video = ImageClip(stat_card_path, duration=duration)

    # Attach voiceover audio to video
    final_video = video.with_audio(voiceover)

    # Export final video
    os.makedirs("output", exist_ok=True)
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    print(f"✅ Video saved to {output_path}")
    return output_path

def run_video_assembler():
    """
    Assembles the final highlight video
    """
    with open("data/best_match.json", "r") as f:
        best_match = json.load(f)

    print(f"📂 Assembling video for: {best_match['home_team']} vs {best_match['away_team']}")

    output_path = assemble_video()

    print(f"\n🎥 Final video ready: {output_path}")
    return output_path

if __name__ == "__main__":
    run_video_assembler()