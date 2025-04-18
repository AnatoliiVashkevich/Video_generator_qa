import os
import subprocess
import moviepy.config as mpconf
mpconf.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
from gtts import gTTS
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, AudioFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.fx.all import resize
from moviepy.audio.AudioClip import concatenate_audioclips

# Create necessary folders
os.makedirs("temp_audio", exist_ok=True)
os.makedirs("temp_video", exist_ok=True)
os.makedirs("output_video", exist_ok=True)

# Questions and answers
qa_questions = [
    "What is your experience with test automation?",
    "How do you handle unexpected bugs during testing?",
    "Can you explain what test cases are?",
    "How do you prioritize your tests?",
    "What is your experience with performance testing?",
    "Have you ever worked with continuous integration?",
    "What tools have you used for automated testing?",
    "Can you describe your experience with bug reporting?",
    "How do you handle testing in agile environments?",
    "What is regression testing and why is it important?",
    "How do you handle cross-browser testing?",
    "What is your approach to test data management?",
    "Can you explain the importance of boundary value analysis?",
    "How do you ensure tests are repeatable and reliable?",
    "What is the difference between functional and non-functional testing?",
    "Can you explain the difference between verification and validation?",
    "What are the key principles of a successful test plan?",
    "What is the role of exploratory testing in your process?",
    "How do you ensure security is tested in your applications?",
    "What is your experience with load testing tools?",
    "How do you deal with flaky tests?",
    "What is your approach to API testing?",
    "Can you describe your experience with test automation frameworks?",
    "How do you handle test environment setup?",
    "What do you understand by test coverage?",
    "What is the importance of logging in testing?",
    "How do you handle tests that fail intermittently?",
    "What is your approach to user acceptance testing?",
    "Can you explain the concept of boundary testing?",
    "What tools do you use for bug tracking?",
    "What challenges do you face when working with large datasets in testing?",
    "Can you explain your experience with testing in the cloud?",
    "What is your process for continuous feedback in testing?",
    "Can you explain the difference between smoke testing and sanity testing?",
    "How do you handle integration testing in complex systems?",
    "How do you perform database testing?",
    "How do you ensure quality in CI/CD pipelines?",
    "Can you explain your experience with stress testing?",
    "What is your experience with test case maintenance?",
    "How do you handle automation script maintenance?"
    # (Add all 40 questions here...)
]
qa_answers = [
    "I have worked with Selenium and Playwright for automating web applications. I also have experience with Jenkins for continuous integration.",
    "I use a debugging approach, looking at logs and trying to reproduce the issue. I also collaborate with developers to identify the root cause.",
    "Test cases are detailed specifications that outline a set of conditions to verify if an application works as expected.",
    "I prioritize tests based on the criticality of the functionality, the risk of failure, and the frequency of usage.",
    "I have used tools like JMeter and LoadRunner for performance testing, focusing on response times and system scalability.",
    "Yes, I’ve integrated automated tests into Jenkins pipelines to ensure consistent test execution during development.",
    "I have worked with Selenium WebDriver, Cypress, and Playwright to automate functional and regression tests.",
    "I use bug tracking tools like Jira and Bugzilla to document, track, and prioritize defects efficiently.",
    "In agile environments, I collaborate with developers, ensuring test cases align with the user stories and continuously test features as they evolve.",
    "Regression testing ensures that new code changes don’t break existing functionality. It is important to maintain software stability.",
    "I use tools like BrowserStack for cross-browser testing to ensure our web application works across all supported browsers.",
    "I create realistic test data that mimics real-world scenarios to test edge cases and optimize test coverage.",
    "Boundary value analysis helps identify edge cases by testing inputs at the boundaries of valid and invalid data ranges.",
    "I write automated tests and keep track of the results to ensure tests are repeatable and can be run in different environments.",
    "Functional testing ensures that software behaves as expected, while non-functional testing focuses on other aspects like performance and security.",
    "Verification ensures the product meets specifications, while validation confirms the product fulfills user requirements.",
    "A test plan outlines the strategy, scope, resources, and schedule for testing. It ensures that testing is systematic and efficient.",
    "Exploratory testing allows testers to creatively investigate the software. It’s important when no clear requirements are given.",
    "I work with the security team to ensure that applications are secure by conducting security tests like penetration testing.",
    "I’ve used JMeter to perform load testing to measure how well an application handles high traffic and large numbers of concurrent users.",
    "I implement retry logic and monitor test logs to identify patterns that help reduce flakiness in tests.",
    "I test the API endpoints to ensure they function correctly by verifying the responses and handling edge cases.",
    "I have used frameworks like TestNG and Pytest, which provide powerful features for organizing and managing test automation.",
    "I ensure that the test environment is similar to production, using containerization and configuration management tools.",
    "Test coverage refers to how much of the application’s code is tested by automated or manual tests. Higher coverage reduces risk.",
    "Logging in testing helps track the execution flow and capture error details to diagnose issues quickly.",
    "I use retries, prioritize root cause analysis, and collaborate with the team to fix failing tests as soon as possible.",
    "I use tools like Applitools to perform visual validation testing across devices and browsers to ensure consistency.",
    "I perform database testing by validating the integrity, accuracy, and performance of data queries and operations.",
    "CI/CD pipelines ensure tests are automatically executed on each commit, providing faster feedback on the code’s stability.",
    "I stress test the application by simulating extreme conditions like high traffic or data input to check its resilience.",
    "I maintain test cases by regularly reviewing and updating them to align with changes in the application functionality.",
    "I regularly update automation scripts to reflect changes in the application and ensure continued coverage of new features."
    # (Add all 40 answers here...)
]

