
import sys
from PySide6 import QtCore, QtWidgets

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 100
PADDING = 15
WINDOW_GAP = 5
PROGRESS_HEIGHT = 4
TICK_MS = 30


class QtNotification(QtWidgets.QWidget):
    def __init__(
        self,
        title: str,
        content: str,
        on_close: callable = lambda w: None,
        duration_ms: int | None = None,   # NEW
    ):
        super().__init__()
        self.on_close = on_close
        self.duration_ms = duration_ms
        self.elapsed_ms = 0

        # Translucent background
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Frameless + always on top
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        # ---------------- CONTAINER ----------------
        self.container = QtWidgets.QWidget(self)
        self.container.setObjectName("container")
        self.container.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.container.setStyleSheet("""
            #container {
                background-color: rgba(0, 0, 0, 200);
                color: white;
                border-radius: 10px;
            }
            QLabel {
                background-color: transparent;
            }
            QPushButton#closeButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
                padding: 0px;
            }
            QPushButton#closeButton:hover {
                color: #ff6666;
            }
            QProgressBar {
                border: none;
                background: rgba(255, 255, 255, 40);
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: rgba(255, 255, 255, 180);
                border-radius: 2px;
            }
        """)

        # ---------------- TITLE ----------------
        self.title_label = QtWidgets.QLabel(title, self.container)
        self.title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color:white;"
        )

        # ---------------- CONTENT ----------------
        self.content_label = QtWidgets.QLabel(content, self.container)
        self.content_label.setStyleSheet(
            "font-size: 18px;color:white;"
        )

        # ---------------- CLOSE BUTTON ----------------
        self.close_button = QtWidgets.QPushButton("✕", self.container)
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)

        # ---------------- PROGRESS BAR ----------------
        self.progress = QtWidgets.QProgressBar(self.container)
        self.progress.setRange(0, 1000)
        self.progress.setValue(1000)
        self.progress.setTextVisible(False)

        # ---------------- TIMER ----------------
        self.timer = None
        if self.duration_ms and self.duration_ms > 0:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self._on_tick)
            self.timer.start(TICK_MS)

    # ---------------- TIMER LOGIC ----------------
    def _on_tick(self):
        self.elapsed_ms += TICK_MS
        remaining = max(0, self.duration_ms - self.elapsed_ms)

        progress = int((remaining / self.duration_ms) * 1000)
        self.progress.setValue(progress)

        if remaining <= 0:
            self.close()

    # ---------------- CLOSE ----------------
    def close(self):
        if self.timer:
            self.timer.stop()
        self.on_close(self)
        super().close()

    # ---------------- LAYOUT ----------------
    def resizeEvent(self, event):
        self.container.setGeometry(0, 0, self.width(), self.height())

        self.title_label.setGeometry(
            PADDING,
            PADDING,
            self.width() - 2 * PADDING - 30,
            30
        )

        self.content_label.setGeometry(
            PADDING,
            PADDING + 35,
            self.width() - 2 * PADDING - 30,
            30
        )

        self.close_button.setGeometry(
            self.width() - PADDING - 24,
            (self.height() - 24) // 2,
            24,
            24
        )

        self.progress.setGeometry(
            PADDING,
            self.height() - PROGRESS_HEIGHT - 6,
            self.width() - 2 * PADDING,
            PROGRESS_HEIGHT
        )

        super().resizeEvent(event)

    # ---------------- POSITIONING ----------------
    def update_position(self, number_before=0):
        screen = QtWidgets.QApplication.primaryScreen()
        geometry = screen.availableGeometry()

        margin = 2
        x = geometry.right() - WINDOW_WIDTH - margin
        y = geometry.top() + margin + number_before * (WINDOW_HEIGHT + WINDOW_GAP)

        self.move(x, y)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    w1 = QtNotification(
        "possible missed chord",
        "[th, t`] = than",
        duration_ms=4000
    )
    w1.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    w1.update_position(0)
    w1.show()

    w2 = QtNotification(
        "possible missed chord",
        "[to] = to",
        duration_ms=7000
    )
    w2.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    w2.update_position(1)
    w2.show()

    sys.exit(app.exec())
