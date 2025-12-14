from PySide6 import QtCore


class NotificationBridge(QtCore.QObject):
    notify = QtCore.Signal(str, str)


bridge = NotificationBridge()
