from argparse import ArgumentParser
from datacorder import utils
from typing import List
from os import path
from videoio import videoread

import os


def main_(src_files: List[str], dst: str, fps: int):
    seq = utils.AutoSequence()
    for file in src_files:
        root = path.join(dst, "%03d" % seq.next())
        writer = utils.FrameWriter(root=root, verbose=True, name_format="%03d")
        throttled_writer = utils.FrameThrottle(callback=writer.write, fps=fps)
        for frame in videoread(file):
            throttled_writer(frame)


def main():
    parser = ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--fps", default=24, type=int)
    args = parser.parse_args()

    inputs = [path.join(args.input, file) for file in os.listdir(args.input)]
    main_(inputs, args.output, args.fps)


if __name__ == "__main__":
    main()
