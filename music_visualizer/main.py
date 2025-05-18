import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QSlider,
    QHBoxLayout,
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

import cv2

from .audio import AudioPlayer
from .video import VideoSource
from . import effects


class VisualizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Visualizer")
        self.resize(800, 600)
        self.init_ui()

        self.audio = AudioPlayer()
        self.audio.amplitude_changed.connect(self.update_amplitude)

        self.video = VideoSource(0)
        self.video.frame_ready.connect(self.update_frame)

        self.amplitude = 0.0
        self.effect_intensity = 1.0

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label, 1)

        controls = QHBoxLayout()
        self.open_audio_btn = QPushButton("Open Audio")
        self.open_video_btn = QPushButton("Open Video")
        self.play_btn = QPushButton("Play")
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(1, 100)
        self.intensity_slider.setValue(50)

        controls.addWidget(self.open_audio_btn)
        controls.addWidget(self.open_video_btn)
        controls.addWidget(self.play_btn)
        controls.addWidget(self.intensity_slider, 1)
        layout.addLayout(controls)

        self.open_audio_btn.clicked.connect(self.choose_audio)
        self.open_video_btn.clicked.connect(self.choose_video)
        self.play_btn.clicked.connect(self.toggle_play)
        self.intensity_slider.valueChanged.connect(self.change_intensity)

    def choose_audio(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Audio", "", "Audio Files (*.mp3 *.wav)")
        if path:
            self.audio.load(path)

    def choose_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi)")
        if path:
            self.video.stop()
            self.video = VideoSource(path)
            self.video.frame_ready.connect(self.update_frame)
            self.video.start()

    def toggle_play(self):
        if self.audio.player.state() == self.audio.player.PlayingState:
            self.audio.pause()
            self.video.stop()
        else:
            self.audio.play()
            self.video.start()

    def change_intensity(self, value):
        self.effect_intensity = value / 50.0

    def update_amplitude(self, amp):
        self.amplitude = amp

    def update_frame(self, frame):
        frame = effects.apply_color_shift(frame, self.amplitude, self.effect_intensity)
        frame = effects.apply_blur(frame, self.amplitude, self.effect_intensity)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(img))


def main():
    app = QApplication(sys.argv)
    window = VisualizerWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
