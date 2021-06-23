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


def test():
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

            # string to be assigned
            transcript = extract_transcript(transcript_dict)

            # ep is the object (row in the episodes table)
            # ep has an attribute transcript that I assign to 'transcript'
            ep.transcript = transcript
            print(ep.transcript[:50])
            print("-" * 30)
            # Next I check the searchepisode object that I access through its relation to ep.
            # searchepisode has an attribute transript that I want to assign a value to.
            print(ep.searchepisode[0])
            # First, I print the current value
            print(ep.searchepisode[0].transcript)
            # Then I assign a value to it
            ep.searchepisode[0].transcipt = transcript
            # Finally I print to confirm the update.
            print(ep.searchepisode[0].transcript)
            print("*" * 30)
            print("")

            # To troubleshoot I try updating the attribute description on the searchepisode object.
            print(ep.searchepisode[0].description)
            ep.searchepisode[0].decsription = transcript
            print("After re-assignment")
            print(ep.searchepisode[0].description)

            return transcript

            model.db.session.add(ep)

            model.db.session.commit()
            # Each result is for a consecutive portion of the audio. Iterate through
            # them to get the transcripts for the entire audio file.
            # for result in transcript["results"]:
            # The first alternative is the most likely one for this portion.
            #   print(u"Transcript: {}".format(result.alternatives[0].transcript))

            # p.transcript = transcript
            # print(ep.episode_id)
            # return ep


def extract_transcript(transcript: Dict) -> str:
    """Extract the transcript from the response returned by Google speech API."""

    # Each audio file is broken into snippets transcribed and stored separately.
    # In addition to the transcript each snippet is a list of dicts containing
    # meta data and words offset data.
    # Loop through transcription file to extract and combine transcript one text.
    print("Number of snippets: ", len(transcript["results"]))
    snippets = []
    for snippet in transcript["results"]:
        snippets.append(snippet["alternatives"][0]["transcript"])
    return "".join(snippets)


if __name__ == "__main__":
    model.connect_to_db(server.app)
    # main()
    test()
