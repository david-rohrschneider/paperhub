import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class MailSettings(BaseModel):

    sendgrid_api_key: str = ""
    sendgrid_from_email: str = ""


class MongoSettings(BaseModel):

    uri: str = "mongodb://localhost:27017"
    db_name: str = "paperhub"


class ThumbnailSettings(BaseModel):

    width: int = 600
    format: str = "jpg"
    quality: int = 50
    local_folder: str = "thumbnails"


class FeedSettings(BaseModel):

    num_positive_samples: int = 50


class S3Settings(BaseModel):

    thumbnails_bucket: str = "thumbnails"
    thumbnail_content_type: str = "image/jpeg"
    presigned_url_expiry: int = 3600

    # only used locally because of internal presigned URL generation
    dev_endpoint: str | None = None


class Settings(BaseSettings):
    """Server config settings."""

    # General settings
    frontend_url: str = "http://localhost:5173"
    version: str = "0.1.0"
    firebase_cert_path: str = "firebase-cert.json"

    # Mongo Engine settings
    mongo: MongoSettings = MongoSettings()

    # FastMail SMTP server settings
    mail: MailSettings = MailSettings()

    # Thumbnail settings
    thumbnail: ThumbnailSettings = ThumbnailSettings()

    # Feed settings
    feed: FeedSettings = FeedSettings()

    # S3 settings
    s3: S3Settings = S3Settings()
    aws_endpoint_url: str

    model_config = SettingsConfigDict(env_nested_delimiter="__")


CONFIG = Settings()
"""Global configuration object."""


if not os.path.exists(CONFIG.thumbnail.local_folder):
    os.makedirs(os.path.abspath(CONFIG.thumbnail.local_folder))
