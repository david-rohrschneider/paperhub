from concurrent.futures import ThreadPoolExecutor
import requests
from pdf2image import convert_from_bytes

from src.config import CONFIG


def generate_thumbnail_from_url(url: str, name: str) -> str:
    """Generate a thumbnail image from a PDF URL.

    Args:
        url (str): PDF URL.
        name (str): Thumbnail name.

    Returns:
        str: Local Thumbnail URL.
    """
    response = requests.get(url)

    if response.status_code != 200:
        return None

    if response.headers.get("Content-Type") != "application/pdf":
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


def generate_thumbnails_from_urls(urls: list[str], names: list[str]) -> list[str]:
    """Simoultaniously generate thumbnail images from PDF URLs.

    Args:
        urls (list[str]): PDF URLs.
        names (list[str]): Thumbnail names.

    Returns:
        list[str]: Local Thumbnail URLs.
    """
    params = list(zip(urls, names))
    thread_fn = lambda x: generate_thumbnail_from_url(*x)

    with ThreadPoolExecutor(max_workers=CONFIG.thumbnail.max_workers) as executor:
        results = list(executor.map(thread_fn, params))

    return results
