from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    url: str
    max_comments: int = 6000 

class AiReplyRequest(BaseModel):
    comment: dict
    video_details: dict

