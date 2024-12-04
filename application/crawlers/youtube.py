import re
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

from loguru import logger

from domain.documents import VideoDocument
from .base import BaseSeleniumCrawler


class YouTubeCrawler(BaseSeleniumCrawler):
    model = VideoDocument

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Video already exists in the database: {link}")
            return

        logger.info(f"Starting scraping YouTube video: {link}")

        try:
            def extract_video_id(url):
                match = re.search(r'(?:v=|v\/|embed\/|youtu\.be\/|\/v\/|\/e\/|watch\?v=|watch\?.+&v=)([^#\&\?]{11})', url)
                return match.group(1) if match else None

            video_id = extract_video_id(link)
            if not video_id:
                print("Invalid YouTube URL")
                return

            ydl_opts = {"quiet": True, "skip_download": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(link, download=False)

            print(video_info.keys())

            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([entry['text'] for entry in transcript])

            print(f"Tags: {video_info['tags']}")
            
            user = kwargs["user"]
            instance = self.model(
                content=video_info,
                platform="youtube",
                author_id=user.id,
                author_full_name=user.full_name,

                name=video_info["title"],
                link=link,
                video_author=video_info['uploader'],
                description=video_info['description'],
                categories=video_info['categories'],
                transcript=transcript_text,
                tags=video_info['tags'],
                chapters=video_info['chapters']
                
            )
            instance.save()

        except Exception:
            raise

        logger.info(f"Finished scraping YouTube video: {link}")


