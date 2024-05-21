import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError

from scraper.models import Link, Page

logger = logging.getLogger(__name__)


def get_links(url: str, timeout: int = 5) -> tuple[str, list[tuple[str, str]]]:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        raise

    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.title.string if soup.title and soup.title.string else ""
    links = soup.find_all("a", href=True)
    return name, [
        (urljoin(url, link["href"]), link.text.strip()[:126])
        for link in links
        if link.text and link.text.strip()
    ]


def create_page(url: str) -> None:

    page, created = Page.objects.get_or_create(url=url)
    if created:
        page_name, links = get_links(url)
        page.name = page_name or url
        page.save()

        link_instances = []
        seen_urls = set()
        for link, name in links:
            if link in seen_urls:
                continue
            seen_urls.add(link)
            name = name or link
            link_instance = Link(url=link, name=name, page=page)
            link_instances.append(link_instance)

        try:
            Link.objects.bulk_create(link_instances)
        except IntegrityError as e:
            logger.error(f"Error creating links for {url}: {e}")

    else:
        logger.info(f"Page {url} already exists")
