from PyQt6.QtWidgets import QLineEdit, QApplication, QMessageBox
from PyQt6.QtCore import QTimer

from num2words import num2words  # type: ignore

from constants import Const as C


def filter_rubles(input_str: str) -> str:
    """
    Очищает строку от лишних символов (пробелы, апострофы и т.д.).

     Args:
         input_str (str): Исходная строка.

     Returns:
         str: Очищенная строка.
    """
    excess_characters = C.EXCESS_CHARACTERS
    for character in excess_characters:
        input_str = input_str.replace(character, "")
    return input_str


def put_line_input(line_edit: QLineEdit, rubles: float) -> None:
    """
    Выводит в виджет жирным шрифтом отформатированную сумму
    Args:
        line_edit (QLineEdit): Виджет ввода суммы
        rubles (float): сумма

    Returns: None
    """
    line_edit.setText(amount_format(rubles))
    set_bold_font(line_edit)


def parse_rubles(rubles_str: str) -> float | None:
    """
    Преобразует сумму в рублях (str) в вещественное число.

    Args:
        rubles_str (str): Строка, содержащая сумму в рублях. В строке возможны "лишние" символы: пробелы и апострофы

    Returns:
        float: Сумма в рублях (float), округлённая до 2 десятичных знаков.
               Возвращает None, если ввод некорректен.
    """
    # Очищаем строку от нежелательных символов
    cleaned_str = filter_rubles(rubles_str)

    try:
        # Преобразуем очищенную строку в число с плавающей точкой, округляем до двух десятичных знаков
        return round(float(cleaned_str), 2) if cleaned_str else 0.00
    except ValueError:
        msg_box_text = C.TEXT_ERROR_PRG
        msg_box_text += f"{rubles_str=} {cleaned_str=}"
        msg_box = QMessageBox()
        msg_box.setText(msg_box_text)
        msg_box.exec()
        return None


def amount_to_words(amount: float) -> str:
    """
    Преобразует сумму в текстовое представление на русском языке с правильным склонением слова "рубль".

    Args:
        amount (float): Сумма денег, которую нужно преобразовать в слова.

    Returns:
        str: Строковое представление суммы с рублями и копейками.
    """

    # Получаем целую часть суммы (рубли)
    rubles = int(amount)
    # Получаем дробную часть суммы (копейки), округляя до ближайшего целого
    kopecks = round((amount - rubles) * 100)

    # Преобразуем рубли в слова и делаем первую букву заглавной
    rubles_word = num2words(rubles, lang=C.LANG).capitalize()

    # Определяем одну и две последние цифры рублей для правильного склонения
    rubles_positif = abs(rubles)
    last_digit = rubles_positif % 10
    last_two_digits = rubles_positif % 100

    # Базовое слово - "рублей"
    ruble_declension = C.FORMS_RUBLE.genitive_plural

    # Проверка на исключения для правильного склонения
    if not (11 <= last_two_digits <= 14):
        if last_digit == 1:
            ruble_declension = C.FORMS_RUBLE.nominative
        elif 2 <= last_digit <= 4:
            ruble_declension = C.FORMS_RUBLE.genitive

    # Формируем итоговую строку, добавляя ведущие нули к копейкам при необходимости
    return f"{rubles_word} {ruble_declension} {kopecks:02} {C.TEXT_KOP}."


def show_amount(amount: float) -> str:
    """
    Формирует строку, состоящую из цифрового и текстового представления суммы в рублях и копейках.

    Args:
        amount (float): Сумма денег, которую нужно отобразить.

    Returns:
        str: Строковое представление суммы в цифрах и в рублях и копейках.
    """
    return f"{amount_format(amount)} {C.TEXT_RUB}. ({amount_to_words(amount)})"


def amount_format(amount: float) -> str:
    return f"{amount:.2f}"


# noinspection PyPep8Naming
def extract_NDS(amount: float, percent_NDS: float) -> float:
    """
    Вычленяет НДС из суммы.

    Формула: НДС = сумма * процент / (100 + процент)

    Args:
        amount (float): Исходная сумма.
        percent_NDS (float): процент НДС

    Returns:
        float: Вычлененная сумма НДС.
    """
    return amount * percent_NDS / (100 + percent_NDS)


# noinspection PyPep8Naming
def display_amount(
    r_edit_line: QLineEdit, amount: float, NDS_including: bool, percent_NDS: float
) -> None:
    """
    Устанавливает текст в r_edit_line, устанавливает позицию курсора для более читабельного отображения информации.

    Args:
        r_edit_line (QLineEdit): Поле для отображения суммы
        amount (float): Сумма денег.
        NDS_including (bool): Признак того, что в сумму входит НДС
        percent_NDS (float) : процент НДС
    """

    r_edit_line.setText(format_summa_and_NDS(amount, NDS_including, percent_NDS))
    cursor_to_beginning(r_edit_line)


# noinspection PyPep8Naming
def format_summa_and_NDS(amount: float, NDS_including: bool, percent_NDS: float) -> str:
    """
    Форматирует текст суммы и НДС.

    Args:
        amount (float): Сумма денег.
        NDS_including (bool): Признак того, что в сумму входит НДС
        percent_NDS (float) : процент НДС

    Returns:
        Отформатированный текст
    """
    return f"{show_amount(amount)}" + (
        f", {C.TEXT_INCLUDING_NDS} {show_amount(extract_NDS(amount, percent_NDS))}"
        if NDS_including
        else ""
    )


def cursor_to_beginning(r_edit_line: QLineEdit) -> None:
    """Устанавливает курсор в начало поля - для того, что бы текст в любом случае отображается с начала"""
    r_edit_line.setCursorPosition(0)


def put_clipboard(widget: QLineEdit) -> None:
    """
    Копирует текст из widget в буфер обмена и отображает сообщение о копировании.

    Args:
        widget (QLineEdit): Поле, текст из которого будет скопирован.
    """
    clipboard = QApplication.clipboard()  # Получение доступа к буферу обмена
    if clipboard and widget.text():
        clipboard.setText(widget.text())  # Запись текста в буфер обмена
        show_message(
            C.TEXT_WRITTEN_IN_CLIPBOARD, C.TIME_TO_SHOW_SUCCESS_MS
        )  # Сообщение о копировании в буфер обмена
    else:
        show_message(
            C.TEXT_NO_WRITTEN_IN_CLIPBOARD, C.TIME_TO_SHOW_FAILURE_MS
        )  # Сообщение о провале копирования в буфер обмена


def show_message(text: str, wait: int) -> None:
    """
    Отображает всплывающее сообщение.
    Сообщение автоматически закрывается через заданное в параметре время.
    Параметры:
    text - текст выводимого сообщения
    wait - максимальное время нахождения сообщения на экране в мс
    """
    # Создаём окно сообщения
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.show()

    # Создаём функцию для закрытия окна
    def close_app() -> None:
        msg_box.deleteLater()

    # Для закрытия окна устанавливаем таймер
    QTimer.singleShot(wait, close_app)


def set_style_input(line_edit: QLineEdit) -> None:
    """
    Устанавливает стиль для поля ввода.

    Args:
        line_edit (QLineEdit): Поле, которое будет стилизовано.
    """
    line_edit.setStyleSheet(C.STYLE_INPUT)


def set_bold_font(line_edit: QLineEdit) -> None:
    """
    Делает шрифт в QLineEdit жирным.

    Args:
        line_edit (QLineEdit): Поле, шрифт которого будет изменён.
    """
    font = line_edit.font()
    font.setBold(True)
    line_edit.setFont(font)
