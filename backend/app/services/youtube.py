from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re

class YouTubeService:
    def extract_video_id(self, url: str) -> str:
        """Extracts the video ID from a YouTube URL."""
        # Handles various YouTube URL formats
        patterns = [
            r"(?:v=|youtu\.be/|youtube\.com/embed/)([\w-]{11})",
            r"youtube\.com/watch\?v=([\w-]{11})"
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def fetch_transcript(self, url: str) -> str:
        """Fetches the transcript for a YouTube video."""
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError("Invalid YouTube video URL.")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join([entry['text'] for entry in transcript])
            return text
        except (TranscriptsDisabled, NoTranscriptFound):
            raise ValueError("Transcript not available for this video.")
        except Exception as e:
            raise ValueError(f"Error fetching transcript: {str(e)}")

    def validate_url(self, url: str) -> bool:
        """Validates if the URL is a YouTube video URL."""
        return 'youtube.com/watch?v=' in url or 'youtu.be/' in url 