from time import sleep
from src.tube import get, search_for, get_print, download
from src import styling, utils
from src.style import Style
import sys
from subprocess import check_output
from youtube_dl import version
from src.args import get_args

LOGO = """
      ______
     /_  __/__  _________ ___  ____ _   __
      / / / _ \/ ___/ __ `__ \/ __ \ | / /
     / / /  __/ /  / / / / / / /_/ / |/ / 
    /_/  \___/_/  /_/ /_/ /_/ .___/|___/  
                           /_/            

@boldThe Terminal based front-end for mpv and youtube-dl@end
"""

TERMPV_VERSION = "0.1.1"

class MainTube:
    def __init__(self, search=None, quick_aud=None, quick_vid=None) -> None:
        # Some variables
        self.count = 0
        self.cached = []
        self.index = 0
        if quick_vid:
            self.quick = 'v'
        elif quick_aud:
            self.quick = 'a'
        else:
            self.quick = False

        # The child screen
        self.is_on_info_page = False
        self.is_on_prompt = False
        self.is_on_about = False

        # Start search after creating an object
        self.search(search)

    def info(self):
        if not self.is_on_about and not self.is_on_info_page:
            styling.screen.clear()
            print(LOGO, flush=True)
            print("Feel free to use, modify or share this program under GPLv3 license.", flush=True)
            utils.status(" Press %boldq%end to return.")

    def play(self, active_obj, video_only=False):
        self.quick = False
        styling.screen.clear()
        print(f"""{Style.BOLD}{active_obj['title']}{Style.END}
by {active_obj['author']}
""")
        from src.player import Player
        try:
            player = Player(f"https://youtube.com/watch?v={active_obj['id']}", active_obj['duration'],
                            video_only=video_only)
            player.play()
            player()
            player.wait_for_playback()
        except:
            pass
        finally:
            styling.screen.clear()
            print("Loading...", flush=True)
            get_print(active_obj['id'])
            self.is_on_prompt = False

    def __call__(self):
        while True:
            arrow = styling.screen.getArrow()
            if arrow == styling.Arrow.DOWN:
                if not self.is_on_info_page:
                    self.go("down")
                else:
                    pass
            elif arrow == 'q':
                if self.is_on_about and not self.is_on_info_page:
                    self.is_on_about = False
                    self.refresh()
                else:
                    break
            elif arrow == styling.Arrow.UP:
                if not self.is_on_info_page:
                    self.go("up")
                else:
                    pass
            elif arrow == 'b':
                if self.is_on_info_page:
                    self.is_on_info_page = False
                    self.refresh()
                else:
                    pass
            elif arrow == 'enter':
                active_obj = self.__get_active_obj()
                if not self.is_on_info_page:
                    styling.screen.clear()
                    print("Loading...", flush=True)
                    get_print(active_obj['id'])
                    self.is_on_info_page = True
                elif self.is_on_info_page and not self.is_on_prompt:
                    self.is_on_prompt = True
                    styling.screen.clear()
                    response = input(
                        f"Do you want to play {Style.BOLD}{active_obj['title']}{Style.END} [Y/N]?")
                    if response.lower() == 'y' or response.lower() == 'yes':
                        ano_response = input("Audio or Video? [A/V/D]")
                        if ano_response.lower() == 'a' or ano_response.lower() == 'd':
                            self.play(active_obj, False)
                        else:
                            self.play(active_obj, True)
                    else:
                        self.is_on_prompt = False
                        styling.screen.clear()
                        print("Loading...", flush=True)
                        get_print(active_obj['id'])
                        self.is_on_info_page = True
            elif arrow == 's':
                styling.screen.clear()
                self.search()
            elif arrow == 'd':
                if self.is_on_info_page:
                    styling.screen.clear()
                    active_obj = self.__get_active_obj()
                    print(
                        f"{active_obj['title']}\nby {active_obj['author']}", flush=True)
                    prompt1 = input("Would you like to download this? [Y/N] ")
                    if prompt1.lower() == "y" or prompt1.lower() == "yes":
                        prompt2 = input("Audio [mp3] or Video [mp4]? [A/V] ")
                        try:
                            if prompt2.lower() == "v":
                                download(active_obj['id'], "video")
                            else:
                                download(active_obj['id'], "audio")
                        finally:
                            print("Finished! Press any key to return to info page ")
                            styling.screen.getChar()
                            styling.screen.clear()
                            print(
                                "The download process is ended! Returning to info page...", flush=True)
                            sleep(2)
                            get_print(active_obj['id'])
                    else:
                        styling.screen.clear()
                        print(
                            "Download cancelled! Returning to info page...", flush=True)
                        sleep(2)
                        get_print(active_obj['id'])
            elif arrow == "i":
                if not self.is_on_info_page and not self.is_on_prompt:
                    self.is_on_about = True
                    self.info()


    def __get_active_obj(self):
        for obj in self.cached:
            if obj['is_active']:
                return obj

    def search(self, args=None):
        self.count = 0
        self.cached = []
        styling.screen.clear()
        resulted = None
        if not args:
            resulted = input("Search: ")
        else:
            resulted = args
        styling.screen.clear()
        print("Loading... This might take a while", flush=True)
        results = search_for(resulted)
        styling.screen.clear()
        if not results:
            raise KeyboardInterrupt
        for thing in results:
            subtitle = {}
            try:
                subtitle = thing['subtitles']
            except KeyError:
                pass
            self.cached.append({
                'id': thing['id'],
                'title': thing['title'],
                'thumbnail': thing['thumbnail'],
                'link': thing['webpage_url'],
                'author': thing['channel'],
                'is_active': True if self.count == 0 else False,
                'duration': thing['duration'],
                'upload_date': thing['upload_date'],
                'description': thing['description'],
                'subtitle': subtitle
            })
            self.count += 1
        if self.quick == 'a':
            self.is_on_info_page = True
            active_obj = self.__get_active_obj()
            self.play(active_obj, True)
        elif self.quick == 'v':
            self.is_on_info_page = True
            active_obj = self.__get_active_obj()
            self.play(active_obj)
        else:
            self.is_on_info_page = False
            utils.line(" RESULTS ")
            for obj in self.cached:
                print(utils.from_template(obj, obj['is_active']), flush=True)
            utils.status()

    def refresh(self):
        styling.screen.clear()
        utils.line(" RESULTS ")
        for obj in self.cached:
            print(utils.from_template(obj, obj['is_active']), flush=True)
        utils.status()

    def go(self, action):
        if action == 'up':
            self.index -= 1
        else:
            self.index += 1
        try:
            if self.cached[self.index]['is_active']:
                pass
        except IndexError:
            if action == 'up':
                self.index = self.index + 1
            else:
                self.index = self.index - 1
        else:
            if action == 'up':
                self.cached[self.index + 1]['is_active'] = False
                self.cached[self.index]['is_active'] = True
            else:
                self.cached[self.index - 1]['is_active'] = False
                self.cached[self.index]['is_active'] = True
            self.refresh()


