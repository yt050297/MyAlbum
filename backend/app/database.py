import os
import sys

# ベースパスを指定（例: backend/app ディレクトリ）
base_path = os.path.dirname(os.path.abspath(__file__))  # __file__はこのスクリプトのパス
if base_path not in sys.path:
    sys.path.append(base_path)

from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv  # dotenvをインポート

# .envファイルの読み込み
load_dotenv()

DATABASE_USER = os.getenv("POSTGRES_USER", "Admin")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Admin")
DATABASE_NAME = os.getenv("POSTGRES_DB", "database")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

# PostgreSQL の接続URL
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# データベースエンジンを作成
engine = create_engine(DATABASE_URL)


# データベースセッションを取得する依存関係
def get_db():
    with Session(engine) as session:
        yield session


# テーブルを作成
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
