import cv2
import os
import numpy as np

from os import path
from dataclasses import dataclass, field
from typing import Callable


class AutoSequence(dict):
    def next(self, key=None, default_start=0):
        current_value = self.get(key, default_start)
        next_value = current_value + 1
        self[key] = next_value
        return next_value


class FrameThrottle:
    """
    Handle only the clearest frames in a video or a video stream
    """

    def __init__(self, callback: Callable, fps=24):
        self.fps = fps
        self.callback = callback
        self.selected_frame = None
        self.max_clear = -1
        self.nframes = 0

    def __call__(self, frame):
        if self.nframes < self.fps:
            self.nframes += 1
            clear = cv2.Laplacian(frame, cv2.CV_8UC3).var()
            if clear > self.max_clear:
                self.max_clear = clear
                self.selected_frame = frame
        else:
            self.callback(self.selected_frame)
            self.nframes = 0
            self.selected_frame = None
            self.max_clear = -1


def max_sequence_from_dir(d: str):
    files = os.listdir(d)
    names = [path.splitext(file)[0] for file in files]

    def try_int(x):
        try:
            return int(x)
        except Exception:
            return -99
    idx = [try_int(name) for name in names]
    if len(idx) == 0:
        return 0
    return max(idx)


class FrameWriter:
    def __init__(self, root, name_format="%09d", ext="jpg", verbose=False):
        self.root = root
        self.name_format = name_format
        self.ext = ext
        self.verbose = verbose

        if path.isdir(root):
            self.current_idx = max_sequence_from_dir(root)
        else:
            os.makedirs(root, exist_ok=True)
            self.current_idx = 0

    def get_frame_name(self, idx):
        return (self.name_format % idx) + "." + self.ext

    def write(self, image: np.ndarray):
        self.current_idx += 1
        name = self.get_frame_name(self.current_idx)
        out = path.join(self.root, name)
        cv2.imwrite(out, image)
        if self.verbose:
            print(f" Output written to {out}")
