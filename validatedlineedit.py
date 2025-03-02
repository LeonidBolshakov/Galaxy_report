from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

from constants import Const as C


class ValidatedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setValidator(
            QRegularExpressionValidator(QRegularExpression(C.RE_INPUT_DOUBLE))
        )

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.hasAcceptableInput():
            self.setStyleSheet(C.STYLE_ERROR)
        else:
            self.setStyleSheet("")
