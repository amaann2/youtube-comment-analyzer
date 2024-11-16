import requests
import json
import os
from app import settings

VIDEO_DETAILS_URL = "https://www.googleapis.com/youtube/v3/videos"
COMMENTS_URL = "https://www.googleapis.com/youtube/v3/commentThreads"
MAX_COMMENTS_TO_EXTRACT = 6000

def get_video_id_from_url(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    """
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    raise ValueError("Invalid YouTube URL format.")

def get_video_details(video_id: str):
    """
    Fetch video details using the YouTube Data API.
    """
    params = {
        "id": video_id,
        "part": "snippet,statistics",
        "key": settings.google_cloud_api_key
    }
    response = requests.get(VIDEO_DETAILS_URL, params=params).json()

    if "items" in response and response["items"]:
        video = response["items"][0]
        return {
            "title": video["snippet"]["title"],
            "description": video["snippet"]["description"],
            "channel_title": video["snippet"]["channelTitle"],
            "published_at": video["snippet"]["publishedAt"],
            "view_count": video["statistics"].get("viewCount", 0),
            "like_count": video["statistics"].get("likeCount", 0),
            "comment_count": video["statistics"].get("commentCount", 0),
        }
    raise ValueError("Failed to fetch video details or API quota exceeded.")

def get_comments(video_id: str):
    """
    Fetch comments using the YouTube Data API.
    """
    comments = []
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 100,
        "key": settings.google_cloud_api_key
    }

    while len(comments) < MAX_COMMENTS_TO_EXTRACT:
        response = requests.get(COMMENTS_URL, params=params).json()

        if "items" in response:
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": comment["authorDisplayName"],
                    "comment": comment["textDisplay"],
                    "like_count": comment["likeCount"],
                    "published_at": comment["publishedAt"]
                })
        else:
            break

        if "nextPageToken" in response:
            params["pageToken"] = response["nextPageToken"]
        else:
            break
    print(f"Extracted {len(comments)} comments.")
    return comments[:MAX_COMMENTS_TO_EXTRACT]

def save_data_as_json(data: dict, video_id: str) -> str:
    """
    Save video details and comments as a JSON file.
    """
    directory = os.path.join(settings.static_dir, video_id)
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, "data.json")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return file_path
