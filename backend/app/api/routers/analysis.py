from fastapi import APIRouter

from app.utils.decorator import try_catch_decorator
from app.services.analysis_service import process_youtube_data

router = APIRouter(prefix="/analysis", tags=["YouTube Analysis"])

@router.post("/")
@try_catch_decorator()
async def extract_youtube_data(url: str):
    """
    Endpoint to extract video details and comments from a given YouTube URL.
    """
    return await process_youtube_data(url)

