from fastapi import APIRouter

from app.utils.decorator import try_catch_decorator
from app.services.analysis_service import process_youtube_data, sentiment_analysis, analyze_common_words, get_top_ten_comments
from app.schemas.analysis_schema import AnalysisRequest, AiReplyRequest
from app.utils.save_data import save_data_as_json
from app.utils.id_utils import get_next_numeric_id
from app.prompt.comment_reply import generate_ai_reply_prompt
from app.helpers.llm_helper import get_llm
from langchain_core.prompts import ChatPromptTemplate

router = APIRouter(prefix="/analysis", tags=["YouTube Analysis"])

@router.post("/")
@try_catch_decorator()
async def extract_youtube_data(request: AnalysisRequest):
    """
    Endpoint to extract video details and comments from a given YouTube URL.
    """
    id = get_next_numeric_id()

    # Create and await all tasks
    result = await process_youtube_data(request.url, request.max_comments)
    sentiment_result = await sentiment_analysis(result)
    common_words_result = await analyze_common_words(result)
    top_ten_comments = await get_top_ten_comments(result)

    save_data = {
        "id": id,
        **sentiment_result,
        **common_words_result,
        **top_ten_comments,
        **result
    }
    save_data_as_json(save_data, id)

    return {
        "id": id,
        "success": True
    }


@router.post("/ai-reply")
@try_catch_decorator()
async def generate_ai_reply(request: AiReplyRequest):
    llm = get_llm()
    prompt = generate_ai_reply_prompt(request.comment, request.video_details)
    
    # Define the chat prompt template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that can answer questions."),
        ("user", "{input}")
    ])


    prompt_with_input = prompt_template | llm
    response = prompt_with_input.invoke({"input": prompt})
    return {
        "reply": response.content
    }
        