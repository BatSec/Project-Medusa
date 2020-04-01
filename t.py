import vlc
import os
import config
import shutil
import tkinter.font as font
from tkinter import *
from tinytag import TinyTag, TinyTagException
from PIL import Image, ImageTk

config.i = 0
config.mname = ''
config.song = []
config.goto = 0
config.tmp = 0
config.playing = 0
config.path = "/home/lowkey/Music/"


for root, dirs, files, in os.walk(config.path):
    for name in files:
            config.song.append(name)


def main():
    try:
        config.csong = config.song[config.tmp]
    except IndexError:
        print("No songs Found!!")
        exit()
    config.sound_file = vlc.MediaPlayer(config.path + config.csong)
    temp_track = TinyTag.get(config.path + config.csong, image=True)
    title = temp_track.title
    if title is None:
        title = config.song[config.tmp]
    elif len(title) > 20:
        title = title[:20] + "..."
    print("Now Playing:", title)
    pic = temp_track.get_image()
    if pic is not None:
        f1 = open("temp.jpg", "wb")
        f1.write(pic)
    else:
        shutil.copy("default.jpg", "temp.jpg")
    config.mname = title


def play(check, sound_file):
    if config.i == 0:
        sound_file.play()
        config.i = 1
        config.playing = 1
    else:
        sound_file.pause()
        config.i = 0
        print("Paused")
        config.playing = 0
    refresh(0)


def next(sound_file):
    config.tmp += 1
    config.goto = 0
    main()
    if config.playing == 1:
        sound_file.pause()
        config.i = 0
    refresh(1)


def prev(sound_file):
    if config.tmp != 0:
        config.tmp -= 1
        config.goto = 0
        main()
        if config.playing == 1:
            sound_file.pause()
            config.i = 0
        refresh(1)


def refresh(var):
    global img, playimg
    img = Image.open("temp.jpg")
    img = img.resize((300, 300), Image.ANTIALIAS)
    img.save("temp.jpg")
    img = ImageTk.PhotoImage(Image.open("temp.jpg"))
    lpic.config(image=img)
    cname.config(text=config.mname)
    if var == 1:
        playimg = PhotoImage(file="play.png")
        BtPlay.config(image=playimg)
    elif config.playing == 1:
        playimg = PhotoImage(file="pause.png")
        BtPlay.config(image=playimg)
    else:
        playimg = PhotoImage(file="play.png")
        BtPlay.config(image=playimg)


main()
config.goto = 1
root = Tk()
myFont = font.Font(size=16)
root.title("Medusa")
root.geometry("420x500")
icon = PhotoImage(file = 'icon.png') 
root.iconphoto(False, icon)
playimg = PhotoImage(file="play.png")
forward = PhotoImage(file="forward.png")
back = PhotoImage(file="back.png")
search = PhotoImage(file="search.png")
ref = PhotoImage(file="refresh.png")
img = Image.open("temp.jpg")
img = img.resize((300, 300), Image.ANTIALIAS)
img.save("temp.jpg")
img = ImageTk.PhotoImage(Image.open("temp.jpg"))
lpic = Label(root, image=img)
BtPlay = Button(root, border='0', image=playimg, command=lambda: play(config.i,config.sound_file))
BtNext = Button(root, border='0', image=forward, command=lambda: next(config.sound_file))
BtPrev = Button(root, border='0', image=back, command=lambda: prev(config.sound_file))
BtTrev = Button(root, border='0', image=search ,command= lambda: os.system('python3 treverse_songs.py'))
BtRef = Button(root, border='0', image=ref)
cname = Label(root, text=config.mname, font=myFont)
# MyButton1.place(relx=0.5, rely=0.5, anchor="c")
lpic.place(relx=0.5, rely=0.0, anchor="n")
cname.place(relx=0.5, rely=0.75, anchor="c")
BtPlay.place(relx=0.5, rely=0.85, anchor="c")
BtPrev.place(relx=0.25, rely=0.85, anchor="c")
BtNext.place(relx=0.75, rely=0.85, anchor="c")
BtTrev.place(relx=0.1, rely=0.85, anchor="c")
BtRef.place(relx=0.9, rely=0.85, anchor="c")
root.mainloop()
