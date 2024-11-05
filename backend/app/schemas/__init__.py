# Pydanticを使用したスキーマ定義
from pydantic import BaseModel
from datetime import date


class UploadImage(BaseModel):
    title: str
    album_date: str
    file: str
