import sys
import os
import subprocess

from urllib.parse import urlparse
from google.cloud import storage

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

sys.path.append(
    "/Users/torasirkka/Documents/Hackbright2021/MyProject/podsearch/backend"
)

import time
from typing import List

BUCKET_NAME = "audiofiles-storage"
AUDIO_FLAC_PATH = "audio-flac"
TRANSCRIPTION_JSON_PATH = "transcripts"
USER_PROJECT = "brilliant-flame-314106"


def main():

    client = storage.Client()

    audio_url = sys.argv[1]
    name = sys.argv[2]

    print(f"Path to resource: {audio_url}")
    print(f"Unique identifier: {name}")

    # preparation: creating filenames needed:
    transcribed_name = TRANSCRIPTION_JSON_PATH + "/" + name + ".json"
    flac_bucket_path = AUDIO_FLAC_PATH + "/" + name + ".flac"

    # 0. Check if file in bucket. If yes: return None
    client = storage.Client()

    if file_is_in_bucket(
        client, transcribed_name, BUCKET_NAME, TRANSCRIPTION_JSON_PATH
    ):
        print(
            f"Transcribed audio '{transcribed_name}' already exists in bucket '{BUCKET_NAME}'."
        )
        return

    # 1. If flac audio-file not in bucket:
    #    Download and rename file. Maintain file ext.
    if not file_is_in_bucket(client, flac_bucket_path, BUCKET_NAME, AUDIO_FLAC_PATH):
        file_name = download(audio_url, name)

        # a. Convert to mono, flac, creating new file.
        flac_file_name = convert_to_flac(file_name, name)

        # b. Upload flac audio file to bucket
        upload_to_bucket(
            client,
            flac_file_name,
            bucket_name=BUCKET_NAME,
            destination_path=flac_bucket_path,
        )

    # 2. transcribe & check transcription is in bucket
    session = get_google_api_session()
    transcribe(session, name, BUCKET_NAME, TRANSCRIPTION_JSON_PATH, AUDIO_FLAC_PATH)


def file_is_in_bucket(
    client: storage.Client,
    file_name: str,
    bucket_name: str,
    path,
) -> bool:
    """Checks if a file with the name file_name is found in the bucket."""

    names = get_blob_names(client, bucket_name, path)
    return file_name in names


def get_blob_names(client: storage.Client, bucket_name: str, path: str) -> List[str]:
    """Get list of all filenames in the bucket."""
    blobs = client.list_blobs(bucket_name, prefix=path)
    # Each blob has an attribute 'name', which is the one we are after.
    return [blob.name for blob in blobs]


def download(url: str, name: str) -> str:
    """Download resource found at url to current directory.

    Name resource 'name.xyz', where xyz is file extension parsed from url."""

    file_ext = get_file_ext(url)
    file_name = name + file_ext
    subprocess.run(["curl", "-L", "-o", file_name, url])

    return file_name


def get_file_ext(url: str) -> str:
    """Parse out the file extension from a url, indicating what the file type is of the linked data."""
    file_type = os.path.basename(urlparse(url).path)
    _, file_ext = os.path.splitext(file_type)
    return file_ext


def convert_to_flac(file_name: str, name: str) -> str:
    """Create new audio file by converting audio in file_name to flac and mono. Name new file name.flac"""

    converted_audio_fname = name + ".flac"
    subprocess.run(["ffmpeg", "-y", "-i", file_name, "-ac", "1", converted_audio_fname])
    return converted_audio_fname


def upload_to_bucket(
    client: storage.Client,
    file_path: str,
    bucket_name: str,
    destination_path: str,
):
    """Upload file to google cloud storage bucket."""

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_path)

    print("Uploading...")
    # TODO fix timeout on upload!!
    blob.upload_from_filename(file_path)
    print("File {} uploaded to {}.".format(file_path, destination_path))


def get_google_api_session() -> AuthorizedSession:
    """Create a session object with authorization to do API calls within the specified scope."""

    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return AuthorizedSession(credentials)


def transcribe(
    session: AuthorizedSession,
    name: str,
    bucket: str,
    destination_path: str,
    source_path: str,
):
    # 1 construct api call info
    audio_uri = "gs://" + bucket + "/" + source_path + "/" + name + ".flac"
    output_uri = "gs://" + bucket + "/" + destination_path + "/" + name + ".json"

    config = get_speach_to_text_config(audio_uri, output_uri)

    # 2. Post request, longrunning speech-to-text.
    start_transcription(session, config)
    print("Transcribing...")


def get_speach_to_text_config(audio_uri, output_uri):
    """Create config file for the v1p1beta1 longrunning speech to text google API."""

    config = {
        "config": {
            "language_code": "en-US",
            "encoding": "FLAC",
            "audio_channel_count": 1,
            "enable_word_time_offsets": True,
        },
        "audio": {"uri": audio_uri},
        "outputConfig": {"gcsUri": output_uri},
    }

    return config


def start_transcription(session: AuthorizedSession, config: dict):
    """Start transcription of audio file. """
    resp = session.post(
        "https://speech.googleapis.com/v1p1beta1/speech:longrunningrecognize",
        headers={
            "Content-Type": "application/json; charset=utf-8",
        },
        json=config,
    )
    print(resp)


if __name__ == "__main__":
    main()

# to test: run python3 -i transcribe_one.py "https://cdn.simplecast.com/audio/5c3025/5c302538-714d-4d5d-be74-21d38440ae5c/d915ceb2-0367-4e8c-b2aa-a66944ba4b67/smartless-trailer2-v8a-2-rmix03_tc.mp3?aid=rss_feed&feed=pvzhyDQn" "SmartLessTrailer2SurpriseG94c0d3e3d8004be9acee8b411999dc43"
# python3 -i transcribe_one.py "https://cdn.simplecast.com/audio/5c3025/5c302538-714d-4d5d-be74-21d38440ae5c/8d7a257c-8a00-41e2-9e1d-a5ca3bae1e5f/smartless-trailer-a1sauce-comp_tc.mp3?aid=rss_feed&feed=pvzhyDQn" "SmartLessTrailer1LaunchTra246f9cf6438442a5af4ac7a11f006821"
# transcribe(session, 'YoIsThisRacist_sample', BUCKET_NAME,TRANSCRIPTION_JSON_PATH,AUDIO_FLAC_PATH)