def run(search=None, quick_vid=False, quick_aud=False):
    try:
        main = MainTube(search, quick_vid, quick_aud)
        main()
    except KeyboardInterrupt:
        styling.screen.clear()
        print("Quiting program...")
        import sys
        sys.exit()

def get_versions():
    result = check_output('mpv --version'.split(' '))
    lines = result.decode().split('\n')
    mpv_version = lines[0][4:10]
    ffmpeg_version = lines[9][16:21]
    return (mpv_version, ffmpeg_version)


def welcome(arg, version_only=False):
    if not version_only:
        styling.screen.clear()
    mpv, ffmpeg = get_versions()
    VERSIONS = {
        "termpv": TERMPV_VERSION,
        "youtube-dl": version.__version__,
        "mpv": mpv,
        "ffmpeg": ffmpeg
    }
    if arg.intro:
        FORMAT = {
            "@bold": "\033[1m",
            "@end": "\033[0m"
        }
        lines = LOGO
        for k, v in FORMAT.items():
            lines = lines.replace(k, v)
        for _i in range(len(lines)):
            sys.stdout.write(lines[_i])
            sys.stdout.flush()
            sleep(0.005)
        sleep(2)
    for k, v in VERSIONS.items():
        print(f"Using {k} - version {v}")
    if not version_only:
        utils.status(" Type... %bolds%end - Search | %boldd%end - Quick Download | %boldq%end - Exit ")
        i = input("> ")
        i = i.lower()
        if i == "q":
            sys.exit(0)
        elif i == "s":
            run()
        elif i == "d":
            while True:
                link = input("Link: ")
                if not link:
                    continue
                else:
                    break
            while True:
                type1 = input("Audio (mp3) or Video (mp4)? [A/V] ")
                if not type1:
                    continue
                if not type1.lower() in ["a", "v"]:
                    continue
                else: break
            type1 = "audio" if type1 == "a" else "video"
            download(link, type1)
    else:
        sys.exit(0)
                

def start():
    arg = get_args()
    if arg.search:
        run(" ".join(arg.search), quick_vid=arg.quick_video,
            quick_aud=arg.quick_audio)
    elif arg.file:
        styling.screen.clear()
        from src.player import Player
        play = Player(" ".join(arg.file), file_only=True)
        try:
            play.play()
            play()
            play.wait_for_playback()
        except:
            pass
        finally:
            styling.screen.clear()
            print("Quitting...", flush=True)
            sys.exit()
    elif arg.quick_audio or arg.quick_video:
        run(quick_aud=arg.quick_audio, quick_vid=arg.quick_video)
    elif arg.version:
        welcome(arg, version_only=True)
    else:
        welcome(arg)
