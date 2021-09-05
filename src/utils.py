from typing import List
from src.style import Style
from datetime import datetime, timedelta
import os
from subprocess import check_output
import re

OUTPUT_TEMPLATE_INLINE = f"""{Style.BOLD}%title{Style.END} by %author
Duration: %time | Uploaded in: %upload
"""

OUTPUT_TEMPLATE = f"""{Style.BOLD}%title{Style.END}
Duration: %time
Creator: %creator
Uploaded in %upload (%since)
Likes: %likes
Dislikes: %dislikes
Average rate: %avg_rate/5
Tags: %tags
Category: %category"""

def num_to_time(num: int):
    a = timedelta(seconds=num)
    b = str(a)
    if(b.startswith('0:')):
        b = b[2:]
    return b


def ago(date: datetime):
    since = datetime.now() - date
    a = ['year', 'week', 'day', 'hour', 'minute', 'second']
    b = [int(since.days / 365), int(since.days / 7), since.days,
             int(since.seconds / 60 / 60), int(since.seconds / 60), since.seconds]
    for i in range(len(b)):
        if(b[i] != None and b[i] > 0):
            s = 's' if b[i] > 1 else ''
            return str(b[i]) + ' ' + a[i] + s + ' ago'


def from_template(obj, is_first_line=False) -> str:
    upload_date = obj['upload_date']
    dt = datetime(int(upload_date[:4]), int(
        upload_date[4:6]), int(upload_date[6:]))
    dt = f"{dt.year}/{dt.month}/{dt.day}"
    template_format = {
        "%author": obj['author'],
        "%title": f"{Style.UNDERLINE}{obj['title']}{Style.END}" if is_first_line else obj['title'],
        "%upload": dt,
        "%time": num_to_time(obj['duration']),
    }
    result = OUTPUT_TEMPLATE_INLINE
    for k, v in template_format.items():
        result = result.replace(k, v)
    return result


def from_template_info(obj) -> List[str]:

    def show_image(url, args):
        for c in ';|\\':
            if(c in url or c in args or '&&' in url or '&&' in args):
                return ['Execution contains disallowed characters!']

        result = check_output(f'chafa {url} {args}'.split(' '))
        return result.decode().split('\n')

    upload_date = obj['upload_date']
    dtog = datetime(int(upload_date[:4]), int(
        upload_date[4:6]), int(upload_date[6:]))
    dt = f"{dtog.year}/{dtog.month}/{dtog.day}"
    try:
        likes = obj['like_count']
        dislikes = obj['dislike_count']
        avg_rate = obj['average_rating']
    except KeyError:
        # videos which hides their rate count.
        likes = 0
        dislikes = 0
        avg_rate = 0
    template_format = {
        "%title": obj['title'],
        "%upload": dt,
        "%time": num_to_time(obj['duration']),
        "%since": ago(dtog),
        "%creator": obj['channel'],
        "%thumbnail": obj['thumbnail'],
        "%likes": str('{:,}'.format(likes)),
        "%dislikes": str('{:,}'.format(dislikes)),
        "%avg_rate": f"{avg_rate:.2f}",
        "%category": obj['categories'][0],
        "%tags": ', '.join(obj['tags'][:3]) + '...' if len(obj['tags']) > 3 else ''
    }
    result = OUTPUT_TEMPLATE
    for k, v in template_format.items():
        result = result.replace(k, v)
    img = show_image(obj['thumbnail'].replace("https", "http"), "-s 32x64")
    result = result.split('\n')
    term_size1 = os.get_terminal_size()
    term_size = term_size1.columns
    for lineID in range(len(img)):
        if(lineID < len(result)):
            limit_col = term_size - 32
            img[lineID] += ' ' + result[lineID][:limit_col - 1]
        else:
            img[lineID] += '\n'
    img[-1] += f"Link to video: {obj['webpage_url']}"[:term_size] + "\n"
    img[-1] += obj['description'][:250]
    return img

def status(info=None):
    formats = {
        "%bold": Style.BOLD,
        "%end": Style.END
    }
    if not info:
        info = " %boldup/down%end - Navigate your results | %boldenter%end - Info | %bolds%end - Search | %boldq%end - Exit "
    for k, v in formats.items():
        info = info.replace(k, v)
    match_count = re.findall("(%bold|%end)", info)
    line(info, len(match_count) * 3)


def line(title: str = None, extra: int=0):
    trm_size = os.get_terminal_size()
    trm_size = trm_size.columns - 1
    if title:
        center = title.center(trm_size, "=")
        center2 = "=" * int(extra / 2) + center + "=" * int(extra / 2)
        print(center2, flush=True)
    else:
        print("=" * trm_size, flush=True)
