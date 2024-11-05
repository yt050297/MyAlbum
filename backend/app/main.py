import sys
import os

# ベースパスを指定（例: backend/app ディレクトリ）
base_path = os.path.dirname(os.path.abspath(__file__))  # __file__はこのスクリプトのパス
if base_path not in sys.path:
    sys.path.append(base_path)

# ここでモジュールをインポート

from routers import upload_image, get_images
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine
from database import create_db_and_tables, engine
import uvicorn

app = FastAPI()

app.include_router(upload_image.router)
app.include_router(get_images.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# 許可するオリジンのリスト
origins = [
    "http://localhost:3000",  # Reactアプリが動いているポート
]

# CORSミドルウェアの追加
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # 許可するオリジンを設定
    allow_origins="*",
    allow_credentials=True,  # Cookieを含める場合はTrueに設定
    allow_methods=["*"],  # 許可するHTTPメソッド（GET, POSTなど）
    allow_headers=["*"],  # 許可するHTTPヘッダー
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
