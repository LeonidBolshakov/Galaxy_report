import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QLineEdit
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

from report import Report
from validatedlineedit import ValidatedLineEdit


class TestReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Инициализация QApplication (обязательно для работы с Qt)
        cls.app = QApplication([])

    def setUp(self):
        # Создаем экземпляр окна перед каждым тестом
        self.window = Report()
        self.window.show()

    def tearDown(self):
        # Закрываем окно после каждого теста
        self.window.close()

    def test_input_validation_and_display(self):
        # Находим нужные виджеты.
        clients_widget = self.window.findChild(ValidatedLineEdit, "EditClients")
        total_clients_widget = self.window.findChild(QLineEdit, "rEditClients")
        corporation_without_NDS_widget = self.window.findChild(QLineEdit, "rEditCorp")
        corporation_with_NDS_widget = self.window.findChild(QLineEdit, "rEditCorpNDS")
        left_widget = self.window.findChild(QLineEdit, "rEditLeft")
        over_widget = self.window.findChild(QLineEdit, "rEditOver")

        # Установка значений с отладочной печатью
        clients_widget.setText("100")

        QApplication.processEvents()

        # Обрабатываем события приложения
        QApplication.processEvents()

        # Проверяем результаты
        self.assertEqual(
            total_clients_widget.text(), "100.00 руб. (Сто рублей 00 коп.)"
        )
        self.assertEqual(
            corporation_without_NDS_widget.text(),
            "50.00 руб. (Пятьдесят рублей 00 коп.)",
        )
        self.assertEqual(
            corporation_with_NDS_widget.text(),
            "60.00 руб. (Шестьдесят рублей 00 коп.), включая НДС 10.00 руб. (Десять рублей 00 коп.)",
        )
        self.assertEqual(
            left_widget.text(),
            "60.00 руб. (Шестьдесят рублей 00 коп.), включая НДС 10.00 руб. (Десять рублей 00 коп.)",
        )
        self.assertEqual(
            over_widget.text(),
            "0.00 руб. (Ноль рублей 00 коп.), включая НДС 0.00 руб. (Ноль рублей 00 коп.)",
        )

    @patch("PyQt6.QtWidgets.QApplication.clipboard")
    def test_clipboard_copy(self, mock_clipboard):
        # Настраиваем mock буфера обмена
        mock_instance = MagicMock()
        mock_clipboard.return_value = mock_instance

        # Находим виджет вывода
        output_widget = self.window.findChild(QLineEdit, "rEditClients")
        output_widget.setText("100.00 руб. (Сто рублей 00 коп.)")

        # Симулируем клик мышью по виджету
        QTest.mouseClick(
            output_widget,
            Qt.MouseButton.LeftButton,
        )

        # Проверяем, что текст скопирован
        mock_instance.setText.assert_called_once_with(
            "100.00 руб. (Сто рублей 00 коп.)"
        )


if __name__ == "__main__":
    unittest.main()
