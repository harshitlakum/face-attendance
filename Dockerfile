FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential cmake pkg-config libopenblas-dev libgl1 libgtk2.0-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
RUN mkdir -p data

ENV DB_PATH=data/embeddings.sqlite PYTHONUNBUFFERED=1
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
