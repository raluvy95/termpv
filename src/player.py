from src import mpv, styling
from src.utils import num_to_time, status
import sys
import time
from src.style import Style
import os
import json
import subprocess


class Player(mpv.MPV):
    def __init__(self, url: str, duration: int = -1, video_only=False, file_only=False):
        if video_only:
            super().__init__(ytdl=True, player_operation_mode='pseudo-gui',
                             input_default_bindings=True,
                             input_vo_keyboard=True,
                             osc=True)
        elif file_only:
            split_file = os.path.splitext(url)
            # Videos
            if split_file[-1] in [".mp4", ".webm", ".mkv", ".flv", ".wmv"]:
                super().__init__(player_operation_mode='pseudo-gui',
                                 input_default_bindings=True,
                                 input_vo_keyboard=True,
                                 osc=True)
            # Audio
            elif split_file[-1] in [".mp3", ".ogg", ".m4a", ".oga", ".mogg", ".wma"]:
                super().__init__(video=False)
            else:
                raise TypeError(f"Unknown file extension '{split_file[-1]}'")
        else:
            super().__init__(ytdl=True, video=False)
        if duration == -1:
            # TODO: GET DURATION OF A MEDIA FILE.
            pass
        self.duration = duration
        self.url = url
        self.current_time = 0
        self.remain = 0 if duration >= 0 else "?"
        status(
"""%boldq%end - Stop %boldenter/space%end - Pause %boldl%end - Toggle loop
%boldright/left%end - Seek to 5s %boldup/down%end - Seek to 1m %boldm%end - Toggle mute""")
        sys.stdout.write("\rConnecting to Network...")
        sys.stdout.flush()

        @self.property_observer("time-pos")
        def print_info(_name, value):
            try:
                current_second = int(value)
                if self.current_time != current_second:
                    self.current_time = current_second
                    if self.remain == "?":
                        self.duration = "?"
                    else:
                        self.remain = duration - self.current_time
                    trm_size = os.get_terminal_size()
                    trm_size = trm_size.columns - 1
                    d = num_to_time(self.duration) if self.duration != "?" else "?"
                    r = num_to_time(self.remain) if self.remain != "?" else "?"
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{d}] {self.progress_bar()} {r} remains")
                    sys.stdout.flush()
            except TypeError:
                pass

    def __call__(self):
        # THE KEYBOARD LISTENER
        self.wait_until_playing()
        while True:
            arrow = styling.screen.getControl()
            if arrow == 'q':
                self.stop()
                styling.screen.clear()
                print("Finished playing! Returning to the info page...")
                time.sleep(0.5)
                self.terminate()
                break
            elif arrow == styling.Arrow.RIGHT:
                self.seek(5)
            elif arrow == styling.Arrow.LEFT:
                self.seek(-5)
            elif arrow == styling.Arrow.UP:
                self.seek(60)
            elif arrow == styling.Arrow.DOWN:
                self.seek(-60)
            elif arrow == 'l':
                if self.loop:
                    self.loop = False
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{num_to_time(self.duration)}] {self.progress_bar()} {num_to_time(self.remain)} remains - Loop disabled!")
                    sys.stdout.flush()
                else:
                    self.loop = True
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{num_to_time(self.duration)}] {self.progress_bar()} {num_to_time(self.remain)} remains - Loop activated!")
                    sys.stdout.flush()
            elif arrow == "enter" or arrow == ' ':
                is_paused = self._get_property("pause")
                if is_paused:
                    self._set_property("pause", False)
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{num_to_time(self.duration)}] {self.progress_bar()} {num_to_time(self.remain)} remains - Resume")
                    sys.stdout.flush()
                else:
                    self._set_property("pause", True)
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{num_to_time(self.duration)}] {self.progress_bar()} {num_to_time(self.remain)} remains - Paused!")
                    sys.stdout.flush()
            elif arrow == "+":
                volume = self._get_property("volume")
                if int(volume) == 100:
                    pass
                else:
                    volume += 10
                    self._set_property("volume", volume)
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{num_to_time(self.duration)}] {self.progress_bar()} {num_to_time(self.remain)} remains - Volume {volume}%")
                    sys.stdout.flush()
            elif arrow == "-":
                volume = self._get_property("volume")
                if int(volume) == 0:
                    pass
                else:
                    volume -= 10
                    self._set_property("volume", volume)
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{num_to_time(self.duration)}] {self.progress_bar()} {num_to_time(self.remain)} remains - Volume {volume}%")
                    sys.stdout.flush()
            elif arrow == "m":
                volume = self._get_property("volume")
                if int(volume) == 0:
                    self._set_property("volume", 100)
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{num_to_time(self.duration)}] {self.progress_bar()} {num_to_time(self.remain)} remains - Unmuted!")
                    sys.stdout.flush()
                else:
                    self._set_property("volume", 0)
                    sys.stdout.write(
                        f"\r[{num_to_time(self.current_time)}/{num_to_time(self.duration)}] {self.progress_bar()} {num_to_time(self.remain)} remains - Muted!")
                    sys.stdout.flush()

    def play(self):
        return super().play(self.url)

    def progress_bar(self):
        width = 3
        percentage = ((self.current_time) / self.duration) * 100
        fill = round(percentage / 10) * width
        empty = (width * 10) - fill
        return f'[{"#" * (fill)}{" " * empty}]'
