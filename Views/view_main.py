from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QStackedLayout,
    QToolBar,
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize

from .view_encrypt import EncryptWidget
from .view_decrypt import DecryptWidget


class MainWindow(QMainWindow):
    """
    Entry GUI point for application.

    Args:
        QMainWindow: Provides main application window
    """

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 400)
        self.setMinimumSize(800, 400)
        self.setObjectName("MainWindow")
        self.setCentralWidget(QWidget())

        lyt_base = QHBoxLayout()
        self.centralWidget().setLayout(lyt_base)

        self.lyt_stack = QStackedLayout()
        self.lyt_stack.addWidget(EncryptWidget())
        self.lyt_stack.addWidget(DecryptWidget())
        lyt_base.addLayout(self.lyt_stack)

        self.wgt_toolbar = QToolBar(self)
        self.wgt_toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.wgt_toolbar)

        act_encrypt = QAction(
            QIcon(
                str(
                    Path(__file__).parent.parent
                    / "Assets"
                    / "Icons"
                    / "EncryptIcon.png"
                )
            ),
            "Encrypt",
            self.wgt_toolbar,
        )
        act_decrypt = QAction(
            QIcon(
                str(
                    Path(__file__).parent.parent
                    / "Assets"
                    / "Icons"
                    / "DecryptIcon.png"
                )
            ),
            "Decrypt",
            self.wgt_toolbar,
        )

        act_encrypt.triggered.connect(self.slot_encrypt)
        act_decrypt.triggered.connect(self.slot_decrypt)
        self.wgt_toolbar.addAction(act_encrypt)
        self.wgt_toolbar.addSeparator()
        self.wgt_toolbar.addAction(act_decrypt)
        self.wgt_toolbar.setIconSize(QSize(48, 48))

    def slot_encrypt(self):
        self.lyt_stack.setCurrentIndex(0)

    def slot_decrypt(self):
        self.lyt_stack.setCurrentIndex(1)
