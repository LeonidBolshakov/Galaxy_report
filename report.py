import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QApplication
from PyQt6 import QtCore

import functions as f
from constants import Const as c


class Report(QMainWindow):
    EditClients: QLineEdit
    EditPaid_1: QLineEdit
    EditPaid_2: QLineEdit
    EditPaid_3: QLineEdit
    EditPercent_NDS: QLineEdit
    rEditClients: QLineEdit
    rEditCorp: QLineEdit
    rEditLeft: QLineEdit
    rEditOver: QLineEdit
    rEditPaid: QLineEdit

    def __init__(self) -> None:
        """Инициализация приложения"""
        super().__init__()

        # Атрибуты класса
        self.clients = 0.0
        self.corp = 0.0
        self.left = 0.0
        self.NDS_left = 0.0
        self.NDS_over = 0.0
        self.NDS_paid = 0.0
        self.NDS_total = 0.0
        self.over = 0.0
        self.paid = 0.0
        self.paid_1 = 0.0
        self.paid_2 = 0.0
        self.paid_3 = 0.0
        self.percent_factor_NDS = c.PERCENT_NDS / 100
        self.total = 0.0

        self.init_UI()  # Инициализация атрибутов UI
        self.setup_connections()  # Установка соединений сигналов и слотов
        self.set_event_filters()  # Установка фильтров событий для некоторых виджетов
        self.set_custom_interface()  # установка внешнего вида интерфейса

    def init_UI(self):
        """Загрузка UI и переменных в объект класса"""

        exe_directory = (  # Директория, из которой был запущен файл
            Path(sys.argv[0]).parent
            if hasattr(sys, "frozen")  # exe файл, получен с помощью PyInstaller
            else Path(__file__).parent  # Если файл запущен как обычный Python-скрипт
        )

        ui_config_abs_path = exe_directory / c.NAME_UI
        uic.loadUi(ui_config_abs_path, self)

    def setup_connections(self):
        self.EditClients.editingFinished.connect(self.on_editing_finished_clients)
        self.EditPaid_1.editingFinished.connect(self.on_editing_finished_paid_1)
        self.EditPaid_2.editingFinished.connect(self.on_editing_finished_paid_2)
        self.EditPaid_3.editingFinished.connect(self.on_editing_finished_paid_3)
        self.EditPercent_NDS.editingFinished.connect(self.on_editing_finished_percent)

    def set_event_filters(self):
        self.rEditClients.installEventFilter(self)
        self.rEditCorp.installEventFilter(self)
        self.rEditLeft.installEventFilter(self)
        self.rEditOver.installEventFilter(self)
        self.rEditPaid.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            match source:
                case self.rEditClients:
                    f.set_clipboard(self.rEditClients)
                case self.rEditCorp:
                    f.set_clipboard(self.rEditCorp)
                case self.rEditPaid:
                    f.set_clipboard(self.rEditPaid)
                case self.rEditLeft:
                    f.set_clipboard(self.rEditLeft)
                case self.rEditOver:
                    f.set_clipboard(self.rEditOver)

        return super().eventFilter(source, event)

    def set_custom_interface(self):
        self.set_style_input()
        self.EditPercent_NDS.setText(f"{c.PERCENT_NDS}")

    def on_editing_finished_clients(self):
        self.clients = f.handle_input(self.EditClients)
        f.compute_and_display(self)

    def on_editing_finished_paid_1(self):
        self.paid_1 = f.handle_input(self.EditPaid_1)
        f.compute_and_display(self)

    def on_editing_finished_paid_2(self):
        self.paid_2 = f.handle_input(self.EditPaid_2)
        f.compute_and_display(self)

    def on_editing_finished_paid_3(self):
        self.paid_3 = f.handle_input(self.EditPaid_3)
        f.compute_and_display(self)

    def on_editing_finished_percent(self):
        self.percent_factor_NDS = f.handle_input(self.EditPercent_NDS) / 100
        f.compute_and_display(self)

    def set_style_input(self):
        input_line_edits = (
            self.EditClients,
            self.EditPaid_1,
            self.EditPaid_2,
            self.EditPaid_3,
            self.EditPercent_NDS,
        )
        for line_edit in input_line_edits:
            f.set_style(line_edit)


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Report()
    window.show()
    sys.exit(app.exec())
