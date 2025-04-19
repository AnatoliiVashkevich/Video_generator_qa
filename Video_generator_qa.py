import os
import subprocess
import azure.cognitiveservices.speech as speechsdk
import moviepy.config as mpconf
mpconf.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips

# Create necessary folders
os.makedirs("temp_audio", exist_ok=True)
os.makedirs("temp_video", exist_ok=True)
os.makedirs("output_video", exist_ok=True)

# Questions and answers
qa_questions = [
    "Can you explain the Agile Manifesto?",
]

qa_answers = [
    "The Agile Manifesto is a set of values and principles that guide software development.",
]

final_video_clips = []

# Function to generate TTS (Text-to-Speech) using Azure
def generate_tts(text, filename):
    speech_key = "F85shBkPdPLA2P26FY4UDdXa9F4F588cKkl29uEhqa0WqVnIZuh0JQQJ99BDACYeBjFXJ3w3AAAYACOGUsCd"  # Replace with your actual key
    service_region = "eastus"  # Replace with your actual region if different
    voice = "en-US-JacobNeural"  # You can change the voice here. Example: "en-US-JennyNeural" for female voice.

    # Set up Azure Speech Config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = voice
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    # Create the synthesizer and generate speech
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    # Handle response based on success or failure
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"✅ Azure TTS success: {filename}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("❌ Azure TTS canceled:", result.cancellation_details.reason)
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details:", result.cancellation_details.error_details)

        # Fallback to gTTS if Azure fails
        print("⚠️ Falling back to gTTS...")
        try:
            from gtts import gTTS
            tts = gTTS(text)
            tts.save(filename)
            print("✅ Fallback TTS success using gTTS.")
        except Exception as e:
            print("❌ gTTS fallback failed:", str(e))

# Function to generate silence (for pauses)
def generate_silence(duration, filename):
    subprocess.run([  # Use ffmpeg to generate a silence audio clip
        "ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(duration), "-q:a", "9", "-acodec", "libmp3lame",
        filename, "-y"
    ])

# Function to generate text clips (subtitles)
def generate_text_clip(text, duration, size=(1280, 720), fontsize=48):
    return TextClip(
        text, fontsize=fontsize, color='black',
        size=size, bg_color='#95dfe3', method='caption'
    ).set_duration(duration)

# Process the QA pairs
for idx, (question, answer) in enumerate(zip(qa_questions, qa_answers), 1):
    print(f"Processing QA pair {idx}...")

    # Question part
    q_audio_file = f"temp_audio/q_{idx}.mp3"
    generate_tts(question, q_audio_file)
    q_audio = AudioFileClip(q_audio_file)
    q_pause_duration = len(question.split()) * 0.3 * 2  # Calculate pause duration based on number of words
    generate_silence(q_pause_duration, f"temp_audio/q_pause_{idx}.mp3")
    q_pause = AudioFileClip(f"temp_audio/q_pause_{idx}.mp3")

    q_combined_audio = concatenate_audioclips([q_audio, q_pause])
    q_clip = generate_text_clip(question, q_combined_audio.duration)
    q_clip = q_clip.set_audio(q_combined_audio)

    # Answer part
    a_audio_file = f"temp_audio/a_{idx}.mp3"
    generate_tts(answer, a_audio_file)
    a_audio = AudioFileClip(a_audio_file)
    a_pause_duration = len(answer.split()) * 0.3 * 2  # Calculate pause duration based on number of words
    generate_silence(a_pause_duration, f"temp_audio/a_pause_{idx}.mp3")
    a_pause = AudioFileClip(f"temp_audio/a_pause_{idx}.mp3")

    a_combined_audio = concatenate_audioclips([a_audio, a_pause])
    a_clip = generate_text_clip(answer, a_combined_audio.duration)
    a_clip = a_clip.set_audio(a_combined_audio)

    # Append both clips to final list
    final_video_clips.extend([q_clip, a_clip])

# Final video creation
final_video = concatenate_videoclips(final_video_clips, method="compose")
final_video.write_videofile("output_video/qa_final_video.mp4", fps=24)

# Clean up temp folders (optional)
# import shutil
# shutil.rmtree("temp_audio")
# shutil.rmtree("temp_video")

print("✅ Video created: output_video/qa_final_video.mp4")
