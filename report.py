import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QApplication
from PyQt6 import QtCore

import functions as f
from constants import Const as C
from validatedlineedit import ValidatedLineEdit


class Report(QMainWindow):
    EditClients: ValidatedLineEdit
    EditPaid_1: ValidatedLineEdit
    EditPaid_2: ValidatedLineEdit
    EditPaid_3: ValidatedLineEdit
    EditPercent_NDS: ValidatedLineEdit
    rEditClients: QLineEdit
    rEditCorpNDS: QLineEdit
    rEditCorp: QLineEdit
    rEditLeft: QLineEdit
    rEditOver: QLineEdit
    rEditPaid: QLineEdit

    def __init__(self) -> None:
        """Инициализация UI, атрибутов и подключение сигналов."""
        super().__init__()
        self.init_UI()  # Инициализация атрибутов UI

        # Атрибуты хранят финансовые данные
        self.clients = 0.0  # Заплачено клиентами
        self.corp = 0.0  # Подлежит перечислению в корпорацию
        self.total_corp = 0.0  # В корпорацию, включая НДС
        self.NDS_corp = 0.0  # В том числе НДС в корпорацию
        self.left = 0.0  # Осталось заплатить
        self.NDS_left = 0.0  # Осталось заплатить НДС
        self.over = 0.0  # Переплачено
        self.NDS_over = 0.0  # Переплачено
        self.paid = 0.0  # Заплачено
        self.paid_1 = 0.0  # Первый платёж
        self.paid_2 = 0.0  # Второй платёж
        self.paid_3 = 0.0  # Третий платёж
        self.NDS_paid = 0.0  # НДС заплачено
        self.percent_factor_NDS = (
            C.PERCENT_NDS / 100
        )  # Процент НДС, переведённый в коэффициент (поделённый на 100)
        self.fields_output = (
            self.rEditClients,
            self.rEditCorpNDS,
            self.rEditCorp,
            self.rEditLeft,
            self.rEditOver,
            self.rEditPaid,
        )

        self.setup_connections()  # Установка соединений сигналов и слотов
        self.set_event_filters()  # Установка фильтров событий (кликанье мышкой) для полей ввода
        self.set_custom_interface()  # установка внешнего вида интерфейса

    def init_UI(self):
        """Загрузка UI и переменных в объект класса"""

        exe_directory = (  # Директория, из которой был запущен файл
            Path(sys.argv[0]).parent
            if hasattr(sys, "frozen")  # exe файл, получен с помощью PyInstaller
            else Path(__file__).parent  # Если файл запущен как обычный Python-скрипт
        )

        ui_config_abs_path = exe_directory / C.NAME_UI
        uic.loadUi(ui_config_abs_path, self)

    def setup_connections(self):
        """Подключает сигналы редактирования полей к обработчикам."""
        self.EditClients.editingFinished.connect(self.on_editing_finished_clients)
        self.EditPaid_1.editingFinished.connect(self.on_editing_finished_paid_1)
        self.EditPaid_2.editingFinished.connect(self.on_editing_finished_paid_2)
        self.EditPaid_3.editingFinished.connect(self.on_editing_finished_paid_3)
        self.EditPercent_NDS.editingFinished.connect(self.on_editing_finished_percent)
        # Всегда устанавливаем курсор в начало поля вывода

    def set_event_filters(self):
        """Инициирует обработку кликов по полям вывода для копирования в буфер обмена."""
        for field in self.fields_output:
            field.installEventFilter(self)

    def eventFilter(self, source, event):
        """Проверяет, был ли клик мыши. Если был, копирует текст поля в буфер обмена"""
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            f.put_clipboard(source)
        return super().eventFilter(source, event)

    def set_custom_interface(self):
        """Персонализирует интерфейс"""
        self.set_style_input()
        self.EditPercent_NDS.setText(f"{C.PERCENT_NDS}")

    def on_editing_finished_clients(self):
        self.clients = f.handle_input(self.EditClients)
        self.compute_and_display()

    def on_editing_finished_paid_1(self):
        self.paid_1 = f.handle_input(self.EditPaid_1)
        self.compute_and_display()

    def on_editing_finished_paid_2(self):
        self.paid_2 = f.handle_input(self.EditPaid_2)
        self.compute_and_display()

    def on_editing_finished_paid_3(self):
        self.paid_3 = f.handle_input(self.EditPaid_3)
        self.compute_and_display()

    def on_editing_finished_percent(self):
        self.percent_factor_NDS = f.handle_input(self.EditPercent_NDS) / 100
        self.compute_and_display()

    def set_style_input(self) -> None:
        """
        Устанавливает стили для полей ввода информации
        Returns: None
        """

        input_line_edits = (
            self.EditClients,
            self.EditPaid_1,
            self.EditPaid_2,
            self.EditPaid_3,
            self.EditPercent_NDS,
        )
        for line_edit in input_line_edits:
            f.set_style_input(line_edit)

    def compute_and_display(self):
        """
        Выполняет вычисления и обновляет отображение значений в интерфейсе.

        Вызывает функции compute для расчётов, analysis_compute для анализа результатов и display для
        обновления интерфейса пользователя.
        """
        self.compute()
        self.analysis_compute()
        self.display()

    def compute(self):
        """
        Вычисляет основные финансовые показатели на основе введенных данных:
        - Общая сумма платежей.
        - НДС платежей.
        - Сумма для корпорации без НДС.
        - НДС от суммы для корпорации.
        - Сумма с НДС для корпорации.
        - Остаток платежей.
        - НДС на остаток.
        """
        self.paid = round(self.paid_1 + self.paid_2 + self.paid_3, 2)
        self.NDS_paid = round(f.extract_NDS(self.paid, self.percent_factor_NDS), 2)
        self.corp = round(self.clients * C.PERCENT_CORP / 100, 2)
        self.NDS_corp = round(self.corp * self.percent_factor_NDS, 2)
        self.total_corp = round(self.corp + self.NDS_corp, 2)
        self.left = round(self.total_corp - self.paid, 2)
        self.NDS_left = round(f.extract_NDS(self.left, self.percent_factor_NDS), 2)

    def analysis_compute(self):
        """
        Анализирует остаток долга после платежей.

        Если остаток отрицательный, устанавливает переплату и обнуляет остаток и соответствующие НДС.
        """
        if self.left < 0:
            self.over = -self.left
            self.NDS_over = -self.NDS_left
            self.left = 0.0
            self.NDS_left = 0.0
        else:
            self.over = 0.0
            self.NDS_over = 0.0

    def display(self):
        """
        Обновляет отображение всех соответствующих полей в интерфейсе с учетом вычисленных значений.
        """
        f.display_amount(self.rEditClients, self.clients)
        f.display_amount(self.rEditCorp, self.corp)
        f.display_amount(self.rEditCorpNDS, self.total_corp, self.NDS_corp)
        f.display_amount(self.rEditPaid, self.paid, self.NDS_paid)
        f.display_amount(self.rEditLeft, self.left, self.NDS_left)
        f.display_amount(self.rEditOver, self.over, self.NDS_over)


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Report()
    window.show()
    sys.exit(app.exec())
