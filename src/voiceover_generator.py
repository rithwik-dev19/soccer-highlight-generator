import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

# Load API key from .env file
load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def generate_voiceover(script, output_path="output/voiceover.mp3"):
    """
    Converts a text script into an audio voiceover file
    using ElevenLabs text-to-speech
    """

    print("🎙️ Generating voiceover...")

    # Generate audio using ElevenLabs
    audio = client.text_to_speech.convert(
        text=script,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # "George" - deep sports commentator voice
       model_id="eleven_turbo_v2_5",
        output_format="mp3_44100_128"
    )

    # Make sure output folder exists
    os.makedirs("output", exist_ok=True)

    # Save the audio file
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"✅ Voiceover saved to {output_path}")
    return output_path

def run_voiceover_generator():
    """
    Reads script from data/script.txt
    Generates voiceover and saves to output/voiceover.mp3
    """
    # Read script from saved file
    with open("data/script.txt", "r") as f:
        script = f.read()

    print(f"📂 Loaded script from data/script.txt")
    print(f"\n📝 Script content:")
    print("-" * 40)
    print(script)
    print("-" * 40)

    # Generate voiceover
    output_path = generate_voiceover(script)

    print(f"\n🎵 Audio file ready: {output_path}")
    return output_path

if __name__ == "__main__":
    run_voiceover_generator()