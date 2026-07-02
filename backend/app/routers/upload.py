from fastapi import APIRouter, UploadFile, File
from app.services.storage_service import save_uploaded_file

router = APIRouter()

@router.post("/upload")
def upload():
    return {
        "success": True,
        "message": "Upload received"
    }
    
@router.post("/upload/file")
async def upload_file(file: UploadFile=File(...)):
    saved = save_uploaded_file(file)
    return {
        "filename": file.filename,
        "size": file.size,
        "content_type": file.content_type,
        **saved
    }