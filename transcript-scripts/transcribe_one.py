import sys

BUCKET_NAME = "audiofiles-storage"
AUDIO_FLAC_PATH = "audio-flac"
TRANSCRIPTION_JSON_PATH = "transcripts"


def main():

    audio_url = sys.argv[1]
    name = sys.argv[2]

    print(audio_url, name)

    # 1. Download and rename file. Maintain file ext.
    file_name = download(audio_url, name)

    # 2. Convert to mono, flac, creating new file.
    flac_file_name = convert_to_flac(file_name)

    # 3.
    client = get_google_storage_client()
    upload_to_bucket(
        client,
        flac_file_name,
        bucket_name=BUCKET_NAME,
        destination_path=AUDIO_FLAC_PATH,
    )

    # 4. transcribe
    session = get_google_api_session()
    transcribe(session, name, BUCKET_NAME, TRANSCRIPTION_JSON_PATH, AUDIO_FLAC_PATH)


def transcribe(session, name, bucket, destination_path, source_path):
    # 1 construct api call info
    audio_uri = "gs://" + bucket + "/" + source_path + "/" + name + ".flac"
    output_uri = "gs://" + bucket + "/" + destination_path + "/" + name + ".json"

    config = get_speach_to_text_config(audio_uri, output_uri)

    # 2. Post request, longrunning speech-to-text.
    token = start_transcription(session, config)

    # 3. Wait until transcription concluded
    wait_for_transcription(token)


def download(url: str, name: str) -> None:
    pass
    # 2.


if __name__ == "__main__":
    main()