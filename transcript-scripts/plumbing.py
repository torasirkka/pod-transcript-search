# Input: episode. Output: transcript
# getting example episode to work with:
import sys
import subprocess

sys.path.append(
    "/Users/torasirkka/Documents/Hackbright2021/MyProject/podsearch/backend"
)
import model
import server
from urllib.parse import urlparse
import os
from typing import List
from google.cloud import storage
import google_requests

model.connect_to_db(server.app)
STATUS = [None, "in progress", "done", "error"]


def initiate_episode_transcription() -> model.Episode:
    """"""
    episodes = episodes_without_transcript()
    chosen_ep = episodes[0]
    # updating but not yet committing status
    chosen_ep.status = STATUS[1]
    # checking if transcript exists in google bucket
    fname = chosen_ep.fname
    if google_requests.file_is_in_bucket(client=client, file_name=fname):
        # TODO add fn that downloads, adds and commits transcript to db
        pass
    else:
        transcribe_episode(chosen_ep)

    # model.db.session.add(chosen_ep)
    # model.db.session.commit()
    return chosen_ep


def episodes_without_transcript() -> List[model.Episode]:
    """List episodes that do not have a transcription."""

    return model.Episode.query.filter_by(status=None).all()


def transcribe_episode(ep: model.Episode):
    """Pre-process sound. If successful preprocess: transcribe episode. Set and commit status of episode."""
    audio_download_and_processing(ep)
    print(ep.status)
    if ep.status == STATUS[3]:
        # if audiodownload and conversion not successful: interrupt the transcription process
        print("woops")

    pass


def audio_download_and_processing(ep: model.Episode):
    """Download audio, convert to flac mono, return name of and path to audio."""

    # Download audio from url and store as temporary audio-file with name audio_fname
    audio_fname = ep.fname + get_file_ext(ep.mp3_url)
    download_process = subprocess.run(["curl", "-L", "-o", audio_fname, ep.mp3_url])
    if download_process.returncode != 0:
        ep.status = STATUS[3]

    # Convert audio to mono and flac.
    converted_audio_fname = ep.fname + ".flac"
    conversion = subprocess.run(
        ["ffmpeg", "-y", "-i", audio_fname, "-ac", "1", converted_audio_fname]
    )
    if conversion.returncode != 0:
        ep.status = STATUS[3]


def get_file_ext(url: str) -> str:
    """Parse out the file extension from a url, indicating what the file type is of the linked data."""
    file_type = os.path.basename(urlparse(url).path)
    _, file_ext = os.path.splitext(file_type)
    return file_ext


def delete_audio_files():
    """Remove audiofiles from current folder"""


url = "https://chrt.fm/track/FE12B2/traffic.omny.fm/d/clips/89050f29-3cfb-4513-a5d2-ac79004bd7ba/55c64838-70c7-4576-b4e4-ac800012ec27/dfee1f45-6630-41c9-a518-ad42004f34de/audio.mp3?utm_source=Podcast&in_playlist=05855b96-adce-4eaa-9d54-ac8300634c3"

x = urlparse(url)
y = os.path.basename(x.path)
print(os.path.splitext(y))
print(y)


if __name__ == "__main__":
    client = storage.Client()
    # eps = episodes_without_transcript()
    initiate_episode_transcription()
    # print(audio_download_and_processing(url))
    # subprocess.run(["curl", "-L", "-o", "test.mp3", url])
