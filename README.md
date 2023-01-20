# Backup-Google-Drive

This is a simple script to backup your Google Drive to your local machine. It uses the Google Drive API to download all files and folders from your Google Drive. It will create a folder structure on your local machine that mirrors your Google Drive. It will also create a log file that contains the file/folder name, the file/folder ID, and the file/folder size.

## Input your Google Drive credentials

You will need to create a Google API project and enable the Google Drive API. 
Algorithmia: 
* [Choose Google Drive API v3 and click Authorize APIs.](https://developers.google.com/oauthplayground/)
* Click Exchange authorization code for tokens.
* Copy the access token and paste it into the credentials.json file.

## Requirements

```bash
pip install -r requirements.txt
```

## Run

```bash
python src/run-backup-process.py 
```