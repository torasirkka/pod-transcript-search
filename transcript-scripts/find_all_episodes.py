import sys

sys.path.append(
    "/Users/torasirkka/Documents/Hackbright2021/MyProject/podsearch/backend"
)
import model
import server

model.connect_to_db(server.app)

# Find episodes that have no transcript
episodes = model.Episode.query.filter_by(transcript=None).all()

# Loop through episodes and print out cmd line
# commands that match input of transcribe_one.

for ep in episodes:
    print(f"python3 transcribe_one.py {ep.mp3_url} {ep.fname}")
