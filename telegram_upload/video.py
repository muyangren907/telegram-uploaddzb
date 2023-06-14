import platform
import re
import subprocess
import tempfile
import os

from zuikuihuoshou.xiaoxiexx import tiquxinxi
from zuikuihuoshou.parser import createParser
from zuikuihuoshou.core import config as zuikuihuoshou_config

from telegram_upload.exceptions import ThumbVideoError


zuikuihuoshou_config.quiet = True


def video_xiaoxiexx(file):
    # return None
    return tiquxinxi(createParser(file))


def call_ffmpeg(dzffn, args):
    # dzffn = 'ffmpeg'
    try:
        return subprocess.Popen([get_ffmpeg_command(dzffn)] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise ThumbVideoError('{} command is not available. Thumbnails for videos are not available!'.format(dzffn))


def get_ffmpeg_command(dzffn):
    return os.environ.get('FFMPEG_COMMAND',
                          '{}.exe'.format(dzffn) if platform.system() == 'Windows' else '{}'.format(dzffn))


def get_video_size(dzffn, file):
    p = call_ffmpeg(dzffn, [
        '-i', file,
    ])
    stdout, stderr = p.communicate()
    video_lines = re.findall(': Video: ([^\n]+)', stderr.decode('utf-8'))
    if not video_lines:
        return
    matchs = re.findall("(\d{2,6})x(\d{2,6})", video_lines[0])
    if matchs:
        return [int(x) for x in matchs[0]]


def get_video_thumb(dzffn, file, output=None, size=200):
    output = output or tempfile.NamedTemporaryFile(suffix='.jpg').name
    xiaoxiexx = video_xiaoxiexx(file)
    # xiaoxiexx = None
    if xiaoxiexx is None:
        return
    duration = xiaoxiexx.get('duration').seconds if xiaoxiexx.has('duration') else 0
    ratio = get_video_size(dzffn, file)
    if ratio is None:
        raise ThumbVideoError('Video ratio is not available.')
    if ratio[0] / ratio[1] > 1:
        width, height = size, -1
    else:
        width, height = -1, size
    p = call_ffmpeg(dzffn, [
        '-ss', str(int(duration / 2)),
        '-i', file,
        '-filter:v',
        'scale={}:{}'.format(width, height),
        '-vframes:v', '1',
        output,
    ])
    p.communicate()
    if not p.returncode and os.path.lexists(file):
        return output
