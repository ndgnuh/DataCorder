import cv2

from dataclasses import dataclass
from typing import Callable


@dataclass
class State:
    running: bool = True
    recording: bool = False


def default_frame_handler(*args, **kwargs):
    pass


class App:
    def __init__(self,
                 device,
                 frame_handler: Callable = default_frame_handler):
        self.device = device
        self.frame_handler = frame_handler
        self.state = State()

    def draw(self, frame):
        state = self.state
        if state.recording:
            cv2.putText(frame, "[Rec]",
                        (0, 30),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
                        (255, 0, 0))
        return frame

    def run(self):
        cap = cv2.VideoCapture(self.device)

        while self.state.running:
            _, frame = cap.read()

            if frame is not None:
                dframe = self.draw(frame.copy())
                cv2.imshow("video", dframe)
                self.frame_handler(frame=frame, state=self.state)

            key = cv2.waitKey(1)
            if key == 0xFF & ord('q'):
                self.state.running = False

            if key == 0xFF & ord('r'):
                self.state.recording = not self.state.recording
