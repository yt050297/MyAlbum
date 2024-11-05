import os
import sys

# ベースパスを指定（例: backend/app ディレクトリ）
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if base_path not in sys.path:
    sys.path.append(base_path)

print("Python executable:", sys.executable)
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import ValidationError
from models import Image_info
from services.upload_images import save_file
from datetime import datetime
from database import get_db
from schemas import UploadImage
import shutil
import os
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/upload-image/")
async def upload_image(
    image_data: UploadImage,  # Pydanticモデルで受け取る
    db: Session = Depends(get_db),
):
    file_location = save_file(
        image_data,
        f"{image_data.title}_{datetime.now().timestamp()}.jpeg",
    )

    # データベースに記録
    image_record = Image_info(
        title=image_data.title,
        album_date=image_data.album_date,
        file_path=file_location,
        upload_date=datetime.utcnow(),
    )
    db.add(image_record)
    db.commit()

    return JSONResponse(
        content={
            "result": "true",
            "message": f"File saved to {file_location}",
        },
        status_code=201,
    )
