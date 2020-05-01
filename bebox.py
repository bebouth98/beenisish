import os
import pafy
import time
import youtube_dl
import webbrowser
queue = []
pafy.set_api_key("AIzaSyAy2195YHslXWtjZY-0W_SdmVscXVzYL2Y")

def addqueu(search):
    os.system('youtube-dl -j --dump-json "ytsearch1:{0}" > json.txt'.format(search))
    file = open('json.txt', "r")
    lines = file.readlines()
    tmpstr = lines[0]
    tmpid = tmpstr[8:19]
    link = "https://www.youtube.com/watch?v=" + tmpid
    queue.append(link)
    print(link + "has been added to queue")
def play():
    print("playing " + queue[0])
    webbrowser.open(queue[0])
def isPlaying(link, tic):
    vid = pafy.new(link)
    toc = tic + vid.length
    if int(time.perf_counter()) >= toc:
        return True
    else:
        return False

first = False
gotFirst = False
tic = 0
while True:
    if gotFirst:
        if first:
            tic = int(time.perf_counter())
            first = False
            play()
        elif len(queue) > 1 and isPlaying(queue[0], tic):
            tic = int(time.perf_counter())
            queue.pop(0)
            play()
        else:
            print("song still playing")
    inp = input("Enter Song Request with !song:")
    req = inp[0:5]
    if req == "!song":
        search = inp[5:]
        if len(search) == 0:
            print("must add song request after !song")
            continue
        else:
            addqueu(search)
            if not gotFirst:
                first = True
                gotFirst = True
    if req == "!skip":
        if len(queue) == 1:
            queue.pop(0)
            tic = int(time.perf_counter())
            gotFirst = False
            first = False
        elif len(queue) > 1:
            tic = int(time.perf_counter())
            queue.pop(0)
            play()
        else:
            print("nothing to skip")
    if req == "!done":
        break;




