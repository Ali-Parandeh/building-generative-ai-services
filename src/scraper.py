import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup
from loguru import logger


def extract_urls(text: str) -> list[str]:
    url_pattern = r"(?P<url>https?:\/\/[^\s]+)"
    urls = re.findall(url_pattern, text)
    return urls


def parse_inner_text(html_string: str) -> str:
    soup = BeautifulSoup(html_string, "lxml")
    content = soup.find("div", id="bodyContent").get_text(strip=True)
    if len(content) == 0:
        logger.warning("Could not parse the HTML content")
    return content


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        html_string = await response.text()
        return parse_inner_text(html_string)


async def fetch_all(urls: list[str]) -> str:
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls], return_exceptions=True
        )
    return " ".join(results)
