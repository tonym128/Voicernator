import wave
import json
import uuid
import os
from pydantic import DurationError

from vosk import Model, KaldiRecognizer, SetLogLevel
import Word as custom_Word

model_path = "models/vosk-model-en-us-0.22"
audio_filename = "chapter1.wav"

model = Model(model_path)
wf = wave.open(audio_filename, "rb")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

# get the list of JSON dictionaries
results = []
# recognize speech using vosk model
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)
part_result = json.loads(rec.FinalResult())
results.append(part_result)

# convert list of JSON dictionaries to list of 'Word' objects
list_of_words = []
for sentence in results:
    if len(sentence) == 1:
        # sometimes there are bugs in recognition 
        # and it returns an empty dictionary
        # {'text': ''}
        continue
    for obj in sentence['result']:
        w = custom_Word.Word(obj)  # create custom Word object
        list_of_words.append(w)  # and add it to list

wf.close()  # close audiofile

# output to the screen
with open('words.sh','w') as f:
    for word in list_of_words:
        if word.conf == 1:
            if not os.path.exists(f"./words"):
                os.makedirs(f"./words")

            if not os.path.exists(f"./words/{word.word}"):
                os.makedirs(f"./words/{word.word}")
            guid = str(uuid.uuid4())
            command = f"ffmpeg -i {audio_filename} -ss {word.start} -t {word.duration()} .//words//{word.word}//{guid}.wav\n"
            print(f"{word.word}, {word.start}, {word.duration()}")
            f.write(command)

with open('pauses.sh','w') as f:
    start = list_of_words[0].end + 0.1
    end = 0.1
    for word in list_of_words[1:]:
        if not os.path.exists(f"./pauses"):
            os.makedirs(f"./pauses")
        end = word.start - 0.1
        duration = round(end - start,3)
        if duration > 0:
            command = f"ffmpeg -i {audio_filename} -ss {start} -t {duration} .//pauses//{duration}.wav\n"
            f.write(command)

        start = word.end
