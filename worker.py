from PySide6 import QtCore


class MainWorker(QtCore.QThread):
    def __init__(self, key_itr):
        super().__init__()
        self.key_itr = key_itr

    def run(self):
        import key_event_loop
        key_event_loop.key_loop(self.key_itr)

    def stop(self):
        self.running.value = False
