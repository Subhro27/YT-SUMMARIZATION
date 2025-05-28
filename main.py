from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from pydantic import BaseModel
import google.generativeai as genai
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Initialize FastAPI app
app = FastAPI(title="YouTube Video Summarization API")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize YouTube Data API client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Define request model
class VideoRequest(BaseModel):
    url: str  # Expect a YouTube URL

# Serve the frontend
@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Function to extract video ID from YouTube URL
def get_video_id(url: str) -> str:
    try:
        if "youtube.com/watch?v=" in url:
            return url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        else:
            raise ValueError("Invalid YouTube URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid YouTube URL: {str(e)}")

# Function to get transcript
def get_transcript(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except (TranscriptsDisabled, NoTranscriptFound):
        return None  # Return None if transcript is unavailable
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transcript: {str(e)}")

# Function to get video metadata (title and description) using YouTube Data API
def get_video_metadata(video_id: str) -> str:
    try:
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        if not response["items"]:
            raise HTTPException(status_code=404, detail="Video not found")
        snippet = response["items"][0]["snippet"]
        title = snippet.get("title", "")
        description = snippet.get("description", "")
        return f"Title: {title}\nDescription: {description}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video metadata: {str(e)}")

# Function to summarize text using Gemini 2.0 Flash
def summarize_text(text: str, is_metadata: bool = False) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        if is_metadata:
            prompt = f"Summarize the following YouTube video title and description in 2-3 sentences, capturing the main points concisely:\n\n{text}"
        else:
            prompt = f"Summarize the following video transcript in 3-5 sentences, capturing the main points concisely:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing text: {str(e)}")

# API endpoint to summarize YouTube video
@app.post("/summarize")
async def summarize_video(request: VideoRequest):
    video_id = get_video_id(request.url)
    # Try to get transcript first
    transcript = get_transcript(video_id)
    if transcript:
        summary = summarize_text(transcript, is_metadata=False)
        source = "transcript"
    else:
        # Fall back to metadata if no transcript
        metadata = get_video_metadata(video_id)
        summary = summarize_text(metadata, is_metadata=True)
        source = "metadata"
    return {"video_id": video_id, "summary": summary, "source": source}