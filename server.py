"""Server for pod transcript app."""
from typing import Dict, List
from flask import (Flask, render_template, request, flash, session,
                   redirect)
import feedparser
from model import connect_to_db
import uuid

app = Flask(__name__)
app.secret_key = "dev"
#app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# -----------------------
# Using their REST API

# # Import libraries
# from google.cloud import speech_v1p1beta1 as speech

# #from mutagen.mp3 import MPEGInfo


# MP3_PATH = "~/audio_mp3/"     #Input audio file path
# TRANSCRIPT_PATH = "~/transcripts/" #Final transcript path
# BUCKET_NAME = "audiofiles-storage" #Name of the bucket created in the step before

# file_name = BUCKET_NAME + MP3_PATH
# LOCAL_FILEPATH = '/audio-files'
# local_file_name = LOCAL_FILEPATH + '/Art.mp3'

# def write_transcripts(transcript_filename,transcript):
#     f= open(TRANSCRIPT_PATH + transcript_filename,"w+")
#     f.write(transcript)
#     f.close()

# #def get_mp3_info(mp3_file):
#     """"""
#     #from pydub import AudioSegment
#     #from mutagen.mp3 import MP3
# #    return MPEGInfo(mp3_file).sample_rate

# def transcribe_file(gcs_uri):
#     """Transcribe the given mp3 audio file.
    
#     Performs asynchronous speech recognition on an audio file
    
#     Args:
#         storage_uri URI for audio file in Cloud Storage"""
#     from google.cloud import speech
#     import io
    
#     client = speech.SpeechClient()

#     audio = speech.RecognitionAudio(uri=gcs_uri)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.MP3,
#         language_code="en-US",
#         enable_word_time_offsets = True,
#     )

#     operation = client.long_running_recognize(config=config, audio=audio)

#     print("Waiting for operation to complete...")
#     result = operation.result(timeout=90)


#     # Each result is for a consecutive portion of the audio. Iterate through
#     # them to get the transcripts for the entire audio file.
#     for result in response.results:
#         alternative = result.alternatives[0]
#         # The first alternative is the most likely one for this portion.
#         print(f"Transcript: {alternative.transcript}")
#         print(f"Transcript: {alternative.confidence}")
#         #print(u"transcript: {}".format(result.alternatives[0].transcript))
    
#     #write_transcripts(TRANSCRIPT_PATH, response)

#         for word_info in alternative.words:
#             word = word_info.word
#             start_time = word_info.start_time
#             end_time = word_info.end_time

#             print(
#                 f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
#             )


# if __name__ == "__main__":
#     print(local_file_name)
#     test = get_mp3_info('audio-files/Art.mp3')
#     #transcribe_file()

