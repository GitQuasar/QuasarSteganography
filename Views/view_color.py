from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QColor


class ColorWidget(QWidget):
    """
    ColorWidget view.

    A dummy widget. Use it to debug your layout rendering.
    """

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
