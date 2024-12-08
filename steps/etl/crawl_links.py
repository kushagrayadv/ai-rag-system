import json
from typing import Dict, List
from urllib.parse import urlparse

from clearml import Task
from loguru import logger
from tqdm import tqdm

from application.crawlers.dispatcher import CrawlerDispatcher
from domain.documents import UserDocument


def crawl_links(user: UserDocument, links: List[str]) -> List[str]:
  try:
    def _crawl_link(dispatcher: CrawlerDispatcher, link: str, user: UserDocument) -> tuple[bool, str]:
      crawler = dispatcher.get_crawler(link)
      crawler_domain = urlparse(link).netloc

      try:
        crawler.extract(link=link, user=user)
        return True, crawler_domain
      except Exception as e:
        logger.error(f"An error occurred while crawling: {e!s}")
        return False, crawler_domain

    def _add_to_metadata(metadata: Dict, domain: str, successful_crawl: bool) -> dict:
      if domain not in metadata:
        metadata[domain] = {"successful": 0, "total": 0}
      metadata[domain]["successful"] += int(successful_crawl)
      metadata[domain]["total"] += 1
      return metadata

    links = json.loads(links)
    dispatcher = CrawlerDispatcher.build().register_github().register_youtube()

    logger.info(f"Starting to crawl {len(links)} link(s).")

    metadata = {}
    successful_crawls = 0
    for link in tqdm(links):
      successful_crawl, crawled_domain = _crawl_link(dispatcher, link, user)
      successful_crawls += successful_crawl

      metadata = _add_to_metadata(metadata, crawled_domain, successful_crawl)

    task = Task.current_task()
    task.upload_artifact("crawled_links", metadata)

    logger.info(f"Successfully crawled {successful_crawls} / {len(links)} links.")
    print(links)

    return links

  except Exception as e:
    print(f"An error occurred: {type(e).__name__}")
    print(f"Error message: {str(e)}")
