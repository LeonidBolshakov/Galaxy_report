import re

from PyQt6.QtWidgets import QLineEdit, QApplication, QMessageBox
from PyQt6.QtCore import QTimer

from num2words import num2words

from constants import Const as c


def filter_rubles(input_str: str) -> str:
    """
    Удаляет все символы, кроме цифр и точки, из входной строки.

    Args:
        input_str (str): Исходная строка.

    Returns:
        str: Очищенная строка.
    """
    return re.sub(r"[^\d.]", "", input_str)


def handle_input(line_edit: QLineEdit) -> float:
    """
    Обрабатывает ввод пользователя из QLineEdit, преобразует его в число с двумя десятичными знаками
    и устанавливает текст в поле ввода с применением жирного шрифта.

    Args:
        line_edit (QLineEdit): Поле ввода, содержащее строку для обработки.

    Returns:
        float: Очищенная и преобразованная сумма в рублях.
    """
    rubles = parse_rubles(line_edit.text())
    line_edit.setText(f"{rubles:.2f}")
    set_bold_font(line_edit)
    return rubles


def parse_rubles(rubles_str: str) -> float:
    """
    Преобразует строковое представление суммы в рублях в число с двумя десятичными знаками.

    Args:
        rubles_str (str): Строка, содержащая сумму в рублях.

    Returns:
        float: Сумма в рублях как число float с двумя десятичными знаками.
               Возвращает 0.0, если ввод некорректен.
    """
    # Очищаем строку от нежелательных символов
    cleaned_str = filter_rubles(rubles_str)

    try:
        # Преобразуем очищенную строку в число с плавающей точкой
        rubles_amount = float(cleaned_str)
        # Округляем до двух десятичных знаков
        return round(rubles_amount, 2)
    except ValueError:
        # Возвращаем 0.0, если преобразование не удалось
        return 0.0


def amount_to_words(amount: float) -> str:
    """
    Преобразует числовую сумму в строковое представление на русском языке с правильным склонением "рубль".

    Args:
        amount (float): Сумма денег, которую нужно преобразовать в слова.

    Returns:
        str: Строковое представление суммы с рублями и копейками.
    """
    # Округляем сумму до копеек
    amount = round(amount, 2)
    # Получаем целую часть суммы (рубли)
    rubles = int(amount)
    # Получаем дробную часть суммы (копейки), округляя до ближайшего целого
    kopecks = round((amount - rubles) * 100)

    # Преобразуем целую часть в слова и делаем первую букву заглавной
    rubles_word = num2words(rubles, lang="ru").capitalize()

    # Определяем одну и две последние цифры рублей для правильного склонения
    last_digit = rubles % 10
    last_two_digits = rubles % 100

    # Базовое слово "рублей"
    ruble_declension = "рублей"

    # Проверка на исключения для правильного склонения
    if not (11 <= last_two_digits <= 14):
        if last_digit == 1:
            ruble_declension = "рубль"
        elif 2 <= last_digit <= 4:
            ruble_declension = "рубля"

    # Формируем итоговую строку, добавляя ведущие нули к копейкам при необходимости
    return f"{rubles_word} {ruble_declension} {kopecks:02} коп."


def show_amount(amount: float) -> str:
    """
    Формирует строку, состоящую из цифрового и текстового представления суммы в рублях и копейках.

    Args:
        amount (float): Сумма денег, которую нужно отобразить.

    Returns:
        str: Строковое представление суммы в цифрах и в рублях и копейках.
    """
    return f"{amount:.2f} руб. ({amount_to_words(amount)})"


def compute_and_display(self):
    """
    Выполняет вычисления и обновляет отображение значений в интерфейсе.

    Вызывает функции compute для расчётов, analysis_compute для анализа результатов и display для
    обновления интерфейса пользователя.
    """
    compute(self)
    analysis_compute(self)
    display(self)


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
    self.NDS_paid = round(extract_NDS(self.paid, self.percent_factor_NDS), 2)
    self.corp = round(self.clients * c.PERCENT_CORP / 100, 2)
    self.NDS_corp = round(self.corp * self.percent_factor_NDS, 2)
    self.total_corp = round(self.corp + self.NDS_corp, 2)
    self.left = round(self.total_corp - self.paid, 2)
    self.NDS_left = round(extract_NDS(self.left, self.percent_factor_NDS), 2)


def extract_NDS(amount: float, percent_factor_NDS: float) -> float:
    """
    Вычисляет сумму НДС для указанной суммы.

    Формула: НДС = сумма * процент / (1 + процент)

    Args:
        amount (float): Исходная сумма.
        percent_factor_NDS (float): процент НДС / 100

    Returns:
        float: Вычисленная сумма НДС.
    """
    return amount * percent_factor_NDS / (1 + percent_factor_NDS)


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
    display_amount(self.rEditClients, self.clients)
    display_amount(self.rEditCorp, self.total_corp, self.NDS_corp)
    display_amount(self.rEditPaid, self.paid, self.NDS_paid)
    display_amount(self.rEditLeft, self.left, self.NDS_left)
    display_amount(self.rEditOver, self.over, self.NDS_over)


def display_amount(r_edit_line: QLineEdit, amount: float, NDS: float = 0.0):
    """
    Устанавливает текст в QLineEdit с форматированным отображением суммы и НДС.

    Args:
        r_edit_line (QLineEdit): Поле для отображения суммы.
        amount (float): Сумма денег.
        NDS (float, optional): Сумма НДС. По умолчанию 0.0.
    """
    r_edit_line.setText(
        f"{show_amount(amount)}"
        + (f", в т.ч. НДС {show_amount(NDS)}" if NDS != 0.0 else "")
    )


def set_clipboard(widget: QLineEdit):
    """
    Копирует текст из QLineEdit в буфер обмена и отображает сообщение о копировании.

    Args:
        widget (QLineEdit): Поле, текст из которого будет скопирован.
    """
    clipboard = QApplication.clipboard()  # Получение доступа к буферу обмена
    clipboard.setText(widget.text())  # Запись текста в буфер обмена
    show_message()  # Сообщение о том, что текст скопирован в буфер обмена


def show_message():
    """
    Отображает всплывающее сообщение о том, что текст скопирован в буфер обмена.
    Сообщение автоматически закрывается через заданное время.
    """
    # Создаём окно сообщения
    msg_box = QMessageBox()
    msg_box.setText(c.MESSAGE_TEXT)
    msg_box.show()

    # Создаём функцию для закрытия окна
    def close_app():
        msg_box.close()

    # Устанавливаем таймер на определённое время для закрытия окна
    QTimer.singleShot(c.WINDOW_LIFETIME_MS, close_app)


def set_style(line_edit: QLineEdit):
    """
    Устанавливает стилизацию для QLineEdit через setStyleSheet.

    Args:
        line_edit (QLineEdit): Поле, которое будет стилизовано.
    """
    line_edit.setStyleSheet(c.SET_STYLES)


def set_bold_font(line_edit: QLineEdit):
    """
    Делает шрифт в QLineEdit жирным.

    Args:
        line_edit (QLineEdit): Поле, шрифт которого будет изменён.
    """
    font = line_edit.font()
    font.setBold(True)
    line_edit.setFont(font)
