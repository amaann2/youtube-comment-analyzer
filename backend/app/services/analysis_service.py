from app.helpers.extract_data import get_video_id_from_url, get_video_details, get_comments, save_data_as_json
from app.utils.id_utils import get_next_numeric_id

async def process_youtube_data(url: str):
    """
    Orchestrates the extraction and saving of YouTube video details and comments.
    Args:
        url: The YouTube video URL.
    Returns:
        A dictionary containing the processed data.
    """

    id = get_next_numeric_id()
    video_id = get_video_id_from_url(url)
    

    video_details = get_video_details(video_id)
    video_details['url'] = url  
    
 
    comments = get_comments(video_id)
    
   
    data = {
        "video_details": video_details,
        "comments": comments,
    }
    save_data_as_json(data, id)

    return {"id": id, "data": data}
