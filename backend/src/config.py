import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class MailSettings(BaseModel):
    """Mail server settings."""

    sendgrid_api_key: str
    sendgrid_from_email: str


class MongoSettings(BaseModel):
    """MongoDB settings."""

    uri: str = "mongodb://localhost:27017"
    db_name: str = "paperhub"


class ThumbnailSettings(BaseModel):
    """Thumbnail settings."""

    width: int = 600
    format: str = "jpg"
    quality: int = 50
    local_folder: str = "thumbnails"
    max_workers: int = 5


class ArxivSettings(BaseModel):
    """Arxiv settings."""

    max_results: int = 10
    source_url_base: str = "https://arxiv.org/abs/"


class Settings(BaseSettings):
    """Server config settings."""

    # Server settings
    root_url: str = "http://localhost:8000"
    dev: bool = False
    version: str = "0.1.0"
    firebase_cert_path: str = "firebase-cert.json"

    # Mongo Engine settings
    mongo: MongoSettings = MongoSettings()

    # FastMail SMTP server settings
    mail: MailSettings

    # Thumbnail settings
    thumbnail: ThumbnailSettings = ThumbnailSettings()

    # Arxiv settings
    arxiv: ArxivSettings = ArxivSettings()

    model_config = SettingsConfigDict(env_nested_delimiter="__")


CONFIG = Settings()
"""Global configuration object."""


if not os.path.exists(CONFIG.thumbnail.local_folder):
    os.makedirs(os.path.abspath(CONFIG.thumbnail.local_folder))
