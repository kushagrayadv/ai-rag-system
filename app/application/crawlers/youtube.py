import time
from typing import List, Dict

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from loguru import logger

from app.domain.documents import VideoDocument
from .base import BaseSeleniumCrawler


class YouTubeCrawler(BaseSeleniumCrawler):
    model = VideoDocument

    def __init__(self, scroll_limit: int = 3) -> None:
        super().__init__(scroll_limit)

    def set_extra_driver_options(self, options) -> None:
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Video already exists in the database: {link}")
            return

        logger.info(f"Starting scraping YouTube video: {link}")

        self.driver.get(link)
        time.sleep(5)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        video_data = {
            "Title": self._scrape_section(soup, "h1", {"class": "title style-scope ytd-video-primary-info-renderer"}),
            "Description": self._scrape_section(soup, "yt-formatted-string", {"class": "content style-scope ytd-video-secondary-info-renderer"}),
            "Views": self._scrape_section(soup, "span", {"class": "view-count style-scope yt-view-count-renderer"}),
            "Likes": self._scrape_likes(),
            "Channel Name": self._scrape_section(soup, "yt-formatted-string", {"class": "style-scope ytd-channel-name"}),
            "Transcript": self._scrape_transcript(),
        }

        user = kwargs["user"]
        instance = self.model(
            content=video_data,
            name=video_data["Title"],
            link=link,
            platform="youtube",
            author_id=user.id,
            author_full_name=user.full_name,
        )
        instance.save()

        logger.info(f"Finished scraping YouTube video: {link}")

    def _scrape_section(self, soup: BeautifulSoup, tag: str, attrs: Dict[str, str]) -> str:
        """Scrape a specific section from the YouTube page."""
        element = soup.find(tag, attrs)
        return element.get_text(strip=True) if element else "N/A"

    def _scrape_likes(self) -> str:
        """Scrape the number of likes for the video."""
        try:
            like_button = self.driver.find_element(By.XPATH, '//*[contains(@aria-label, "like this video")]')
            return like_button.get_attribute("aria-label")
        except Exception as e:
            logger.warning(f"Error scraping likes: {e}")
            return "N/A"

    def _scrape_transcript(self) -> str:
        """Extract the transcript of the video if available."""
        try:
            logger.info("Attempting to extract video transcript.")

            # Open the '...' menu for more options
            more_options_button = self.driver.find_element(By.XPATH, '//button[@aria-label="More actions"]')
            more_options_button.click()
            time.sleep(2)

            # Click on the 'Show transcript' button
            transcript_button = self.driver.find_element(By.XPATH, '//yt-formatted-string[text()="Show transcript"]')
            transcript_button.click()
            time.sleep(2)

            # Scroll and extract the transcript content
            transcript_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            transcript_items = transcript_soup.find_all("div", {"class": "cue-group style-scope ytd-transcript-body-renderer"})

            transcript = []
            for item in transcript_items:
                timestamp = item.find("span", {"class": "cue-time style-scope ytd-transcript-body-renderer"}).get_text(strip=True)
                text = item.find("span", {"class": "cue style-scope ytd-transcript-body-renderer"}).get_text(strip=True)
                transcript.append(f"{timestamp}: {text}")

            logger.info("Transcript extracted successfully.")
            return "\n".join(transcript)

        except Exception as e:
            logger.warning(f"Error extracting transcript: {e}")
            return "Transcript not available."
