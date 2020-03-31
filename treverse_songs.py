import os
from tinytag import TinyTag, TinyTagException

tracks = []

for root, dirs, files, in os.walk("/home/lowkey/Documents/Programs/Python/Project Medusa/Music"):
    for name in files:
        if name.endswith((".mp3",".m4a",".flac",".alac")):
            tracks.append(name)
            try:
                temp_track = TinyTag.get(root + "/" + name) #change to \ for windows
                print(temp_track.title, "-", temp_track.artist)
            except TinyTagException:
                print("Error")
