import sys

sys.path.append(
    "/Users/torasirkka/Documents/Hackbright2021/MyProject/pod-transcript-search/backend"
)
import model
import server
from google.cloud import storage
from typing import List, Dict
import json
from sqlalchemy.orm import joinedload


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
            transcript_dict = download_transcript(
                client,
                transcribed_name,
                BUCKET_NAME,
            )

            transcript = extract_transcript(transcript_dict)

            ep.transcript = transcript
            ep.searchepisode[0].transcript = transcript

            model.db.session.add(ep)
            model.db.session.add(ep.searchepisode[0])
            print(
                f"Added transcript to episode {ep.episode_title} and searchepisode {ep.searchepisode[0].searchepisodes_id}"
            )
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


def extract_transcript(transcript: Dict) -> str:
    """Extract the transcript from the response returned by Google speech API."""

    # Each audio file is broken into snippets whose consecutive transcriptsare stored
    # in a list under the key "results". Each snippet is a dict containing meta data
    # and words offset data in addition to the transcript under the key "transcript".
    # Loop through the list of snippetsto extract and combine the transcripts to one
    # text.
    print("Number of snippets: ", len(transcript["results"]))
    snippets = []
    for snippet in transcript["results"]:
        snippets.append(snippet["alternatives"][0]["transcript"])
    return "".join(snippets)


if __name__ == "__main__":
    model.connect_to_db(server.app)
    main()