import sys
import re

sys.path.append(
    "/Users/torasirkka/Documents/Hackbright2021/MyProject/podsearch/backend"
)
import model
import server

model.connect_to_db(server.app)


def main():
    # Find episodes that have no transcript
    episodes = model.Episode.query.filter_by(transcript=None).all()

    # Loop through episodes and print out cmd line
    # commands that match input of transcribe_one.

    print("#!/bin/bash")
    for ep in episodes:
        print(f"python3 transcribe_one.py '{ep.mp3_url}' '{fname(ep)}'")


def fname(ep: model.Episode) -> str:
    """Hash fn that generates a unique fname for a podcast episode.

    This is the filename for the transcriptions cache stored used as back-up.
    It consists of the first 15 chars of the podcast and episode titles + the
    32 last episode uuid chars.
    """

    # TODO: check out https://docs.python.org/3/library/functools.html#functools.cached_property

    # WARNING: LEGAL_FILENAME_CHARS is used in hash fn to generate unique ids. DO NOT ALTER! May cause
    # transcription of files already transcribed!
    LEGAL_FILENAME_CHARS = r"[a-zA-Z0-9]"

    def only_legal_chars(s: str) -> str:
        return "".join([char for char in s if re.match(LEGAL_FILENAME_CHARS, char)])

    pod_title = only_legal_chars(ep.podcast.title)
    ep_title = only_legal_chars(ep.episode_title)
    ep_guid = only_legal_chars(ep.guid)

    return pod_title[:17] + ep_title[:17] + ep_guid[-32:]


if __name__ == "__main__":
    main()