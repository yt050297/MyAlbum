import os
import sys

# ベースパスを指定（例: backend/app ディレクトリ）
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if base_path not in sys.path:
    sys.path.append(base_path)

from fastapi import UploadFile, HTTPException
import base64


UPLOAD_BASE_DIRECTORY = os.path.abspath(
    os.path.join(base_path, "../public/uploaded_images")
)


def save_file(image_data: object, filename: str) -> str:
    upload_directory = os.path.join(
        UPLOAD_BASE_DIRECTORY, image_data.title + "-" + image_data.album_date
    )
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    # Base64デコード
    file_data = base64.b64decode(image_data.file)
    file_location = os.path.join(upload_directory, filename)

    # ファイルに書き込む
    with open(file_location, "wb") as buffer:
        buffer.write(file_data)

    return file_location
