# FastAPI(Python) Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 必要なパッケージのインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションのコードをコピー
COPY ./app /app

# アプリケーションの起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
