import logging
import os

import asyncio
from httpx import AsyncClient
from pdf2image import convert_from_bytes
from PIL.Image import Image

from src.adapters import s3_adapter
from src.config import CONFIG


logger = logging.getLogger(__name__)


async def generate_thumbnail_from_url(
    url: str, name: str, client: AsyncClient
) -> Image | None:
    """Generate a thumbnail image from a PDF URL.

    Args:
        url (str): PDF URL.
        name (str): Thumbnail name.
        client (AsyncClient): HTTPX Async Client.

    Returns:
        Image | None: Thumbnail PIL Image or None if an error occurred.
    """
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
            first_page=1,
            last_page=1,
            fmt=CONFIG.thumbnail.format,
            jpegopt={"quality": CONFIG.thumbnail.quality},
            size=(CONFIG.thumbnail.width, None),
        )

        img_path = os.path.join(
            CONFIG.thumbnail.local_folder, name + "." + CONFIG.thumbnail.format
        )
        if os.path.exists(img_path):
            os.remove(img_path)

        if not images:
            return None

        return images[0]

    except Exception as e:
        logger.error(f"Error generating thumbnail:\n{e}\n")
        return None


async def generate_thumbnails(
    url_names: list[tuple[str, str]]
) -> dict[str, str | None]:
    """Simultaneously generate thumbnail images from PDF URLs.

    Args:
        url_names (list[tuple[str, str]]): List of PDF URLs and Thumbnail names.

    Returns:
        dict[str, str | None]: Dictionary of Thumbnail names and S3 presigned URLs.
    """
    semaphore = asyncio.Semaphore(10)

    async with AsyncClient() as client:

        async def sem_task(url: str, name: str):
            async with semaphore:
                if not s3_adapter.exists(name):
                    img = await generate_thumbnail_from_url(url, name, client)

                    if not img:
                        return name, None

                    s3_adapter.upload_from_pil(name, img)

                return name, s3_adapter.get_presigned_url(name)

        tasks = [sem_task(url, name) for url, name in url_names]
        results = await asyncio.gather(*tasks)

    return {name: url for name, url in results}
