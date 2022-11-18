# The code only test in windows system.
# -*- coding:utf-8 -*-

import os
import datetime
import loguru
import numpy as np
import cv2
from moviepy.editor import VideoFileClip
from tkinter.filedialog import *

from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

Folder_path = str("c:\\javanull")
file_exists = os.path.exists(Folder_path)
Folder_img = str(Folder_path + "\\img\\")
Folder_resize = str(Folder_path + "\\resize\\")
Folder_gif = str(Folder_path + "\\gif\\")
height = 550
width = 680


def log(s):
    loguru.logger.info(s)
    return s


def error_log(e):
    loguru.logger.error(e)
    return e


def make_dir():
    try:
        os.makedirs(Folder_path)
        os.makedirs(Folder_path + Folder_img)
        os.makedirs(Folder_path + Folder_resize)
        os.makedirs(Folder_path + "\\log")
        os.makedirs(Folder_path + Folder_gif)
        log(f'The file {file_exists} does not exist')

    except OSError as e:
        error_log('清空資料失敗'+str(e))
        pass
    # let exception propagate if we just can't
    # cd into the specified directory
    os.chdir(Folder_path)


if file_exists:
    log("folder has been exists")
else:
    make_dir()
    log('make new folder')


def img_resize():

    file_list = Folder_img
    dir_path = Folder_img

    # list to store files
    res = []
    # Iterate directory
    try:
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)
            files = str(dir_path + '' + path)
            log(files)
            im = cv2.imdecode(np.fromfile(str(file_list + '' + path), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            im = cv2.resize(im, (height, width))
            cv2.imencode('.jpg', im)[1].tofile(os.path.join(str(Folder_resize), path))
            if os.path.exists(files):
                os.remove(files)
    except OSError as e:
        error_log(e)
        pass


def mov_gif():
    try:
        accepted_files = [("Mov files", "*.mov"), ("MP4 files", "*.mp4")]
        path = askopenfilename(filetypes=accepted_files)
        filename = os.path.basename(path)

        clip = VideoFileClip(path)
        # Reduce the audio volume (volume x 0.8)
        clip = clip.volumex(0.8)

        clip = clip.resize((width, height))

        # fps=24 or fps=8 256 色一秒 24 格 or 256 色一秒 8 格
        clip.write_gif(Folder_gif+filename+".gif", fps=8)

        clip.close()
        log("mov_gif converse file->" + Folder_gif+filename)
    except OSError as e:
        error_log(e)
        pass


if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG',
        encoding="utf-8"
    )

log('please enter you selection 1 (resize) , 2 (Mov or Mp4 to gif) or 0 exits )')
c = input()
if c == '1':
    log('The image file has been resize and transfer into-> '+Folder_resize)
    img_resize()
elif c == '2':
    mov_gif()
    log('The Mov-video file has been converse to gif')
else:
    log('not action')

