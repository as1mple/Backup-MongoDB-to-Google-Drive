import json
import requests


def get_files_by_chat_id(host: str, port: str, chat_id: str) -> dict:
    """Get files by chat id."""
    params = {
        "user_id": chat_id,
    }
    return requests.get(f"http://{host}:{port}/get/data", params=params).json()


def get_save_data(host: str, port: str, time_from: str, time_to: str) -> dict:
    """Get save data."""
    params = {
        "time_from": time_from,
        "time_to": time_to,
    }
    return requests.get(f"http://{host}:{port}/get/data", params=params).json()


def upload_file(token: str, file: bytes, file_name: str, parents: str) -> dict:
    """Upload file to Google Drive."."""
    headers = {"Authorization": f"Bearer {token}"}

    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"

    params = {
        "name": file_name,
        "parents": [parents],
    }

    files = {
        "data": ("metadata", json.dumps(params), "application/json;charset=UTF-8"),
        "file": file,
    }
    return requests.post(url, headers=headers, files=files).json()


def create_folder(token: str, folder_name: str, parents=None) -> dict:
    """Create folder in Google Drive."""
    headers = {"Authorization": f"Bearer {token}"}

    url = "https://www.googleapis.com/upload/drive/v3/files"

    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }

    if parents:
        file_metadata["parents"] = [parents]

    file_with_metadata = {
        "data": ("metadata", json.dumps(file_metadata), "application/json; charset=UTF-8")
    }

    return requests.post(url, headers=headers, files=file_with_metadata).json()
