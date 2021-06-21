import os
from typing import List
from google.cloud import storage
import requests

BUCKET_NAME = "audiofiles-storage"
AUDIO_FILE_PATH = "audiofiles-storage/audio-flac/"
PREFIX = "transcripts"


def file_is_in_bucket(
    client: storage.Client, file_name: str, bucket_name: str = BUCKET_NAME
) -> bool:
    """Checks if a file with the name file_name is found in the bucket."""

    names = _get_blob_names(client, bucket_name=bucket_name)
    return file_name in names


def _get_blob_names(client: storage.Client, bucket_name: str) -> List[str]:
    """Get list of all filenames in the bucket."""

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = client.list_blobs(bucket_name, prefix=PREFIX)
    # Each blob has an attribute 'name', which is the one we are after.
    return [blob.name for blob in blobs]


from google.cloud import storage


def upload_blob(
    source_file_name: str,
    bucket_name: str,
    target_file_path: str,
    client: storage.Client(),
):
    """Uploads a file to the bucket."""

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(target_file_path)
    # TODO fix timeout on upload!! Can I download directly to bucket? How to integrate with the rest of the transcription pipeline?
    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(source_file_name, target_file_path))


def transcribe_blob(
    gc_audio_path: str, gc_results_path: str, client: storage.Client()
) -> str:

    """Initiate transcription of audiofile at gc_audio_path. Saver results
    to gc_results_path."""

    gcloud_config = {
        "config": {
            "language_code": "en-US",
            "encoding": "FLAC",
            "audio_channel_count": 1,
            "enable_automatic_punctuation": True,
            "enable_word_time_offsets": True,
        },
        "audio": {"uri": gc_audio_path},
        "outputConfig": gc_results_path,
    }

    resp = requests.post(
        "https://speech.googleapis.com/v1/speech:longrunningrecognize",
        headers={
            "Content-Type": "application/json; charset=utf-8",
        },
        data=gcloud_config,
    )
    resp.json()  # {'name': 'gcloud operation name'}
    return resp.json()


def poll_transcription(gc_op_name: str):

    return requests.get("https://speech.googleapis.com/v1/operations/" + gc_op_name)


if __name__ == "__main__":
    client = storage.Client()

    # --------------------------------------------
    # Tests for checking if transcription exists in bucket cache
    test1 = _get_blob_names(client, "audiofiles-storage")
    test2 = file_is_in_bucket(
        client,
        file_name="YoIsThisRacist_sample.flac",
        bucket_name="audiofiles-storage",
    )
    test3 = file_is_in_bucket(
        client,
        file_name="transcripts/Yo_is_this_racist_sample.json",
        bucket_name="audiofiles-storage",
    )

    # test4 = upload_blob(
    #     "/Users/torasirkka/Documents/Hackbright2021/MyProject/podsearch/transcript-scripts/YoIsThisRacistCuriousGeorgeYOURdfee1f45663041c9a518ad42004f34de.flac",
    #     client,
    # )
