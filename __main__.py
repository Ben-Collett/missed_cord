import sys
import signal
import config
import subprocess


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

if config.qt_mode:

    from PySide6 import QtWidgets, QtCore
    from qt_notification_manager import QTNotificationManager
    from qt_bridge import bridge
    from worker import MainWorker

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 🔁 Allow SIGINT processing
    sigint_timer = QtCore.QTimer()
    sigint_timer.start(100)
    sigint_timer.timeout.connect(lambda: None)
    worker = MainWorker(proc.stdout)

    def handle_sigint(sig, frame):
        proc.terminate()
        worker.wait()
        app.quit()

    signal.signal(signal.SIGINT, handle_sigint)

    manager = QTNotificationManager()
    bridge.notify.connect(manager.send_notification)

    worker.start()

    sys.exit(app.exec())

else:
    from main import main
    main(proc.stdout)
