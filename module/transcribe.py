import os
import subprocess
import assemblyai as aai


def download_youtube_audio(youtube_url, i=0):
    try:
        print(f"Downloading audio from: {youtube_url}")
        output_path=f"files/{i}audio.mp3"
        
        command = [
            "yt-dlp",
            "-f", "bestaudio/best",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", output_path,
            youtube_url
        ]
        subprocess.run(command, check=True)
        print(f"Audio downloaded and saved as {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None

def transcribe_audio(file_path):
    try:
        aai.settings.api_key = "3cedd0b89e7747bf84d8f9a18853f05d"  # Replace with your actual API key

        # Enable Automatic Language Detection
        config = aai.TranscriptionConfig(language_detection=True)
        transcriber = aai.Transcriber(config=config)

        print("Uploading audio to AssemblyAI for transcription...")
        transcript = transcriber.transcribe(file_path)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription error: {transcript.error}")
        else:
            print("Transcription completed successfully.")
            return transcript.text
    except Exception as e:
        print(f"Error in transcription: {e}")
        return 'None'

# Main Function

def transcript(url,i):
    youtube_url = url

    # Download YouTube audio
    audio_file = download_youtube_audio(youtube_url,i)
    print("downloaded file:",audio_file)
    if audio_file:
        transcript = transcribe_audio(audio_file)
        if transcript:
            tt=transcript
            if os.path.exists(audio_file):
                os.remove(audio_file)
            return tt

'''
if __name__ == "__main__":
    youtube_url = input("Enter the YouTube video URL: ")
    audio_path = "downloaded_audio.mp3"

    # Download YouTube audio
    audio_file = download_youtube_audio(youtube_url, audio_path)

    if audio_file:
        # Transcribe the downloaded audio
        transcript = transcribe_audio(audio_file)
        if transcript:
            print("Transcript:")
            print(transcript)
'''

# from youtube_transcript_api import YouTubeTranscriptApi
# from deep_translator import GoogleTranslator

# def transcript(url:str) -> str:
#     video_id = url.split('watch?v=')[-1]
#     print("Transcribing :"+video_id)
#     try:
#         # all_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
#         # # print(f"Available transcripts: {all_transcripts}")
#         # available_langs = [t.language_code for t in all_transcripts]
#         # transcript_obj = all_transcripts.find_transcript(available_langs)
#         # transcript = transcript_obj.fetch()

#         # # print(transcript)
#         # # for snippet in transcript:
#         # #     print(snippet.text)
#         fetched_transcript = YouTubeTranscriptApi().fetch(video_id)
#         print(fetched_transcript)
#         raw_text = " ".join(entry.text for entry in fetched_transcript)
#         return raw_text

#         # transcript_lang = transcript_obj.language_code

#         # if transcript_lang != 'en':
#         #     try:
#         #         translated_text = GoogleTranslator(source='auto', target='en').translate(raw_text)
#         #         return translated_text
#         #     except Exception as e:
#         #         return ""
#         # else:
#         #     return raw_text



#     except Exception as e:
#         return ""