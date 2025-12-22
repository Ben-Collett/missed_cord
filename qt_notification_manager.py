from PySide6 import QtWidgets
from qt_notification import QtNotification
from config import current_config


def duration_ms():
    return current_config.duration.milliseconds


def max_notifications():
    return current_config.max_qt_notifications


class QTNotificationManager:
    def __init__(self):
        self.notifications: list[QtNotification] = []

    def remove_window(self, window: QtNotification):
        self.notifications.remove(window)
        self.update_positions()

    def update_positions(self):
        for i, window in enumerate(self.notifications):
            number_before = len(self.notifications) - i - 1
            window.update_position(number_before)

    def send_notification(self, title, content):
        widget = QtNotification(
            title, content, self.remove_window, duration_ms=duration_ms())
        self.notifications.append(widget)

        while len(self.notifications) > max_notifications():
            # automatically gets removed from the list on close
            self.notifications[0].close()
        self.update_positions()

        widget.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    # app.setQuitOnLastWindowClosed(False)
    manager = QTNotificationManager()
    manager.send_notification("hello", "there")
    manager.send_notification("general", "konobi")
    app.exec()
