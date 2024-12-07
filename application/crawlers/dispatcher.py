import re
from urllib.parse import urlparse

from loguru import logger

from .base import BaseCrawler
from .github import GithubCrawler
from .youtube import YouTubeCrawler


class CrawlerDispatcher:
    def __init__(self) -> None:
        self._crawlers = {}

    @classmethod
    def build(cls) -> "CrawlerDispatcher":
        dispatcher = cls()

        return dispatcher

    def register_github(self) -> "CrawlerDispatcher":
        self.register("https://github.com", GithubCrawler)

        return self
    
    def register_youtube(self) -> "CrawlerDispatcher":
        self.register("https://youtube.com", YouTubeCrawler)

        return self

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        parsed_domain = urlparse(domain)
        domain = parsed_domain.netloc

        self._crawlers[r"https://(www\.)?{}/*".format(re.escape(domain))] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        print("BaseCrawler:", url)
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()
        else:
            logger.error(f"No crawler found for {url}.")
            raise Exception(f"No crawler found for {url}")
