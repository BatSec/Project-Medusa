import vlc
import os
import config
import shutil
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
    global img
    global playimg
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
root.title("Medusa")
root.geometry("420x500")
playimg = PhotoImage(file="play.png")
forward = PhotoImage(file="forward.png")
back = PhotoImage(file="back.png")
img = Image.open("temp.jpg")
img = img.resize((300, 300), Image.ANTIALIAS)
img.save("temp.jpg")
img = ImageTk.PhotoImage(Image.open("temp.jpg"))
lpic = Label(root, image=img)
BtPlay = Button(root, border='0', image=playimg, command=lambda: play(config.i,config.sound_file))
BtNext = Button(root, border='0', image=forward, command=lambda: next(config.sound_file))
BtPrev = Button(root, border='0', image=back, command=lambda: prev(config.sound_file))
BtTrev = Button(root, text="Show PlayList", command= lambda: os.system('python3 treverse_songs.py'))
cname = Label(root, text=config.mname)
space = Label(root, text=' ')
space2 = Label(root, text=' ')
space3 = Label(root, text=' ')
lpic.grid(row=0, column=1)
space.grid(row=1)
cname.grid(row=2, column=1)
space2.grid(row=3)
BtPlay.grid(row=4, column=1)
BtNext.grid(row=4, column=2)
BtPrev.grid(row=4, column=0)
space3.grid(row=5)
BtTrev.grid(row=7, column=1)
root.mainloop()
