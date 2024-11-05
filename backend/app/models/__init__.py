from sqlmodel import SQLModel, Field
from datetime import datetime


class Image_info(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    album_date: str
    file_path: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
