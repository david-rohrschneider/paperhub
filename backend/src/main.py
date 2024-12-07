import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from beanie import init_beanie
import firebase_admin
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from src.auth.dependencies import current_user
from src.config import CONFIG
from src.users.models import User
from src.users.routes import router as UsersRouter
from src.libraries.models import Library
from src.libraries.routes import router as LibrariesRouter
from src.papers.models import Paper
from src.papers.routes import router as PapersRouter


logging.basicConfig(level=logging.INFO)
__logger = logging.getLogger(__name__)


DESCRIPTION = """
This API powers paperhub.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes application services."""

    app.mongodb_client = AsyncIOMotorClient(CONFIG.mongo.uri)
    app.db = app.mongodb_client.get_database(CONFIG.mongo.db_name)

    ping_response = await app.db.command("ping")

    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")

    __logger.info("MongoDB connection initialized successfully")

    await init_beanie(app.db, document_models=[User])
    __logger.info("Beanie initialized successfully")

    credential = firebase_admin.credentials.Certificate(CONFIG.firebase_cert_path)
    firebase_admin.initialize_app(credential=credential)
    __logger.info("Firebase app initialized successfully")

    yield

    app.mongodb_client.close()
    __logger.info("MongoDB connection closed")


app = FastAPI(
    title="paperhub API",
    description=DESCRIPTION,
    version=CONFIG.version,
    lifespan=lifespan,
    dependencies=[Depends(current_user)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UsersRouter)
app.include_router(LibrariesRouter)
app.include_router(PapersRouter)
