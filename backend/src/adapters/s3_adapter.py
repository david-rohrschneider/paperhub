import io

import boto3
from botocore.exceptions import ClientError
from PIL.Image import Image

from src.config import CONFIG


__s3_client = boto3.client("s3")
__s3 = boto3.resource("s3")
__thumbnails_bucket = __s3.Bucket(CONFIG.s3.thumbnails_bucket)


def upload_from_pil(paper_id: str, thumbnail: Image) -> None:
    """Upload a thumbnail image to S3.

    Args:
        paper_id (str): Paper ID.
        thumbnail (Image): Thumbnail PIL image.
    """
    file_obj = io.BytesIO()
    thumbnail.save(file_obj, format=thumbnail.format)
    file_obj.seek(0)
    __thumbnails_bucket.upload_fileobj(
        file_obj,
        paper_id,
        {"ContentType": CONFIG.s3.thumbnail_content_type},
    )


def get_presigned_url(paper_id) -> str:
    """Get a presigned URL for the specified paper thumbnail.

    Args:
        paper_id (str): Paper ID.

    Returns:
        str: Presigned URL.
    """
    url: str = __s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": __thumbnails_bucket.name, "Key": paper_id},
        ExpiresIn=CONFIG.s3.presigned_url_expiry,
    )

    if CONFIG.s3.dev_endpoint is not None:
        url = url.replace(CONFIG.aws_endpoint_url, CONFIG.s3.dev_endpoint)

    return url


def exists(paper_id: str) -> bool:
    """Check if a thumbnail exists in S3.

    Args:
        paper_id (str): Paper ID.

    Returns:
        bool: True if the thumbnail exists, False otherwise
    """
    try:
        __s3_client.head_object(Bucket=__thumbnails_bucket.name, Key=paper_id)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise
