from fastapi import APIRouter, HTTPException

from app.schemas.analyzer_schema import AnalyzeRepositoryRequest
from app.services.analyzer_service import RepositoryAnalyzer

router = APIRouter(
    prefix="/analyzer",
    tags=["Repository Analyzer"],
)


@router.post("/")
def analyze_repository(
    request: AnalyzeRepositoryRequest,
):

    try:

        analyzer = RepositoryAnalyzer(
            request.repository_path
        )

        result = analyzer.analyze()

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )