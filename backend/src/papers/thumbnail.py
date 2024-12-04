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
