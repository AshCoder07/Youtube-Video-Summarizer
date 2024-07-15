import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from google import generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, CouldNotRetrieveTranscript

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are tasked with summarizing YouTube videos based on their transcripts. 
Your goal is to distill the essential points and key insights from the entire video,
presenting them in a concise and coherent format. 
Your summary should capture the most significant information, organized into clear bullet points, 
and should not exceed 250 words. The Transcript text will be appended here:"""

def generate_content(transcript, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(transcript + prompt)
    return response.text

def extract_transcript_details(youtube_video_url, language_code):
    try:
        video_id = youtube_video_url.split("=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        transcript_text = ""
        for i in transcript:
            transcript_text += i['text'] + " "
        return transcript_text
    except NoTranscriptFound:
        return "No transcript found for the specified language."
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except CouldNotRetrieveTranscript:
        return "Could not retrieve the transcript. Please check the video URL or try a different language."
    except Exception as e:
        raise e

st.set_page_config(page_title="YouTube Video Summarizer")
st.header("YouTube Video Summarizer Application")

youtube_link = st.text_input("Enter your YouTube URL")
language_code = st.text_input("Enter the language code (e.g., 'en' for English, 'es' for Spanish)")

if youtube_link and language_code:
    video_id = youtube_link.split("=")[-1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    if st.button("Get summary"):
        with st.spinner("Please wait..."):
            transcript_text = extract_transcript_details(youtube_link, language_code)
            if "Error" not in transcript_text and "transcript" not in transcript_text:
                summary = generate_content(transcript_text, prompt)
                st.write(summary)
            else:
                st.error(transcript_text)
