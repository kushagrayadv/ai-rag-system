from urllib.parse import urlparse

from loguru import logger
from tqdm import tqdm
from clearml import Task, Logger

from project.application.crawlers.dispatcher import CrawlerDispatcher
from project.domain.documents import UserDocument


def crawl_links(user: UserDocument, links: list[str]) -> list[str]:
    task = Task.init(project_name="Link Crawling", task_name="Crawl Links")
    task.connect(links)
    task.connect(user)

    dispatcher = CrawlerDispatcher.build().register_linkedin().register_medium().register_github()

    logger.info(f"Starting to crawl {len(links)} link(s).")

    metadata = {}
    successful_crawls = 0
    for link in tqdm(links):
        successful_crawl, crawled_domain = _crawl_link(dispatcher, link, user)
        successful_crawls += successful_crawl

        metadata = _add_to_metadata(metadata, crawled_domain, successful_crawl)

    Logger.current_logger().report_table(
        title="Crawl Results",
        series="domain_stats",
        iteration=0,
        table_plot=metadata
    )

    logger.info(f"Successfully crawled {successful_crawls} / {len(links)} links.")

    return links


def _crawl_link(dispatcher: CrawlerDispatcher, link: str, user: UserDocument) -> tuple[bool, str]:
    crawler = dispatcher.get_crawler(link)
    crawler_domain = urlparse(link).netloc

    try:
        crawler.extract(link=link, user=user)
        return True, crawler_domain
    except Exception as e:
        logger.error(f"An error occurred while crawling: {e!s}")
        return False, crawler_domain


def _add_to_metadata(metadata: dict, domain: str, successful_crawl: bool) -> dict:
    if domain not in metadata:
        metadata[domain] = {"successful": 0, "total": 0}
    metadata[domain]["successful"] += int(successful_crawl)
    metadata[domain]["total"] += 1
    return metadata