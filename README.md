```
  ______
 /_  __/__  _________ ___  ____ _   __
  / / / _ \/ ___/ __ `__ \/ __ \ | / /
 / / /  __/ /  / / / / / / /_/ / |/ / 
/_/  \___/_/  /_/ /_/ /_/ .___/|___/  
                       /_/            
```

# Termpv
The front-end terminal for mpv and youtube-dl written in Python

# Contest
* [Installation](#Installing)
   * [Libraries required](#Libraries)
* [Start](#Start)
* [Configuration](#Configuration)
* [NOTE](#NOTE)
* [TODO](#TODO)
* [Troubleshooting](#Troubleshooting)
* [Credits](#Credits)

# Installing
We only have Linux x86_64 in [releases](https://github.com/raluvy95/termpv/releases)<br>
If you're using other OS or arhitecture, you need to build yourself.<br><br>
Requires to have **Python 3.8** and up. Open an issue if it works in older python version.

## Libraries required
You need to have libraries `ffmpeg`, `mpv`, `youtube-dl`, `chafa` and `python3` installed.

### Linux
Please install required libraries above (not `*-dev`) with your package manager.

### Other OS
I didn't test other OS except for Linux. I would be very appreciate if anyone can test it.

# Start
Clone this repository and run with `python3 cli.py` (make sure you installed libraries above)<br>
You can use with arguments for additional actions, see `cli.py --help` for more info.

# Configuration
We currently don't have custom configuration yet. Why not edit python file?

# NOTE
This project is in working progress which may not 100% working fine. Please fill the issue if you have one problem with this app.

# TODO
* Improvements in Player
* Custom configuration
* ???

# Troubleshooting
#### "FileNotFoundError: [Errno2] No such file or directory: 'mpv'" or similar error
You didn't installed required libraries above.
#### KeyError: 'channel'
You have older youtube-dl version, please upgrade it with `pip` or other package manager you use.


# Credits

Thanks:
* [@MsMaciek](https://github.com/MsMaciek123) - For making better way to listen to keyboard and display thumbnail in info page.

