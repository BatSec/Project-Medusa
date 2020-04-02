import vlc
import os
import config
import shutil
import time
import tkinter.font as font
from tkinter import *
import tkinter.ttk as ttk
from tinytag import TinyTag, TinyTagException
from PIL import Image, ImageTk

config.i = 0
config.mname = ''
config.song = []
config.slen = 0
config.tmp = 0
config.playing = 0
config.path = "/home/lowkey/Music/"
config.isload = 0
config.loadval = 0


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
    if temp_track.duration is not None:
        config.slen = int(temp_track.duration)
    else:
        config.slen = 0
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
        config.sound_file.play()
        config.i = 1
        config.playing = 1
        config.isload = 0
        val = config.slen*1000
        BtPlay.after(val, songEnd)
    else:
        config.sound_file.pause()
        config.i = 0
        print("Paused")
        config.playing = 0
        config.isload = 1
    refresh(0)
    loading()


def next(sound_file):
    config.tmp += 1
    main()
    if config.playing == 1:
        sound_file.pause()
        config.i = 0
    refresh(1)
    config.loadval = 0
    config.isload = 2
    loading()


def prev(sound_file):
    if config.tmp != 0:
        config.tmp -= 1
        main()
        if config.playing == 1:
            sound_file.pause()
            config.i = 0
        refresh(1)
        config.loadval = 0
        config.isload = 2
        loading()


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


def songEnd():
    config.isload = 3
    loading()


def loading():
    if config.isload == 0:
        i = 0
        for i in range(0, config.slen):
            progress.config(value = config.loadval)
            progress.start()
    elif config.isload == 2:
        progress.stop()
        progress.config(value=0)
    elif config.isload == 3:
        progress.stop()
        progress.config(value = (config.slen*20))
    else:
        config.loadval = progress["value"]
        progress.stop()
        progress.config(value=config.loadval)


def uplist(tmp):
    config.isload = 2
    config.loadval = 0
    loading()
    global index, value
    index = config.kaja.curselection()
    value = config.kaja.get(index)
    config.tmp = index[0]
    main()
    config.i = 0
    play(0, config.sound_file)
    config.root1.destroy()
    BtPlay.config(state="normal")


def list():
    BtPlay.config(state="disabled")
    if config.playing == 1:
        config.sound_file.pause()
        refresh(1)
    config.playing = 0
    tmp = 1
    config.root1 = Tk()
    myFont = font.Font(size=16)
    config.kaja = Listbox(config.root1, font=myFont)
    config.root1.geometry("300x500")

    for i in config.song:
        if len(i) > 30:
            i = i[:20] + "..."
        config.kaja.insert(tmp, "  "+i)
        tmp += 1

    config.kaja.place(relx=0.5, rely=0.5, anchor="c", height="500", width="300")
    config.kaja.bind('<<ListboxSelect>>', uplist)
    config.root1.mainloop()


def again():
    config.sound_file.stop()
    config.sound_file.play()
    config.playing = 1
    refresh(0)
    config.isloading = 2
    loading()


main()
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
s = ttk.Style()
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
progress = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient = HORIZONTAL, length = 400, maximum = (config.slen*20), mode = 'determinate', value=0)
BtPlay = Button(root, border='0', image=playimg, command=lambda: play(config.i,config.sound_file))
BtNext = Button(root, border='0', image=forward, command=lambda: next(config.sound_file))
BtPrev = Button(root, border='0', image=back, command=lambda: prev(config.sound_file))
BtTrev = Button(root, border='0', image=search ,command= lambda: list())
BtRef = Button(root, border='0', image=ref, command= lambda: again())
cname = Label(root, text=config.mname, font=myFont)
lpic.place(relx=0.5, rely=0.0, anchor="n")
cname.place(relx=0.5, rely=0.65, anchor="c")
BtPlay.place(relx=0.5, rely=0.85, anchor="c")
BtPrev.place(relx=0.25, rely=0.85, anchor="c")
BtNext.place(relx=0.75, rely=0.85, anchor="c")
BtTrev.place(relx=0.1, rely=0.85, anchor="c")
BtRef.place(relx=0.9, rely=0.85, anchor="c")
progress.place(relx=0.5, rely=0.725, anchor="c", height=7)
root.mainloop()
