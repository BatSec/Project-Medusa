import vlc
import os
import config
import shutil
from tkinter import PhotoImage, Listbox, Button, Tk, Label, Entry
import tkinter.ttk as ttk
import tkinter.font as font
from tinytag import TinyTag
from PIL import Image, ImageTk

# os.environ["VLC_PLUGIN_PATH"] = "plugins/"
# os.chdir(sys._MEIPASS)

config.i = 0
config.songName = ''
config.song = []
config.songLength = 0
config.tmp = 0
config.playing = 0
with open('.cache/defaultPath.txt', 'r+') as defaultPath:
    config.path = defaultPath.readline()
    if not config.path:
        def closeWindow():
            config.path = getPath.get()
            defaultPath.write(config.path)
            defaultPath.close()
            root.destroy()
        root = Tk()
        root.title("Medusa")
        root.geometry("300x150")
        label1 = Label(root, text = "Enter the path to your Music directory:")
        label1.pack(anchor = 'center')
        label2 = Label(root, text = "( eg: /home/username/Music/)")
        label2.pack(anchor = 'center')
        getPath = Entry(root)
        getPath.pack(anchor = 'center')
        Submit = Button(root, text = "OK", command = closeWindow)
        Submit.pack(anchor = 's')
        root.mainloop()
config.isload = 0
config.loadval = 0


for root, dirs, files, in os.walk(config.path):
    for name in files:
        if name.endswith(".mp3"):
            config.song.append(name)


def main():
    try:
        config.csong = config.song[config.tmp]
    except IndexError:
        print("No songs Found!!")
        open('.cache/defaultPath.txt', 'w').close()
        root = Tk()
        root.title("Medusa")
        root.geometry("300x150")
        label1 = Label(root, text = "No songs Found!!")
        label1.pack(anchor = 'center')
        label2 = Label(root, text = "Restart the software and Enter a valid path")
        label2.pack(anchor = 'center')
        button = Button(root, text = "Ok", command = exit)
        button.pack(anchor = 'center')
        root.mainloop()
        exit()
    config.sound_file = vlc.MediaPlayer(config.path + config.csong)
    temp_track = TinyTag.get(config.path + config.csong, image=True)
    if temp_track.duration is not None:
        config.songLength = int(temp_track.duration)
    else:
        config.songLength = 0
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
        shutil.copy("assets/default.jpg", "temp.jpg")
    config.songName = title


def play(check, sound_file):
    if config.i == 0:
        config.sound_file.play()
        config.i = 1
        config.playing = 1
        config.isload = 0
        val = config.songLength*1000
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
    play(0, config.sound_file)
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
        play(0, config.sound_file)
        loading()


def refresh(var):
    global img, playimg
    img = Image.open("temp.jpg")
    img = img.resize((300, 300), Image.ANTIALIAS)
    img.save("temp.jpg")
    img = ImageTk.PhotoImage(Image.open("temp.jpg"))
    lpic.config(image=img)
    cname.config(text=config.songName)
    if var == 1:
        playimg = PhotoImage(file="assets/play.png")
        BtPlay.config(image=playimg)
    elif config.playing == 1:
        playimg = PhotoImage(file="assets/pause.png")
        BtPlay.config(image=playimg)
    else:
        playimg = PhotoImage(file="assets/play.png")
        BtPlay.config(image=playimg)


def songEnd():
    config.isload = 3
    loading()


def loading():
    if config.isload == 0:
        for i in range(0, config.songLength):
            progress.config(value=config.loadval)
            progress.start()
    elif config.isload == 2:
        progress.stop()
        progress.config(value=0)
    elif config.isload == 3:
        progress.stop()
        progress.config(value=(config.songLength*20))
    else:
        config.loadval = progress["value"]
        progress.stop()
        progress.config(value=config.loadval)


def uplist(tmp):
    config.isload = 2
    config.loadval = 0
    loading()
    global index, value
    index = config.songList.curselection()
    value = config.songList.get(index)
    config.tmp = index[0]
    main()
    config.i = 0
    play(0, config.sound_file)
    config.songList.destroy()
    BtPlay.config(state="normal")


def goBack():
    config.songList.destroy()
    config.backButton.destroy()


def list():
    if config.playing == 1:
        config.sound_file.pause()
        progress.stop()
        refresh(1)
    config.playing = 0
    tmp = 1
    myFont = font.Font(size=16)
    config.songList = Listbox(root, font=myFont)
    for i in config.song:
        if len(i) > 30:
            i = i[:30] + "..."
        config.songList.insert(tmp, "  "+i)
        tmp += 1
    config.songList.place(relx=0.5, rely=0.5, anchor="c", height="500", width="420")
    config.songList.bind('<<ListboxSelect>>', uplist)
    config.backButton = Button(root, border='0', image=goback, command=lambda: goBack())
    config.backButton.place(relx=0.875, rely=0.9, anchor='c', height="50", width="50")


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
icon = PhotoImage(file='assets/icon.png')
root.iconphoto(False, icon)
playimg = PhotoImage(file="assets/play.png")
forward = PhotoImage(file="assets/forward.png")
back = PhotoImage(file="assets/back.png")
search = PhotoImage(file="assets/search.png")
ref = PhotoImage(file="assets/refresh.png")
goback = PhotoImage(file="assets/goback.png")
img = Image.open("temp.jpg")
img = img.resize((300, 300), Image.ANTIALIAS)
img.save("temp.jpg")
img = ImageTk.PhotoImage(Image.open("temp.jpg"))
lpic = Label(root, image=img)
s = ttk.Style()
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
progress = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient='horizontal', length=400, maximum=(config.songLength*20), mode='determinate', value=0)
BtPlay = Button(root, border='0', image=playimg, command=lambda: play(config.i, config.sound_file))
BtNext = Button(root, border='0', image=forward, command=lambda: next(config.sound_file))
BtPrev = Button(root, border='0', image=back, command=lambda: prev(config.sound_file))
BtTrev = Button(root, border='0', image=search, command=lambda: list())
BtRef = Button(root, border='0', image=ref, command=lambda: again())
cname = Label(root, text=config.songName, font=myFont)
lpic.place(relx=0.5, rely=0.0, anchor="n")
cname.place(relx=0.5, rely=0.65, anchor="c")
BtPlay.place(relx=0.5, rely=0.85, anchor="c")
BtPrev.place(relx=0.25, rely=0.85, anchor="c")
BtNext.place(relx=0.75, rely=0.85, anchor="c")
BtTrev.place(relx=0.1, rely=0.85, anchor="c")
BtRef.place(relx=0.9, rely=0.85, anchor="c")
progress.place(relx=0.5, rely=0.725, anchor="c", height=7)
root.mainloop()
