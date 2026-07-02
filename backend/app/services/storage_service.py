from pathlib import Path
import shutil
import tempfile
from fastapi import UploadFile

def save_uploaded_file(file: UploadFile):
    temp_dir = Path(tempfile.mkdtemp())
    
    destination = temp_dir/ file.filename
    
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "directory": str(temp_dir),
        "filepath": str(destination)
    }