# pod_transcript_search
Welcome to the pod transcript search webb app! Podsearch allows you to search the content of podcasts. 

In this 2.5min video I introduce the app and talk about how I solved some key challenges:
https://youtu.be/hsC5ueL7obs

## Tech stack used:

Python, Bash, Flask + SQLAlchemy, PostgreSQL, React.

I transcribe the episodes using Google Cloud's Speech-to-Text service and implement a search function on top of the full text search offered by PostgreSQL. 

My front end is a React app and my Flask backend exposes a REST API. I parse podcast RSS feeds in one of my API endpoints, and add them to my database. To transcribe the podcasts I built a batch processing pipeline. This pipeline uses subprocesses to run curl and ffmpeg  to download, downmix and convert format of the audio. It then uses a Google service account to upload the audio file to a GCS bucket, initiate its transcription and download the resulting transcript.

## How to install for local development:
Checkout program:
```
git clone git@github.com:torasirkka/pod-transcript-search.git
```
## Install requirements
You need Python3 and pip3 for this project. You also need the libraries and frameworks listed in requirements.txt. 
```
cd pod-transcript-search
pip3 install requirements.txt
createdb podcasts
python3 server.py
```
