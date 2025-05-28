# 🎥 YouTube Summarization App

An intelligent YouTube video summarizer built using **FastAPI**, **Google Gemini API**, and **YouTube Data API**. This Python-based application extracts video transcripts and generates concise summaries to help users quickly grasp key content without watching the entire video.

## 🚀 Features

* 🔍 **Extracts Transcripts**: Fetches transcripts from YouTube videos using the YouTube Data API.
* 🧠 **AI-Powered Summaries**: Uses Google Gemini API to generate high-quality, human-like summaries.
* ⚡ **FastAPI Backend**: Lightweight and high-performance backend built with FastAPI.
* 📎 **Simple API Interface**: Clean and minimalistic endpoints for easy integration or testing.

## 🛠 Tech Stack

* **Backend Framework**: FastAPI
* **AI Model**: Google Gemini API
* **Video Content**: YouTube Data API v3
* **Language**: Python 3.10+

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/youtube-summarizer-app.git
   cd youtube-summarizer-app
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**

   Create a `.env` file and add the following:

   ```env
   YOUTUBE_API_KEY=your_youtube_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Run the app**

   ```bash
   uvicorn main:app --reload
   ```

## 🧪 API Usage

### `/summarize`

**Method**: POST
**Body**:

```json
{
  "video_url": "https://www.youtube.com/watch?v=your_video_id"
}
```

**Response**:

```json
{
  "summary": "Here is the summary of the video content..."
}
```

