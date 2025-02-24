class Const(frozenset):
    MESSAGE_TEXT = "Текст скопирован в буфер обмена"
    NAME_UI = "_internal\\report.ui"  # Имя файла интерфейса UI
    PERCENT_CORP = 50  # Процент отчисления корпорации
    PERCENT_NDS = 5.0  # Процент НДС
    WINDOW_LIFETIME_MS = 1000  # Время отображения окна сообщения в миллисекундах
    SET_STYLES = """
            background-color: #edfffb; /* Цвет фона */
            color: #0000ff;            /* Цвет текста */
        """  # Стилизация для QLineEdit
