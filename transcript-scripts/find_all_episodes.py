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
        print(f"python3 transcribe_one.py '{ep.mp3_url}' '{model.cache_id(ep)}'")


if __name__ == "__main__":
    main()