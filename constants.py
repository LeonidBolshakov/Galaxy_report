from typing import NamedTuple


class FormsWord(NamedTuple):
    genitive_plural: str
    nominative: str
    genitive: str


class Const(frozenset):
    # Класс-контейнер для констант. Наследуется от frozenset для неизменяемости.
    NAME_UI = "_internal\\report.ui"  # Путь к файлу UI, сформированному Qt Designer
    PERCENT_CORP = 50.0  # Процент отчислений корпорации
    PERCENT_NDS = 20.0  # Процент НДС, заданный по умолчанию.
    TIME_TO_SHOW_SUCCESS_MS = 1000  # Время показа успешного уведомления (мс)
    TIME_TO_SHOW_FAILURE_MS = 5000  # Время показа уведомления об ошибке (мс)
    STYLE_INPUT = """
            background-color: #aaffff; /* Цвет фона */
            color: #0000ff;            /* Цвет текста */
        """  # Стиль для полей ввода (CSS)
    STYLE_ERROR = "background-color: #ffe6e6;"  # Стиль дл ошибочных данных
    # Регулярное выражение для контроля ввода плавающих чисел:
    # - Пробелы в начале и конце выражения допустимы
    # - Целая часть: цифры, апострофы и пробелы
    # - Дробная часть: точка и цифры (опционально)
    RE_INPUT_DOUBLE = r"^\s*\d+(?:['\s]\d+)*(?:\.\d+)?\s*$"
    EXCESS_CHARACTERS = (
        " ",
        "'",
        "\n",
        "`",
        "’",
    )  # Символы для удаления из введённой строки
    LANG = "ru"  # Обозначение языка вывода
    FORMS_RUBLE = FormsWord(
        genitive_plural="рублей", nominative="рубль", genitive="рубля"
    )  # Склонения слова "рубль"
    TEXT_KOP = "коп"  # Сокращение для слова копеек
    TEXT_RUB = "руб"  # Сокращение для слова рублей
    TEXT_INCLUDING_NDS = "включая НДС"
    TEXT_WRITTEN_IN_CLIPBOARD = "Текст скопирован в буфер обмена"
    TEXT_NO_WRITTEN_IN_CLIPBOARD = "Текст НЕ СКОПИРОВАН в буфер обмена"
    TEXT_ERROR_PRG = (
        f"Ошибка в программе. Модуль {__file__}.\n"
        + "Функция 'parse_rubles'.\nОтладочная информация:\n"
        + "Данные прошли валидацию, но не преобразуются во float\n"
    )
