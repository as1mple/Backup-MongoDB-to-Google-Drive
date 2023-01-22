# Backup-MongoDB-to-Google-Drive

This is a simple script to backup your MongoDB database to Google Drive.
Update the script with your database name and Google Drive root folder ID, access token and users id.

## Input your Google Drive credentials

You will need to create a Google API project and enable the Google Drive API. 
Algorithmia: 
* [Choose Google Drive API v3 and click Authorize APIs.](https://developers.google.com/oauthplayground/)
* Click Exchange authorization code for tokens.
* Copy the access token and paste it into the credentials.json file.

## Requirements

## Using bash-script

> Create virtual environment
```bash
python3 -m venv venv
```
- - - -

> Activate virtual environment
```bash
source venv/bin/activate
```

- - - -
> Install requirements
```bash
pip install -r requirements.txt
```

- - - - 
> Make bash-file executable
```bash
chmod +x run-backup-process.sh
```

- - - -
> Run script
```bash
./run-backup-process.sh
```