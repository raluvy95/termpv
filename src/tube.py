from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
from utils import from_template_info, status
import os
import styling

YDL_OPTIONS = {'quiet': True}

def search_for(arg, count=5):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            video = ydl.extract_info(f"ytsearch{count}:{arg}", download=False)['entries']
        except DownloadError:
            print("Looks like there's something went wrong... Retrying...", flush=True)
            times = 1
            while True:
                try:
                    video = ydl.extract_info(f"ytsearch{count}:{arg}", download=False)['entries']
                    break
                except DownloadError:
                    times+=1
                    print(f"Looks like there's something went wrong... Retrying... ({times} attempts)", flush=True)
                    continue
                except KeyboardInterrupt:
                    video = None
                    break

    return video

def get(id):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        video = ydl.extract_info(id, download=False)
    return video

def get_print(id):
    styling.screen.clear()
    result = get(id)
    trm_size = os.get_terminal_size()
    trm_size = trm_size.columns - 1
    print(" INFORMATION ".center(trm_size - 1, "="), flush=True)
    for line in from_template_info(result):
        print(line)
    status(" %boldb%end - Back | %boldenter%end - Play | %boldd%end - Download | %boldq%end - Exit ")

def download(id, type):
    directory = None
    print(f"Will use the current directory - {os.getcwd()}", flush=True)
    prompt = input("Is it ok? [Y/N] ")
    if prompt.lower() == "y" or prompt.lower() == "yes":
        directory = os.getcwd()
        print("OK!", flush=True)
    else:
        while True:
            prompt1 = input("Please select the correct directory" )
            if os.path.isdir(prompt1):
                directory = prompt1
                print("OK!", flush=True)
                break
            elif prompt1.lower() == "q":
                raise SystemError
            else:
                continue
    if not type:
        raise TypeError("Cannot find 'type' key.")
    def hook(d):
        if d['status'] == 'finished':
            print('Done downloading!')
    name = "%(title)s-%(id)s.%(ext)s"
    OPTIONS = {
        'format': 'bestaudio/best' if type == "audio" else 'bestvideo+bestaudio/best',
        'progress_hooks': [hook],
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'outtmpl': f"{directory}/{name}",
        'restrictfilenames': True
    }
    if type == 'audio':
        OPTIONS['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }]
    with YoutubeDL(OPTIONS) as yt:
        if id.startswith("https://youtube.com/watch?=") or id.startswith("https://youtu.be/"):
            yt.download([id[:10]])
        elif id.startswith("http://") or id.startswith("https://"):
            yt.download([id])
        else:
            yt.download([f"https://youtube.com/watch?v={id}"])
    
