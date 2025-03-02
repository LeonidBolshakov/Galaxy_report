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


def handle_input(line_edit: QLineEdit) -> float:
    """
    Обрабатывает ввод: преобразует его в число с двумя десятичными знаками,
    делает шрифт жирным.
    Устанавливает текст в поле ввода.

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
               Возвращает -999999999.99, если ввод некорректен.
    """
    # Очищаем строку от нежелательных символов
    cleaned_str = filter_rubles(rubles_str)

    try:
        # Преобразуем очищенную строку в число с плавающей точкой, округляем до двух десятичных знаков
        return round(float(cleaned_str), 2)
    except ValueError:
        return -999999999.99


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
    ruble_declension = C.FORMS_RUBLE[0]

    # Проверка на исключения для правильного склонения
    if not (11 <= last_two_digits <= 14):
        if last_digit == 1:
            ruble_declension = C.FORMS_RUBLE[1]
        elif 2 <= last_digit <= 4:
            ruble_declension = C.FORMS_RUBLE[2]

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
    return f"{amount:.2f} {C.TEXT_RUB}. ({amount_to_words(amount)})"


# noinspection PyPep8Naming
def extract_NDS(amount: float, percent_factor_NDS: float) -> float:
    """
    Вычленяет сумму НДС для указанной суммы.

    Формула: НДС = сумма * процент / (100 + процент)

    Args:
        amount (float): Исходная сумма.
        percent_factor_NDS (float): процент НДС / 100

    Returns:
        float: Вычлененная сумма НДС.
    """
    return amount * percent_factor_NDS / (1 + percent_factor_NDS)


# noinspection PyPep8Naming
def display_amount(r_edit_line: QLineEdit, amount: float, NDS: float = 0.0):
    """
    Устанавливает текст в r_edit_line с форматированным отображением суммы и НДС.
    Устанавливает курсор в начало текста

    Args:
        r_edit_line (QLineEdit): Поле для отображения суммы.
        amount (float): Сумма денег.
        NDS (float, optional): Сумма НДС. По умолчанию 0.0.
    """
    r_edit_line.setText(
        f"{show_amount(amount)}"
        + (f", {C.TEXT_INCLUDING_NDS} {show_amount(NDS)}" if NDS != 0.0 else "")
    )
    r_edit_line.setCursorPosition(0)


def put_clipboard(widget: QLineEdit):
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
    Отображает всплывающее сообщение о том, что текст скопирован в буфер обмена.
    Сообщение автоматически закрывается через заданное время.
    Параметры:
    text - текст выводимого сообщения
    wait - максимальное время нахождения сообщения на экране в мс
    """
    # Создаём окно сообщения
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.show()

    # Создаём функцию для закрытия окна
    def close_app():
        msg_box.close()

    # Устанавливаем таймер на определённое время для закрытия окна
    QTimer.singleShot(wait, close_app)


def set_style_input(line_edit: QLineEdit):
    """
    Устанавливает стилизацию для QLineEdit через setStyleSheet.

    Args:
        line_edit (QLineEdit): Поле, которое будет стилизовано.
    """
    line_edit.setStyleSheet(C.STYLE_INPUT)


def set_bold_font(line_edit: QLineEdit):
    """
    Делает шрифт в QLineEdit жирным.

    Args:
        line_edit (QLineEdit): Поле, шрифт которого будет изменён.
    """
    font = line_edit.font()
    font.setBold(True)
    line_edit.setFont(font)