final_video_clips = []

def generate_tts(text, filename):
    tts = gTTS(text)
    tts.save(filename)

def generate_silence(duration, filename):
    subprocess.run([
        "ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(duration), "-q:a", "9", "-acodec", "libmp3lame",
        filename, "-y"
    ])

def generate_text_clip(text, duration, size=(1280, 720), fontsize=48):
    return TextClip(
        text, fontsize=fontsize, color='black',
        size=size, bg_color='#95dfe3', method='caption'
    ).set_duration(duration)

for idx, (question, answer) in enumerate(zip(qa_questions, qa_answers), 1):
    print(f"Processing QA pair {idx}...")

    # Question
    q_audio_file = f"temp_audio/q_{idx}.mp3"
    generate_tts(question, q_audio_file)
    q_audio = AudioFileClip(q_audio_file)
    q_pause_duration = len(question.split()) * 0.3 * 2
    generate_silence(q_pause_duration, f"temp_audio/q_pause_{idx}.mp3")
    q_pause = AudioFileClip(f"temp_audio/q_pause_{idx}.mp3")

    q_combined_audio = concatenate_audioclips([q_audio, q_pause])
    q_clip = generate_text_clip(question, q_combined_audio.duration)
    q_clip = q_clip.set_audio(q_combined_audio)

    # Answer
    a_audio_file = f"temp_audio/a_{idx}.mp3"
    generate_tts(answer, a_audio_file)
    a_audio = AudioFileClip(a_audio_file)
    a_pause_duration = len(answer.split()) * 0.3 * 2
    generate_silence(a_pause_duration, f"temp_audio/a_pause_{idx}.mp3")
    a_pause = AudioFileClip(f"temp_audio/a_pause_{idx}.mp3")

    a_combined_audio = concatenate_audioclips([a_audio, a_pause])
    a_clip = generate_text_clip(answer, a_combined_audio.duration)
    a_clip = a_clip.set_audio(a_combined_audio)

    # Append both clips to final list
    final_video_clips.extend([q_clip, a_clip])

# Final video
final_video = concatenate_videoclips(final_video_clips, method="compose")
final_video.write_videofile("output_video/qa_final_video.mp4", fps=24)

# Optional: Clean up temp folders
# import shutil
# shutil.rmtree("temp_audio")
# shutil.rmtree("temp_video")

print("✅ Video created: output_video/qa_final_video.mp4")