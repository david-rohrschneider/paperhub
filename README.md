# Paperhub 📚

Paperhub lets you explore research papers and curate your own reading list. Metadata is fetched from Semantic Scholar, users authenticate via Firebase, and files are stored in MongoDB. Everything is wired together through **Docker Compose** for easy local development.

## Tech stack 🚀

- **Docker Compose** 🐳 – orchestrates the stack
- **Backend** ⚙️ – FastAPI, MongoDB with Beanie ODM, Semantic Scholar client and Firebase authentication
- **Frontend** 🎨 – Vue 3 with Vite and PrimeVue, powered by Bun

## Quick start with Docker

1. Copy `.env.example` to `.env` and set `SYSTEM_FIREBASE_CERT_PATH` to your Firebase service account JSON file.
2. Follow [`backend/README.md`](backend/README.md) and [`frontend/README.md`](frontend/README.md) to create the `.env.docker` and `.env` files for each service.
3. Bring up all services:
   ```bash
   docker compose up --build
   ```
   This starts the database, backend API and frontend app.

For manual installation and additional commands see [`backend/README.md`](backend/README.md) and [`frontend/README.md`](frontend/README.md).
