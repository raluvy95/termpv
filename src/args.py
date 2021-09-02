import argparse

parser = argparse.ArgumentParser(
    add_help=True, description="Terminal based front-end for mpv and youtube-dl")
parser.add_argument("-q", "--quick",
                    dest="quick_video",
                    default=False,
                    action='store_true',
                    help="Quick mode - Instant play without confirmation."
                    )
parser.add_argument("-Q",
                    dest="quick_audio",
                    default=False,
                    action='store_true',
                    help="Same as -q, but will play in audio mode."
                    )
parser.add_argument("-s", "--search",
                    dest="search",
                    default=False,
                    help="Search on YouTube.",
                    type=str,
                    nargs='+',
                    )
parser.add_argument("-i", "--intro",
                    dest="intro",
                    default=False,
                    action="store_true",
                    help="Show animation intro at launch program.",
                    )
parser.add_argument("-f", "--file",
                    dest="file",
                    help="Open filename and play in audio/video depending on what format they use.",
                    default=None,
                    type=str,
                    nargs=1
                    )
parser.add_argument("-v", "--v", "--version",
                    dest="version",
                    help="Shows version and exit.",
                    default=False,
                    action="store_true")


def get_args():
    return parser.parse_args()
