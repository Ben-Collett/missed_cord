from PySide6 import QtCore
from utils import ValueWrapper


class MainWorker(QtCore.QThread):
    def __init__(self, key_itr):
        super().__init__()
        self.key_itr = key_itr
        self.running = ValueWrapper(True)

    def run(self):
        import key_event_loop
        # pass selfso it will test if running
        key_event_loop.key_loop(self.key_itr, running_flag=self.running)

    def stop(self):
        self.running.value = False
