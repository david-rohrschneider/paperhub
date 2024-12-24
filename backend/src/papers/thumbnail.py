import logging
import os

import asyncio
from httpx import AsyncClient
from pdf2image import convert_from_bytes

from src.config import CONFIG


logger = logging.getLogger(__name__)


async def generate_thumbnail_from_url(
    url: str, name: str, client: AsyncClient
) -> str | None:
    """Generate a thumbnail image from a PDF URL.

    Args:
        url (str): PDF URL.
        name (str): Thumbnail name.
        client (AsyncClient): HTTPX Async Client.

    Returns:
        str | None: Local Thumbnail URL.
    """
    file_path = f"{CONFIG.thumbnail.local_folder}/{name}.{CONFIG.thumbnail.format}"

    if os.path.exists(file_path):
        return file_path

    try:
        response = await client.get(url, follow_redirects=True, timeout=None)

        if response.status_code != 200:
            return None

        if "application/pdf" not in response.headers.get("Content-Type"):
            return None

        images = convert_from_bytes(
            response.content,
            output_folder=CONFIG.thumbnail.local_folder,
            single_file=True,
            output_file=name,
            paths_only=True,
            first_page=1,
            last_page=1,
            fmt=CONFIG.thumbnail.format,
            jpegopt={"quality": CONFIG.thumbnail.quality},
            size=(CONFIG.thumbnail.width, None),
        )

        return images[0]
    except Exception as e:
        logger.error(f"Error generating thumbnail:\n{e}\n")
        return None


async def generate_thumbnails(url_names: list[tuple[str, str]]) -> list[str | None]:
    """Simultaneously generate thumbnail images from PDF URLs.

    Args:
        url_names (list[tuple[str, str]]): List of PDF URLs and Thumbnail names.

    Returns:
        list[str | None]: Local Thumbnail URLs.
    """
    semaphore = asyncio.Semaphore(10)

    async with AsyncClient() as client:

        async def sem_task(url, name):
            async with semaphore:
                return await generate_thumbnail_from_url(url, name, client)

        tasks = [sem_task(url, name) for url, name in url_names]
        results = await asyncio.gather(*tasks)

    return results
