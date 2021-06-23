import sys

from sqlalchemy.orm import joinedload

sys.path.append(
    "/Users/torasirkka/Documents/Hackbright2021/MyProject/podsearch/backend"
)
import model
import server
from flask import jsonify
from google.cloud import storage
from typing import List
import json

model.connect_to_db(server.app)

BUCKET_NAME = "audiofiles-storage"
TRANSCRIPTION_JSON_PATH = "transcripts"


def main():
    # Find episodes that have no transcript
    episodes = (
        model.Episode.query.filter_by(transcript=None)
        .options(joinedload(model.Episode.podcast))
        .all()
    )

    # Loop through episodes and check if transcript exists in bucket.
    # If it does: download and commit it to database.
    client = storage.Client()
    existing_transcripts = get_blob_names(client, BUCKET_NAME, TRANSCRIPTION_JSON_PATH)

    for ep in episodes:
        transcribed_name = TRANSCRIPTION_JSON_PATH + "/" + model.cache_id(ep) + ".json"

        if transcribed_name in existing_transcripts:
            print(ep)
            transcript = download_transcript(
                client,
                transcribed_name,
                BUCKET_NAME,
            )
            print(transcript)
            ep.transcript = transcript
            model.db.session.add(ep)

    model.db.session.commit()


def get_blob_names(client: storage.Client, bucket_name: str, path: str) -> List[str]:
    """Get list of all filenames in the bucket."""
    blobs = client.list_blobs(bucket_name, prefix=path)
    # Each blob has an attribute 'name', which is the one we are after.
    return [blob.name for blob in blobs]


def download_transcript(
    client: storage.Client,
    file_path: str,
    bucket_name: str,
):
    """Download transcript json from cloud storage bucket."""

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)

    data = blob.download_as_text()
    return json.loads(data)


if __name__ == "__main__":
    main()
