import os
import pafy
import time
import youtube_dl
import webbrowser
from playsound import playsound
from multiprocessing import Process
link_queue = []
song_queue = []
process_queue = []
counter = 0
id_counter = 0
finished_playthrough = False

current_song = None


def addlink_queue(search):
    global counter, id_counter
    os.system('youtube-dl -j --dump-json "ytsearch1:{0}" > json.txt'.format(search))
    file = open('json.txt', "r")
    lines = file.readlines()
    tmpstr = lines[0]
    tmpid = tmpstr[8:19]
    link = "https://www.youtube.com/watch?v=" + tmpid
    print(link + "has been added to link_queue")
    song_name = str(id_counter) + '.mp3'
    os.system('youtube-dl --extract-audio --audio-format mp3 '  + link + ' --output "' + str(id_counter) + '.%(ext)s"')
    link_queue.append(link)
    song_queue.append(song_name)
    process_queue.append(Process(name="playsong", target=play_song))
    id_counter += 1
def play_song():
    print("playing " + link_queue[0]) # Figure out how the fuck to play the next song in queue once the first is finished without manually skipping
    playsound(song_queue[0])
def isPlaying(link, tic):
    vid = pafy.new(link)
    toc = tic + vid.length
    if int(time.perf_counter()) >= toc:
        return True
    else:
        return False
def skip():
    process_queue[0].terminate()
    os.remove(song_queue[0])
    process_queue.pop(0)
    song_queue.pop(0)
    process_queue[0].start()


while True:
    inp = input("Enter Song Request with !song:")
    req = inp[0:5]
    if req == "!song":
        search = inp[5:]
        if len(search) == 0:
            print("must add song request after !song")
            continue
        else:
            addlink_queue(search)
            if len(song_queue) == 1:
                print("playing song now")
                process_queue[0].start()

    if req == "!skip":
        if len(song_queue) > 1:
            skip()
        else:
            print("No songs left in queue")
    if req == "!done":
        break


for p in process_queue:
    if p != None:
        p.terminate()   

for song in song_queue:
    print(song)
    os.remove(song)