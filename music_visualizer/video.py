import cv2
from PyQt5.QtCore import QObject, pyqtSignal, QTimer


class VideoSource(QObject):
    """Provide frames from webcam or video file."""

    frame_ready = pyqtSignal(object)

    def __init__(self, source=0, parent=None):
        super().__init__(parent)
        self.source = source
        self.cap = cv2.VideoCapture(self.source)
        self.timer = QTimer()
        self.timer.timeout.connect(self.query_frame)

    def start(self, interval=30):
        if not self.timer.isActive():
            self.timer.start(interval)

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.cap:
            self.cap.release()

    def query_frame(self):
        if not self.cap.isOpened():
            return
        ret, frame = self.cap.read()
        if ret:
            self.frame_ready.emit(frame)
