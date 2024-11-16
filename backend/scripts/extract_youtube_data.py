import requests
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_CLOUD_API_KEY')
VIDEO_DETAILS_URL = 'https://www.googleapis.com/youtube/v3/videos'
COMMENTS_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
MEDIA_DIR = os.getenv('STATIC_DIR')

def get_next_numeric_id(directory_path=MEDIA_DIR):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return "1"

    folder_names = os.listdir(directory_path)
    numeric_ids = [int(name) for name in folder_names if name.isdigit()]
    return str(max(numeric_ids) + 1) if numeric_ids else "1"


def get_video_details(video_id):
    params = {
        'id': video_id,
        'part': 'snippet,statistics',
        'key': API_KEY
    }
    response = requests.get(VIDEO_DETAILS_URL, params=params).json()

    if 'items' in response and len(response['items']) > 0:
        video = response['items'][0]
        details = {
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'channel_title': video['snippet']['channelTitle'],
            'published_at': video['snippet']['publishedAt'],
            'view_count': video['statistics'].get('viewCount', 0),
            'like_count': video['statistics'].get('likeCount', 0),
            'comment_count': video['statistics'].get('commentCount', 0),
        }
        return details
    else:
        print("Video not found or API quota exceeded.")
        return {}


def get_comments(video_id, max_comments=1000):
    comments = []
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'maxResults': 100,
        'key': API_KEY
    }
    while len(comments) < max_comments:
        response = requests.get(COMMENTS_URL, params=params).json()

        if 'items' in response:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'comment': comment['textDisplay'],
                    'like_count': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })
        else:
            break

        
        if 'nextPageToken' in response:
            params['pageToken'] = response['nextPageToken']
        else:
            break

    return comments

def save_data_as_json(data, directory_path=MEDIA_DIR):
    next_id = get_next_numeric_id(directory_path)
    target_dir = os.path.join(directory_path, next_id)
    os.makedirs(target_dir, exist_ok=True)
    json_file_path = os.path.join(target_dir, "data.json")

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

    return next_id


if __name__ == '__main__':
    video_id = 'KPCSh79GCCE'  


    video_details = get_video_details(video_id)
    comments = get_comments(video_id, max_comments=500)

    data_to_save = {
        "video_details": video_details,
        "comments": comments
    }

    id= save_data_as_json(data_to_save)
    print(f"Data saved to media/{id}")
