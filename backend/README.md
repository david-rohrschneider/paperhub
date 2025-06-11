# Backend ⚙️

The backend is a FastAPI application that pulls metadata from Semantic Scholar and stores user information in MongoDB. Authentication is managed with Firebase and thumbnails are stored on S3/Minio.

## Tech stack

- **Python 3.12** 🐍
- **FastAPI** 🚀
- **MongoDB** with Beanie ODM 🍃
- **Firebase Admin SDK** 🔥
- **Semantic Scholar client** 📚
- **Minio/S3** for thumbnails 🖼️

## Installation

1. `cd backend`
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.development.example` to `.env.development` and fill in the environment variables.
5. (Optional) copy `.env.docker.example` to `.env.docker` if you plan to run the backend via Docker.

## Running locally

Make sure MongoDB and Minio are running. They can be started via Docker Compose from the repository root:
```bash
docker compose up paperhub-db paperhub-minio create-buckets --build -d
```

Then launch the API:
```bash
uvicorn src.main:app --host localhost --port 8000 --env-file .env.development
```

Format the code before committing:
```bash
black src
```
