import os
from typing import List
from google.cloud import storage

BUCKET_NAME = "audiofiles-storage"
PREFIX = "transcripts"


def get_blob_names(client: storage.Client, bucket_name: str = BUCKET_NAME) -> List[str]:
    """Get list of all filenames in the bucket."""

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = client.list_blobs(bucket_name, prefix=PREFIX)
    # Each blob has an attribute 'name', which is the one we are after.
    return [blob.name for blob in blobs]


def file_is_in_bucket(client: storage.Client, file_name: str, bucket_name: str) -> bool:
    """Checks if a file with the name file_name is found in the bucket."""

    names = get_blob_names(client, bucket_name=bucket_name)
    return file_name in names


if __name__ == "__main__":
    client = storage.Client()

    # --------------------------------------------
    # Tests for checking if transcription exists in bucket cache
    test1 = get_blob_names(client, "audiofiles-storage")
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
