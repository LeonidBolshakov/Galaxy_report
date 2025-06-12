import sys
from pathlib import Path
import typing

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QApplication
from PyQt6 import QtCore

import functions as f
from constants import Const as C
from validatedlineedit import ValidatedLineEdit


class OutputAN(typing.NamedTuple):
    amount: str  # Сумма
    NDS_including: bool  # Признак. НДС включен в сумму.


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
        self.init_UI()  # Инициализация UI, подготовленного Qt Designer, в том числе установка атрибутов полей

        # Атрибуты хранят финансовые данные
        self.clients = 0.0  # Заплачено клиентами
        self.corp = 0.0  # Подлежит перечислению в корпорацию без НДС
        self.total_corp = 0.0  # В корпорацию, включая НДС
        self.left = 0.0  # Осталось заплатить, включая НДС
        self.over = 0.0  # Переплачено, включая НДС
        self.paid = 0.0  # Заплачено, включая НДС
        self.paid_1 = 0.0  # Первый платёж, включая НДС
        self.paid_2 = 0.0  # Второй платёж, включая НДС
        self.paid_3 = 0.0  # Третий платёж, включая НДС
        self.percent_NDS = (
            C.PERCENT_NDS
        )  # Процент НДС корпорации. C.PERCENT_NDS - значение по умолчанию.
        self.input_line_edits = {  # Словарь свойств виджетов ввода
            self.EditClients: "clients",  # Поле ввода. "Клиенты" - Общая сумма, заплаченная клиентами (без НДС).
            self.EditPaid_1: "paid_1",  # Поле ввода. "Оплачено" - Сумма первого платежа в корпорацию.
            self.EditPaid_2: "paid_2",  # Поле ввода. "Оплачено" - Сумма второго платежа в корпорацию.
            self.EditPaid_3: "paid_3",  # Поле ввода. "Оплачено" - Сумма третьего платежа в корпорацию.
            self.EditPercent_NDS: "percent_NDS",  # Процент НДС, применяемый корпорацией.
        }  # Виджеты для ввода информации
        self.output_line_edit = {  # Словарь свойств виджетов вывода
            # Класс OutputAN - имеет 2 параметра: имя атрибута класса и признак, что НДС входит в сумму.
            # Поступило от клиентов без НДС.
            self.rEditClients: OutputAN(amount="clients", NDS_including=False),
            # Надо перечислить в корпорацию без НДС.
            self.rEditCorp: OutputAN(amount="corp", NDS_including=False),
            # Надо перечислить в корпорацию с НДС.
            self.rEditCorpNDS: OutputAN(amount="total_corp", NDS_including=True),
            self.rEditPaid: OutputAN(
                amount="paid", NDS_including=True
            ),  # Всего заплачено с НДС.
            self.rEditLeft: OutputAN(
                amount="left", NDS_including=True
            ),  # Осталось заплатить с НДС.
            self.rEditOver: OutputAN(
                amount="over", NDS_including=True
            ),  # Переплачено с НДС.
        }  # Виджеты для вывода информации

        self.setup_connections()  # Установка соединений сигналов и слотов
        self.set_event_filters()  # Установка фильтров событий для полей вывода
        self.set_custom_interface()  # Настройка внешнего вида интерфейса

    def init_UI(self) -> None:
        """Загрузка UI и атрибутов полей в объект класса"""

        exe_directory = (  # Директория, из которой была запущена программа
            Path(sys.argv[0]).parent
            if hasattr(sys, "frozen")  # exe файл, получен с помощью PyInstaller
            else Path(__file__).parent  # Если файл запущен как обычный Python-скрипт
        )

        ui_config_abs_path = exe_directory / C.NAME_UI
        uic.loadUi(ui_config_abs_path, self)

    def setup_connections(self) -> None:
        """Для всех полей ввода назначает программу обработки сигнала завершения ввода"""
        for line_edit in self.input_line_edits.keys():
            line_edit.signal_focus_out.connect(self.handler_signal_focus_out)

    def set_event_filters(self) -> None:
        """Для всех полей вывода инициирует обработку кликов по полям."""
        for line_edit in self.output_line_edit.keys():
            line_edit.installEventFilter(self)

    def eventFilter(self, source: QLineEdit, event: QtCore.QEvent) -> bool:
        """Переопределение метода обработки событий фильтра.
        Обрабатывает только клики мыши. Если клик был - копирует текст поля в буфер обмена
        """
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            f.put_clipboard(source)
        return super().eventFilter(source, event)

    def set_custom_interface(self) -> None:
        """Персонализирует интерфейс"""
        self.set_style_inputs()  # Устанавливает стиль для всех полей ввода информации
        self.EditPercent_NDS.setText(
            f"{self.percent_NDS}"
        )  # Устанавливает значение поля по умолчанию

    def set_style_inputs(self) -> None:
        """
        Устанавливает стиль для всех полей ввода информации
        Returns: None
        """

        for line_edit in self.input_line_edits:
            f.set_style_input(line_edit)

    def compute_and_display(self) -> None:
        """
        Выполняет вычисления финансовой информации и обновляет отображение значений в интерфейсе.

        Вызывает функции compute для расчётов, analysis_compute для анализа результатов и
        display для обновления интерфейса пользователя.
        """
        self.compute()
        self.analysis_compute()
        self.display()

    def compute(self) -> None:
        """
        Вычисляет основные финансовые показатели на основе введенных данных:
        - Сумма для корпорации без НДС.
        - Сумма для корпорации с НДС.
        - Общая сумма платежей.
        - Остаток платежей.
        """
        self.corp = round(self.clients * C.PERCENT_CORP / 100, 2)
        # noinspection PyPep8Naming
        NDS_corp = self.corp * self.percent_NDS / 100
        self.total_corp = round(self.corp + NDS_corp, 2)
        self.paid = round(self.paid_1 + self.paid_2 + self.paid_3, 2)
        self.left = round(self.total_corp - self.paid, 2)

    def analysis_compute(self) -> None:
        """
        Анализирует остаток долга после платежей.
        Если остаток отрицательный, устанавливает переплату.
        """
        if self.left < 0:
            self.over = -self.left
            self.left = 0.0
        else:
            self.over = 0.0

    def display(self) -> None:
        """
        Обновляет отображение всех выходных полей в интерфейсе.
        """
        for field in self.output_line_edit:
            f.display_amount(
                field,  # Поле вывода финансового показателя
                # Значение финансового показателя
                getattr(self, self.output_line_edit[field].amount),
                # Признак. В сумму финансового показателя входит НДС.
                self.output_line_edit[field].NDS_including,
                self.percent_NDS,  # Процент НДС
            )

    def handler_signal_focus_out(self, obj: ValidatedLineEdit) -> None:
        """Обработчик сигнала выхода из фокуса поля ввода"""
        input_amount = f.parse_rubles(obj.text())
        setattr(self, self.input_line_edits[obj], input_amount)
        f.put_line_input(obj, input_amount)
        self.compute_and_display()


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Report()
    window.show()
    sys.exit(app.exec())
