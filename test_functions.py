import unittest
from unittest.mock import MagicMock, patch
from functions import (
    filter_rubles,
    parse_rubles,
    amount_to_words,
    extract_NDS,
    show_amount,
)


class TestFunctions(unittest.TestCase):
    def test_filter_rubles(self):
        # Стандартные случаи
        self.assertEqual(filter_rubles("12345.67"), "12345.67")
        self.assertEqual(filter_rubles("-372"), "-372")

        # Лишние символы
        self.assertEqual(filter_rubles("1к2345.678"), "1к2345.678")
        self.assertEqual(filter_rubles("1 234'5.678"), "12345.678")

    def test_parse_rubles(self):
        # Корректные числовые строки
        self.assertEqual(parse_rubles("1234.567"), 1234.57)
        self.assertEqual(parse_rubles("1'234.56"), 1234.56)
        self.assertEqual(parse_rubles("1000"), 1000.00)

        # Некорректные строки
        self.assertEqual(parse_rubles(""), 0.0)

    def test_extract_NDS(self):
        # Стандартные случаи
        self.assertAlmostEqual(extract_NDS(1000.0, 5.0), 47.61904761904762)
        self.assertAlmostEqual(extract_NDS(1234.56, 5.0), 58.78857142857142)

        # Нулевые значения
        self.assertEqual(extract_NDS(0.0, 5.0), 0.0)
        self.assertEqual(extract_NDS(1000.0, 0.0), 0.0)

        # Отрицательные значения
        self.assertAlmostEqual(
            extract_NDS(-1000.0, 5.0),
            -47.61904761904762,
        )

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
        self.assertEqual(
            amount_to_words(-1234567.127),
            "Минус один миллион двести тридцать четыре тысячи пятьсот шестьдесят семь рублей -13 коп.",
        )

    def test_show_amount(self):
        # Стандартные суммы
        self.assertEqual(
            show_amount(1234.56),
            "1234.56 руб. (Одна тысяча двести тридцать четыре рубля 56 коп.)",
        )
        # Пограничные случаи
        self.assertEqual(show_amount(0.0), "0.00 руб. (Ноль рублей 00 коп.)")
        self.assertEqual(show_amount(1.0145), "1.01 руб. (Один рубль 01 коп.)")

    def test_parse_rubles_edge_cases(self):
        # Точки в начале и конце
        self.assertEqual(parse_rubles(".123"), 0.12)
        self.assertEqual(parse_rubles("123."), 123.0)

        # Пробелы
        self.assertEqual(parse_rubles("  1234.56  "), 1234.56)

    @patch("functions.QMessageBox")
    def test_parse_rubles_error_case(self, mock_msgbox):
        mock_instance = MagicMock()
        mock_msgbox.return_value = mock_instance
        self.assertIs(parse_rubles(".123."), None)
        mock_msgbox.assert_called_once()
        mock_instance.exec.assert_called_once()

    def test_amount_to_words_negative(self):
        # Отрицательные суммы
        self.assertEqual(
            amount_to_words(-1234.56),
            "Минус одна тысяча двести тридцать четыре рубля -56 коп.",
        )


if __name__ == "__main__":
    unittest.main()
