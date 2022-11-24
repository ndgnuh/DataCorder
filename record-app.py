from argparse import ArgumentParser
from datacorder import utils
from datacorder.app import App


def main():
    parser = ArgumentParser()
    parser.add_argument("--camera-device", default=None)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--fps", default=24, type=int)
    parser.add_argument("--verbose", default=False, action="store_true")

    args = parser.parse_args()
    writer = utils.FrameWriter(root=args.output_dir, verbose=args.verbose)
    throttled_writer = utils.FrameThrottle(callback=writer.write, fps=args.fps)

    def frame_handler(frame, state):
        if state.recording:
            throttled_writer(frame)

    app = App(device=0 if args.camera_device is None else args.camera_device,
              frame_handler=frame_handler)
    app.run()


if __name__ == "__main__":
    main()
