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
                print("with block")
                video_info = ydl.extract_info(link, download=False)

            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([entry['text'] for entry in transcript])

            print("before video_content")
            video_content = {}

            video_content['title'] = video_info['title']
            video_content['description'] = video_info['description']
            video_content['id'] = video_info['id']
            video_content['tags'] = ', '.join(video_info['tags'])
            video_content['categories'] = ', '.join(video_info['categories'])
            video_content['transcript'] = transcript_text

            print("after video_content")

            user = kwargs["user"]
            instance = self.model(
                content=video_content,
                platform="youtube",
                author_id=user.id,
                author_full_name=user.full_name,
                name=video_info["title"],
                link=link,                
            )
            instance.save()

        except Exception:
            raise

        logger.info(f"Finished scraping YouTube video: {link}")


