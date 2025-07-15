from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QLabel,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from Models.mdl_decrypt import ImageDecryptor


class DecryptWidget(QWidget):
    """
    GUI for image decryption.

    Args:
        QWidget: Base widget class that provides properties and methods for creating GUI elements
    """

    def __init__(self):
        super().__init__()

        self.lyt_base = QVBoxLayout()

        self.wgt_path_form = QLineEdit()
        self.wgt_path_form.setPlaceholderText("Choose the image")
        self.wgt_path_form.setReadOnly(True)

        self.lyt_browse_form = QHBoxLayout()

        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.slot_image_browse)

        self.lyt_browse_form.addWidget(self.wgt_path_form, stretch=4)
        self.lyt_browse_form.addWidget(self.btn_browse, stretch=1)

        self.wgt_key_form = QLineEdit()
        self.wgt_key_form.setPlaceholderText("Decryption key")
        self.wgt_key_form.setEchoMode(QLineEdit.EchoMode.Password)

        self.lyt_decrypt = QHBoxLayout()

        self.wgt_image_preview = QLabel()

        self.lyt_decrypt.addWidget(
            self.wgt_image_preview, stretch=1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.wgt_decrypted_text_form = QTextEdit()
        self.wgt_decrypted_text_form.setPlaceholderText("Decrypted text")
        self.wgt_decrypted_text_form.setReadOnly(True)
        self.lyt_decrypt.addWidget(self.wgt_decrypted_text_form, stretch=1)

        self.lyt_bottom_buttons = QHBoxLayout()

        self.btn_decrypt = QPushButton("Decrypt")
        self.btn_decrypt.clicked.connect(self.slot_decrypt)

        self.lyt_bottom_buttons.addWidget(self.btn_decrypt, stretch=1)

        self.lyt_base.addLayout(self.lyt_browse_form, stretch=1)
        self.lyt_base.addWidget(self.wgt_key_form, stretch=1)
        self.lyt_base.addLayout(self.lyt_decrypt, stretch=3)
        self.lyt_base.addLayout(self.lyt_bottom_buttons, stretch=1)

        self.setLayout(self.lyt_base)

    def slot_image_browse(self):
        path_image = Path(
            QFileDialog.getOpenFileName(
                self, "Image to decrypt...", filter="Images (*.png *.jpg)"
            )[0]
        ).resolve()

        if path_image.is_dir():
            return

        pxm_image = QPixmap(str(path_image))

        if pxm_image.isNull():
            msgBox = QMessageBox()
            msgBox.setText("Image is corrupted, therefore cannot be opened correctly")
            return

        self.wgt_path_form.setText(str(path_image))

        pxm_image = pxm_image.scaled(
            320,
            320,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation,
        )

        self.wgt_image_preview.setPixmap(pxm_image)

    def slot_decrypt(self):
        msgBox = QMessageBox()
        if self.wgt_image_preview.pixmap().isNull():
            msgBox.setText("Image hasn't been chosen")
            msgBox.Icon(QMessageBox.Icon.NoIcon)
            msgBox.exec()
            return

        if self.wgt_key_form.text() == "":
            msgBox.setText("Key hasn't been entered")
            msgBox.Icon(QMessageBox.Icon.NoIcon)
            msgBox.exec()
            return

        image_decryptor = ImageDecryptor()

        self.wgt_decrypted_text_form.setText(
            image_decryptor.decrypt(
                Path(self.wgt_path_form.text()).resolve(), self.wgt_key_form.text()
            )
        )
