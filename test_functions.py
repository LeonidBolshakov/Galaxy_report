import unittest
from unittest.mock import MagicMock, patch
from functions import (
    filter_rubles,
    parse_rubles,
    handle_input,
    amount_to_words,
    extract_NDS,
    show_amount,
)
from constants import Const as c


# Для тестирования функций, зависящих от PyQt6, потребуется настройка среды


class TestFunctions(unittest.TestCase):
    def test_filter_rubles(self):
        # Обычные случаи
        self.assertEqual(filter_rubles("1234.56"), "1234.56")
        self.assertEqual(filter_rubles("1a2b3c4.5d6"), "1234.56")
        self.assertEqual(filter_rubles("рубли 1000.00"), "1000.00")

        # Пустая строка
        self.assertEqual(filter_rubles(""), "")

        # Только нежелательные символы
        self.assertEqual(filter_rubles("abc!@#"), "")

        # Несколько точек
        self.assertEqual(filter_rubles("12.34.56"), "0.00")

    def test_parse_rubles(self):
        # Корректные числовые строки
        self.assertEqual(parse_rubles("1234.56"), 1234.56)
        self.assertEqual(
            parse_rubles("1,234.56"), 1234.56
        )  # Запятая не удаляется, так как фильтр не удаляет
        self.assertEqual(parse_rubles("1000"), 1000.00)

        # Некорректные строки
        self.assertEqual(parse_rubles(""), 0.0)
        self.assertEqual(parse_rubles("abc"), 0.0)
        self.assertEqual(
            parse_rubles("12.34.56"), 0.0
        )  # Вернет 12.34, так как float('12.34.56') вызовет ValueError

    def test_extract_NDS(self):
        # Стандартные случаи
        self.assertAlmostEqual(extract_NDS(1000.0, 0.05), 47.61904761904762)
        self.assertAlmostEqual(extract_NDS(1234.56, 0.05), 58.29149593495935)

        # Нулевые значения
        self.assertEqual(extract_NDS(0.0, 0.05), 0.0)
        self.assertEqual(extract_NDS(1000.0, 0.0), 0.0)

        # Отрицательные значения
        self.assertAlmostEqual(extract_NDS(-1000.0, 0.05), -47.61904761904762)

    def test_amount_to_words(self):
        # Стандартные суммы
        self.assertEqual(
            amount_to_words(1234.56), "Одна тысяча двести тридцать четыре рубля 56 коп."
        )
        self.assertEqual(amount_to_words(1.01), "Один рубль 01 коп.")
        self.assertEqual(amount_to_words(2.02), "Два рубля 02 коп.")
        self.assertEqual(amount_to_words(5.05), "Пять рублей 05 коп.")
        self.assertEqual(amount_to_words(21.21), "Двадцать один рубль 21 коп.")
        self.assertEqual(amount_to_words(11.11), "Одиннадцать рублей 11 коп.")
        self.assertEqual(amount_to_words(14.14), "Четырнадцать рублей 14 коп.")
        self.assertEqual(amount_to_words(0.99), "Ноль рублей 99 коп.")

        # Граничные значения
        self.assertEqual(amount_to_words(0.0), "Ноль рублей 00 коп.")
        self.assertEqual(amount_to_words(1000000.00), "Один миллион рублей 00 коп.")

    def test_show_amount(self):
        # Стандартные суммы
        self.assertEqual(
            show_amount(1234.56),
            "1234.56 руб. (Одна тысяча двести тридцать четыре рубля 56 коп.)",
        )
        self.assertEqual(show_amount(0.0), "0.00 руб. (Ноль рублей 00 коп.)")
        self.assertEqual(show_amount(1.01), "1.01 руб. (Один рубль 01 коп.)")

    @patch("functions.QLineEdit")
    def test_handle_input(self, mock_qlineedit):
        # Настройка mock
        mock_qlineedit.text.return_value = "1a2b3c4.56d"
        mock_qlineedit.setText = MagicMock()

        # Тестирование
        result = handle_input(mock_qlineedit)

        # Проверки
        mock_qlineedit.setText.assert_called_with("1234.56")
        self.assertEqual(result, 1234.56)

    def test_filter_rubles_edge_cases(self):
        # Несколько точек
        self.assertEqual(filter_rubles("..123..456.."), "..123..456..")

        # Плюсовые и минусовые знаки (не удаляются)
        self.assertEqual(filter_rubles("-1234.56"), "-1234.56")
        self.assertEqual(filter_rubles("+1234.56"), "+1234.56")

    def test_parse_rubles_edge_cases(self):
        # Точки в начале и конце
        self.assertEqual(parse_rubles(".123"), 0.12)
        self.assertEqual(parse_rubles("123."), 123.0)
        self.assertEqual(parse_rubles(".123."), 0.12)

        # Пробелы
        self.assertEqual(parse_rubles("  1234.56  "), 1234.56)

    def test_amount_to_words_negative(self):
        # Отрицательные суммы (предполагается, что функция не предназначена для отрицательных чисел)
        self.assertEqual(
            amount_to_words(-1234.56),
            "Одна тысяча двести тридцать четыре рубля 56 коп.",
        )

    @patch("functions.num2words")
    def test_amount_to_words_mock_num2words(self, mock_num2words):
        # Проверка интеграции с num2words
        mock_num2words.return_value = "Тест"
        result = amount_to_words(123.45)
        self.assertEqual(result, "Тест рублей 45 коп.")
        mock_num2words.assert_called_with(123, lang="ru")


if __name__ == "__main__":
    unittest.main()
