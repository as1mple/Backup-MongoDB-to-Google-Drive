import yaml
import pandas as pd
from tqdm import tqdm

import json
import base64

from modules.requsets import get_files_by_chat_id, upload_file, create_folder

PATH_TO_USERS_CSV = "resources/data/users.csv"
PATH_TO_USERS_DATA = "resources/data/users.json"
PATH_TO_CREDENTIALS = "resources/credentials.yaml"
PATH_TO_INPUT_DATA = "resources/data/input_data.txt"
PATH_TO_FOLDERS_DATA = "resources/data/folders.json"

with open(PATH_TO_INPUT_DATA, "r") as f:
    USERS = f.read().splitlines()

with open(PATH_TO_CREDENTIALS) as f:
    credentials = yaml.safe_load(f)

TOKEN = credentials["google-drive"]["token"]
ROOT_FOLDER = credentials["google-drive"]["root-folder"]
HOST = credentials["database"]["host"]
PORT = credentials["database"]["port"]

if __name__ == "__main__":
    try:
        with open(PATH_TO_USERS_DATA, "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    try:
        index = int(list(users.keys())[-1])
    except IndexError:
        index = 0

    try:
        with open(PATH_TO_FOLDERS_DATA, "r") as f:
            df = json.load(f)
    except FileNotFoundError:
        df = {}

    for user_id in USERS:
        print(user_id)
        if not df.get(user_id):
            while True:
                try:
                    response = create_folder(TOKEN, user_id, ROOT_FOLDER)

                    if not response.get("error"):
                        break

                    print(response)
                    TOKEN = input("New token = ")
                except Exception as e:
                    print(e)
                    TOKEN = input("New token = ")
            df.update({user_id: response["id"]})

            with open(PATH_TO_FOLDERS_DATA, "w+") as file:
                json.dump(df, file, indent=4, ensure_ascii=False)

        folder_id = df[user_id]

        res = get_files_by_chat_id(HOST, PORT, user_id)

        for data in tqdm(res["result"]):
            index += 1

            text = data["text"]
            user_id = data["user_id"]
            time = data["timestamp"]["$date"]
            description = data["description"]
            decode_bytes = base64.b64decode(data["speech_bytes"])

            while True:
                try:
                    response = upload_file(TOKEN, decode_bytes, f"{index}.wav", folder_id)

                    if not response.get("error"):
                        break

                    print(response)
                    TOKEN = input("New token = ")
                except Exception as e:
                    print(e)
                    TOKEN = input("New token = ")

            users.update(
                {
                    index: {
                        "index": index,
                        "user_id": user_id,
                        "text": text,
                        "description": description,
                        "timestamp": time,
                    }
                }
            )

            with open(PATH_TO_USERS_DATA, "w+") as file:
                json.dump(users, file, indent=4, ensure_ascii=False)

    pd.read_json(PATH_TO_USERS_DATA).T.to_csv(PATH_TO_USERS_CSV, index=False)

    while True:
        try:
            response_users = upload_file(
                TOKEN, open(PATH_TO_USERS_CSV, "rb"), "update_users.csv", ROOT_FOLDER
            )
            response_folder = upload_file(
                TOKEN, open(PATH_TO_FOLDERS_DATA, "rb"), "update_folders-id.json", ROOT_FOLDER
            )

            if not response_users.get("error") and not response_folder.get("error"):
                break

            print(response_users)
            print(response_folder)
            TOKEN = input("New token = ")
        except Exception as e:
            print(e)
            TOKEN = input("New token = ")
