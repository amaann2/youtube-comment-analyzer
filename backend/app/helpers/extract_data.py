import requests
from app import settings


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
    response = requests.get('https://www.googleapis.com/youtube/v3/videos', params=params).json()

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

def get_comments(video_id: str, max_comments: int):
    """
    Fetch comments and their replies using the YouTube Data API.
    """
    comments = []
    params = {
        "part": "snippet,replies", 
        "videoId": video_id,
        "maxResults": 100,
        "key": settings.google_cloud_api_key
    }

    while len(comments) < max_comments:
        response = requests.get('https://www.googleapis.com/youtube/v3/commentThreads', params=params).json()

        if "items" in response:
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comment_data = {
                    "author": comment["authorDisplayName"],
                    "comment": comment["textDisplay"],
                    "like_count": comment["likeCount"],
                    "published_at": comment["publishedAt"],
                    "replies": [] 
                }

                
                if "replies" in item:
                    for reply in item["replies"]["comments"]:
                        reply_snippet = reply["snippet"]
                        reply_data = {
                            "author": reply_snippet["authorDisplayName"],
                            "comment": reply_snippet["textDisplay"],
                            "like_count": reply_snippet["likeCount"],
                            "published_at": reply_snippet["publishedAt"]
                        }
                        comment_data["replies"].append(reply_data)
                comments.append(comment_data)
                
        else:
            break

        # Handle pagination
        if "nextPageToken" in response:
            params["pageToken"] = response["nextPageToken"]
        else:
            break

    print(f"Extracted {len(comments)} comments with replies.")
    return comments[:max_comments]

