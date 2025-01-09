FROM python:3.12-slim

WORKDIR /fastapi

COPY ./requirements.txt /fastapi/requirements.txt

# Update package list and install poppler-utils for pdf2img
RUN apt-get update && apt-get install -y poppler-utils && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade -r /fastapi/requirements.txt

COPY ./src /fastapi/src

CMD ["fastapi", "run", "src/main.py", "--port", "8000"]