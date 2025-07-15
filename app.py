import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from Views.view_main import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv + ["-platform", "windows:darkmode=2"])
    app.setStyle("Fusion")
    app.setApplicationName("GUI Steganografy")
    app.setWindowIcon(
        QIcon(str(Path(__file__).parent / "Assets" / "Icons" / "QuasarIcon.png"))
    )

    with open(str(Path(__file__).parent / "Styles" / "Styles.qss"), "r") as f:
        app.setStyleSheet(f.read())

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
