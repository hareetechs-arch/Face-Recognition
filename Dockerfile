FROM python:3.10

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 --retries 10 -r requirements.txt


COPY . .

CMD ["sh", "-c", "uvicorn face_server:app --host 0.0.0.0 --port $PORT"]
