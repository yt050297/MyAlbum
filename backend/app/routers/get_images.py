from fastapi import APIRouter
from services.get_images import list_image_files
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/get-images/")
async def get_image_list():
    try:
        folder_structure = list_image_files()
        return JSONResponse(content=folder_structure)
    except Exception as e:
        print("Error in list_image_files:", str(e))  # エラーログ
        return JSONResponse(content={"error": "Failed to list images"}, status_code=500)
