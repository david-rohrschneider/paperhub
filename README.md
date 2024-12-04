# paperhub

## Backend

- FastAPI (Server)
- MongoDB (Database)
- Beanie (ORM)
- Firebase (User Auth)
- Black (Formatter)

### Installation
1. `cd backend`
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `cp .env.development.example .env.development`
6. Fill in necessary environment variables

### Run
1. Initialize local mongodb via docker:
   - `cd ..`
   - `docker compose up paperhub-db --build -d`
2. Run the server
```bash
uvicorn src.main:app --host localhost --port 8000 --env-file .env.development
```

### Before you commit
```bash
cd backend && source venv/bin/activate && black src
```