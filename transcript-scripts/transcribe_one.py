import sys
import os
import subprocess

from urllib.parse import urlparse
from google.cloud import storage

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

BUCKET_NAME = "audiofiles-storage"
AUDIO_FLAC_PATH = "audio-flac"
TRANSCRIPTION_JSON_PATH = "transcripts"


def main():

    audio_url = sys.argv[1]
    name = sys.argv[2]

    print(f"Path to resource:{audio_url}")
    print(f"Unique identifier:{name}")

    # 0. Check if file in bucket. If yes: return None
    transcribed_name = name + ".json"
    if file_is_in_bucket(
        client, transcribed_name, BUCKET_NAME, TRANSCRIPTION_JSON_PATH
    ):
        return

    # 1. Download and rename file. Maintain file ext.
    file_name = download(audio_url, name)

    # 2. Convert to mono, flac, creating new file.
    flac_file_name = convert_to_flac(file_name, name)

    # 3. Upload flac file to google bucket
    client = get_google_storage_client()
    upload_to_bucket(
        client,
        flac_file_name,
        bucket_name=BUCKET_NAME,
        destination_path=AUDIO_FLAC_PATH,
    )

    # 4. transcribe & check transcription is in bucket
    session = get_google_api_session()
    transcribe(session, name, BUCKET_NAME, TRANSCRIPTION_JSON_PATH, AUDIO_FLAC_PATH)


def file_is_in_bucket(
    client: storage.Client,
    file_name: str,
    bucket_name: str,
    path,
) -> bool:
    """Checks if a file with the name file_name is found in the bucket."""

    names = _get_blob_names(client, bucket_name, path)
    return file_name in names


def _get_blob_names(client: storage.Client, bucket_name: str, path: str) -> List[str]:
    """Get list of all filenames in the bucket."""

    blobs = client.list_blobs(bucket_name, path)
    # Each blob has an attribute 'name', which is the one we are after.
    return [blob.name for blob in blobs]


def download(url: str, name: str) -> str:
    """Download resource found at url to current directory.

    Name resource 'name.xyz', where xyz is file extension parsed from url."""

    file_ext = get_file_ext(url)
    file_name = name + file_ext
    download_process = subprocess.run(["curl", "-L", "-o", audio_fname, ep.mp3_url])

    return file_name


def get_file_ext(url: str) -> str:
    """Parse out the file extension from a url, indicating what the file type is of the linked data."""
    file_type = os.path.basename(urlparse(url).path)
    _, file_ext = os.path.splitext(file_type)
    return file_ext


def convert_to_flac(file_name: str, name:str) -> str:
    """Create new audio file by converting audio in file_name to flac and mono. Name new file name.flac"""

    conversion = subprocess.run(
        ["ffmpeg", "-y", "-i", audio_fname, "-ac", "1", converted_audio_fname]
    )
    return name + flac

def get_google_storage_client()
    """Get a google storage client."""
    return storage.Client()

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
    blob.upload_from_filename(file, target_file_path)
    print("File {} uploaded to {}.".format(file_path, destination_path))

def get_google_api_session()-> AuthorizedSession:
    """Create a session object with authorization to do API calls within the specified scope."""

    credentials = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return AuthorizedSession(credentials)

def transcribe(session: AuthorizedSession, name: str, bucket:str, destination_path: str, source_path: str):
    # 1 construct api call info
    audio_uri = "gs://" + bucket + "/" + source_path + "/" + name + ".flac"
    output_uri = "gs://" + bucket + "/" + destination_path + "/" + name + ".json"

    config = get_speach_to_text_config(audio_uri, output_uri)

    # 2. Post request, longrunning speech-to-text.
    token = start_transcription(session, config)

    # 3. Wait until transcription concluded
    wait_for_transcription(token)

def get_speach_to_text_config(audio_uri, output_uri):
    """Create config file for the v1p1beta1 longrunning speech to text google API."""

    config = {
        "config": {
            "language_code": "en-US",
            "encoding": "FLAC",
            "audio_channel_count": 1,
            "enable_automatic_punctuation": True,
            "enable_word_time_offsets": True,
        },
        "audio": {
            "uri": audio_uri
        },
        "outputConfig": {
            "gcsUri": output_uri
        },
    }

    return config


def start_transcription(session:AuthorizedSession, config: dict)-> str:
    """Start transcription of audio file. """
    resp = authed_session.post(
        "https://speech.googleapis.com/v1p1beta1/speech:longrunningrecognize",
        headers={
            "Content-Type": "application/json; charset=utf-8",
        },
        json=gcloud_config,
    )
    print(resp)

if __name__ == "__main__":
    main()