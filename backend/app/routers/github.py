from fastapi import APIRouter
from app.services.github_service import clone_repository
from app.schemas.github_schema import CloneRepositoryRequest

router = APIRouter()

@router.post("/github")
async def upload_github(request: CloneRepositoryRequest):
    return clone_repository(request.url)
    