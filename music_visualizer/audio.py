import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudioProbe


class AudioPlayer(QObject):
    """Play audio files and expose amplitude levels."""

    amplitude_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.player = QMediaPlayer()
        self.probe = QAudioProbe()
        self.probe.setSource(self.player)
        self.probe.audioBufferProbed.connect(self.process_buffer)

    def load(self, path: str):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def process_buffer(self, buffer):
        data = buffer.data()
        if not data:
            return
        samples = np.frombuffer(data, dtype=np.int16)
        if samples.size == 0:
            return
        amplitude = float(np.abs(samples).max()) / 32768.0
        self.amplitude_changed.emit(amplitude)
