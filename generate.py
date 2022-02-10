import os
import random
from string import punctuation
import sys
import getopt
argv = sys.argv[1:]
# Before the adventure across the country, we cried but nowhere nearly as long as fox
opt, text = getopt.getopt(argv, 'text:', ['text'])

filelist = []
filelist.append("sox")
for word in text:
    folder = f"./words/{word.strip().lower().translate(str.maketrans('','',punctuation))}"
    if os.path.exists(folder):
        try:
            files = os.listdir(folder)
            if len(files) > 0:
                file = random.choice(files)
            else:
                file = files
            filelist.append(os.path.join(folder,file))
        except:
            print(f"{word} - exception")
    else:
        print(f"Word : {word} not found")
    
    # insert breath
    files = os.listdir("./pauses")

    #filelist.append(f"./pauses/{random.choice(files)}")
    filelist.append(f"./pauses/0.11.wav")

filelist.append("output.wav")
print (*filelist)