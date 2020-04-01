import os
from tkinter import *
from tinytag import TinyTag, TinyTagException

tracks = []
tmp = 1

for root, dirs, files, in os.walk("/home/lowkey/Music"):
    for name in files:
        if name.endswith((".mp3",".m4a",".flac",".alac")):
            try:
                temp_track = TinyTag.get(root + "/" + name) #change to \ for windows
                tracks.append(temp_track.title)
            except TinyTagException:
                tracks.append(name)

root = Tk()
songlist = Listbox(root)
root.geometry("300x500")

for i in tracks:
    if len(i) > 20:
        i = i[:20] + "..."
    songlist.insert(tmp, "  "+i)
    tmp += 1

songlist.place(relx=0.5, rely=0.5, anchor="c", height="500", width="300")
root.mainloop()
