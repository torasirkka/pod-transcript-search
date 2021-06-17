import os
from typing import List
from google.cloud import storage

BUCKET_NAME = "audiofiles-storage"
PREFIX = "transcripts"


def get_cached_files(bucket_name: str = BUCKET_NAME) -> List[str]:
    """Get list of all filenames in the bucket."""

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=PREFIX)
    # Each blob has an attribute 'name', which is the one we are after.
    return [blob.name for blob in blobs]


def transcription_is_in_bucket(cache_file_name: str, bucket_name: str) -> bool:
    """Checks if a file with the name cache_file_name is found in the bucket."""

    names = get_cached_files(bucket_name=bucket_name)
    return cache_file_name in names


if __name__ == "__main__":

    # --------------------------------------------
    # Tests for checking if transcription exists in bucket cache
    test1 = get_cached_files("audiofiles-storage")
    test2 = transcription_is_in_bucket(
        cache_file_name="YoIsThisRacist_sample.flac",
        bucket_name="audiofiles-storage",
    )
    test3 = transcription_is_in_bucket(
        cache_file_name="transcripts/Yo_is_this_racist_sample.json",
        bucket_name="audiofiles-storage",
    )
