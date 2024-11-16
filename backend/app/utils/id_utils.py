import os
def get_next_numeric_id(directory_path="media"):
    try:
        # Check if the directory exists
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            return "1"

        # Get the list of folder names in the directory
        folder_names = os.listdir(directory_path)

        # Extract numeric folder names
        numeric_ids = [int(name) for name in folder_names if name.isdigit()]

        # Find the maximum number and return the next one
        if numeric_ids:
            return str(max(numeric_ids) + 1)
        else:
            return "1"
    except Exception as e:
        print(f"An error occurred while determining the next numeric ID: {e}")
        return None
