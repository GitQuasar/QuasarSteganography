from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QLabel,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from Models.mdl_encrypt import ImageEncryptor


class EncryptWidget(QWidget):
    """
    GUI for image encryption.

    Args:
        QWidget: Base widget class that provides properties and methods for creating GUI elements
    """

    def __init__(self):
        super().__init__()

        self.lyt_base = QVBoxLayout()

        self.wgt_user_message = QLineEdit()
        self.wgt_user_message.setPlaceholderText("Enter message to encrypt")

        self.wgt_path_form = QLineEdit()
        self.wgt_path_form.setPlaceholderText("Choose the image")
        self.wgt_path_form.setReadOnly(True)

        self.lyt_browse_form = QHBoxLayout()

        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.slot_image_browse)

        self.lyt_browse_form.addWidget(self.wgt_path_form, stretch=4)
        self.lyt_browse_form.addWidget(self.btn_browse, stretch=1)

        self.lyt_bottom_buttons = QHBoxLayout()

        self.btn_encrypt = QPushButton("Encrypt")
        self.btn_encrypt.clicked.connect(self.slot_encrypt)

        self.lyt_bottom_buttons.addWidget(self.btn_encrypt, stretch=1)

        self.wgt_image_preview = QLabel()

        self.lyt_base.addLayout(self.lyt_browse_form, stretch=1)
        self.lyt_base.addWidget(self.wgt_user_message, stretch=1)
        self.lyt_base.addWidget(
            self.wgt_image_preview, stretch=3, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.lyt_base.addLayout(self.lyt_bottom_buttons, stretch=1)

        self.setLayout(self.lyt_base)

    def slot_image_browse(self):
        path_image = Path(
            QFileDialog.getOpenFileName(
                self, "Image to encrypt...", filter="Images (*.png *.jpg)"
            )[0]
        ).resolve()

        if path_image.is_dir():
            return

        pxm_image = QPixmap(str(path_image))

        if pxm_image.isNull():
            msgBox = QMessageBox()
            msgBox.setText("Image is corrupted, therefore cannot be opened correctly")
            msgBox.Icon(QMessageBox.Icon.NoIcon)
            msgBox.exec()
            return

        self.wgt_path_form.setText(str(path_image))
        pxm_image = pxm_image.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
        self.wgt_image_preview.setPixmap(pxm_image)

    def slot_encrypt(self):
        msgBox = QMessageBox()
        if self.wgt_image_preview.pixmap().isNull():
            msgBox.setText("Image hasn't been chosen")

        elif self.wgt_user_message.text() == "":
            msgBox.setText("Message hasn't been entered")

        else:
            image_encryptor = ImageEncryptor()
            path_saved: str = str(
                image_encryptor.encrypt(
                    self.wgt_user_message.text(), Path(self.wgt_path_form.text())
                )
            )
            msgBox = QMessageBox()
            msgBox.setText(f"The image has been saved in\n{path_saved}")

        msgBox.Icon(QMessageBox.Icon.NoIcon)
        msgBox.exec()
