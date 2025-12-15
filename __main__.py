import sys
import signal
import config
import subprocess
import queue
from my_key_event import MyKeyEvent, TERMINATE_EVENT

import threading

# Start the subprocess
# `text=True` gives you strings instead of bytes
# `bufsize=1` + `universal_newlines=True` ensures line-buffered reading
proc = subprocess.Popen(
    ["sudo", "python", "-u", "key_board_process.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

key_queue = queue.Queue()

proc_keyreader_needed = True


def read_keys_linux():
    for line in proc.stdout:
        key_queue.put_nowait(MyKeyEvent(*line.strip().split(" ")))


key_reader = threading.Thread(target=read_keys_linux)
key_reader.start()


def kill_key_reader():
    if proc:
        proc.terminate()
    key_queue.put_nowait(TERMINATE_EVENT)
    key_reader.join()


if config.qt_mode:

    from PySide6 import QtWidgets, QtCore
    from qt_notification_manager import QTNotificationManager
    from qt_bridge import bridge
    from worker import MainWorker

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    sigint_timer = QtCore.QTimer()
    sigint_timer.start(100)
    sigint_timer.timeout.connect(lambda: None)
    worker = MainWorker(key_queue)

    def handle_sigint(sig, frame):
        kill_key_reader()
        worker.wait()
        app.quit()

    signal.signal(signal.SIGINT, handle_sigint)

    manager = QTNotificationManager()
    bridge.notify.connect(manager.send_notification)

    worker.start()

    sys.exit(app.exec())

else:
    from key_event_loop import key_loop

    try:
        key_loop(key_queue)
    except KeyboardInterrupt:
        kill_key_reader()
