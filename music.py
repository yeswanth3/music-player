# importing required modules


from tkinter import *  #------------------------- [responsible for GUI]
import os  #--------------------------------------[getting music file names]
from tkinter import filedialog #------------------[to open file]
from pygame import mixer #------------------------[to play/pause/stop music]
import time #-------------------------------------[to find length]
from mutagen.mp3 import MP3 #---------------------[finding length of mp3 file]
import tkinter.messagebox #-----------------------[to show error messages]
from tkinter import ttk #-------------------------[for themes]
from ttkthemes import themed_tk as tk #-----------[for themes]
import threading


#------------creating a window----------------



root = tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.title('yesh')
root.iconbitmap(r'images/note.ico')


#-----------statusbar---------------------------



statusbar = ttk.Label(root, text='welcome to music player', relief=SUNKEN, anchor=W,font='times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)


#--------------create menubar-------------------



menubar = Menu(root)
root.configure(menu=menubar)


#-------------------ask user to open a file-----------------


playlist=[]
def opn_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename=os.path.basename(filename)
    index=0
    playlistbox.insert(index, filename)
    playlist.insert(index,filename_path)
    index=index+1


#------------------create the sub menu 1--------------------------



submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='file', menu=submenu)
# adding options
submenu.add_command(label='open', command=opn_file,font='times 10 italic')
submenu.add_command(label='exit', command=root.destroy,font='times 10 italic')


#-------------------------create the sub menu 2--------------------



def abt_us():
    tkinter.messagebox.showinfo('yesh ', 'hi welcome to yesh music player')

submenu = Menu(menubar, tearoff=0)
# adding options
menubar.add_cascade(label='help', menu=submenu)
submenu.add_command(label='About us', command=abt_us,font='times 10 italic')


#----------------------------frames----------------------



leftframe=Frame(root)
leftframe.pack(side=LEFT)

#listbox

playlistbox=Listbox(leftframe)
playlistbox.pack(padx=20)

rightframe=Frame(root)
rightframe.pack()

topframe=Frame(rightframe)
topframe.pack()


middleframe=Frame(rightframe,relief=RAISED)
middleframe.pack(padx=10,pady=10)

#-------------------buttons to add/delete songs to playlist-------------------------



addbtn=ttk.Button(leftframe,text='add',command=opn_file)
addbtn.pack(side=LEFT,padx=30)

def del_song():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        playlistbox.delete(selected_song)
        playlist.pop(selected_song)
    except:
        tkinter.messagebox.showerror('file not found', 'select a file')

delbtn=ttk.Button(leftframe,text='delete',command=del_song)
delbtn.pack(side=LEFT)


#------------------------label------------------------------



lengthlabel = ttk.Label(rightframe, text='Length --:--',font='times 10 bold')
lengthlabel.pack(pady=5,padx=10)

currenttimelabel =ttk.Label(rightframe, text='current time --:--',relief=GROOVE,font='times 10 bold')
currenttimelabel.pack()


#----------------------showing the deatils-----------------------



def show_details(play_song):
    audio = MP3(play_song)
    total_length = audio.info.length
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = 'total length' + '-' + timeformat
    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()


#----------------------finding the length of mp3 file------------------------



def start_count(t):
    global paused
    cur_tym=0
    while cur_tym<=t and mixer.music.get_busy():
        if paused:
            continue


        else:
            mins, secs = divmod(cur_tym, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = 'current time' + '-' + timeformat
            time.sleep(1)
            cur_tym=cur_tym+1


#-----------------------playing and resuming a song-------------------------------



def play_btn():
    global paused
    if(paused):
        mixer.music.unpause()
        statusbar['text'] = 'resumed'
        paused=False
    else:
        try:
            stop_btn()
            time.sleep(1)
            selected_song=playlistbox.curselection()
            selected_song=int(selected_song[0])
            play_it=playlist[selected_song]
            if (filename_path.endswith('mp3') == True):
                mixer.music.load(play_it)
                mixer.music.play()
                statusbar['text'] = 'playing' + ' ' + os.path.basename(play_it)
                show_details(play_it)
            else:
                tkinter.messagebox.showerror('only MP3', 'select a MP3 file')
        except:
            tkinter.messagebox.showerror('file not found', 'select a file')



playphoto = PhotoImage(file='images/play.png')
btn1 =ttk.Button(middleframe, image=playphoto, command=play_btn)
btn1.grid(row=0,column=0,padx=10)


#--------------------stoping a song--------------------



def stop_btn():

    mixer.music.stop()
    statusbar['text'] = 'stopped'

stopphoto = PhotoImage(file='images/stop.png')
btn2 = ttk.Button(middleframe, image=stopphoto, command=stop_btn)
btn2.grid(row=0,column=1,padx=10)


#------------------------pausing a song-------------------



paused=False
def pause_btn():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = 'paused'

pausephoto = PhotoImage(file='images/pause.png')
btn3 =ttk.Button(middleframe, image=pausephoto, command=pause_btn)
btn3.grid(row=0,column=2,padx=10)


#-------------------rewind the song----------------------



bottomframe=Frame(rightframe,relief=RAISED)
bottomframe.pack(padx=10,pady=10)

def rewind_btn():
    global paused
    global cur_tym
    global rewind
    paused=False
    rewind=True
    play_btn()
    statusbar['text']='rewinded'
    cur_tym=0

rewindphoto = PhotoImage(file='images/rewind.png')
btn4= ttk.Button(bottomframe, image=rewindphoto,command=rewind_btn)
btn4.grid(row=0,column=0,padx=20)


#----------------------mute a song------------------------



muted=False
def mute_btn():
    global muted
    if(muted):
        mixer.music.set_volume(100)
        btn5.configure(image=volumephoto)
        scale.set(100)
        muted=False

    else:
        mixer.music.set_volume(0)
        btn5.configure(image=mutephoto)
        scale.set(0)
        muted=True

mutephoto = PhotoImage(file='images/mute.png')
volumephoto = PhotoImage(file='images/volume.png')
btn5=ttk.Button(bottomframe, image=volumephoto, command=mute_btn)
btn5.grid(row=0,column=1)


#--------------------volumecontrol-------------------



mixer.init()

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(70)
scale.grid(row=0,column=2,padx=20)
#scale.pack()


#----------------------rewriting the original button--------------------



def on_close():
    stop_btn()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_close)


root.mainloop()
