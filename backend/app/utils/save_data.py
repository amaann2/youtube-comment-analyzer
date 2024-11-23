import json
import os
from app import settings

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