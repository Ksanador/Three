import os
import sys
import sqlite3

from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem,
                             QMessageBox)

from UI.ui_main import Ui_MainWindow
from addEditCoffeeForm import AddEditCoffeeForm


def db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'data', 'coffee.sqlite')


class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "Название сорта", "Степень обжарки",
            "Молотый/В зернах", "Описание вкуса", "Цена", "Объем упаковки"
        ])

        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)
        self.tableWidget.doubleClicked.connect(self.edit_coffee)

        self.load_data()

    def load_data(self):
        try:
            con = sqlite3.connect(db_path())
            cur = con.cursor()
            cur.execute(
                "SELECT id, name, roast, ground, description, price, volume "
                "FROM coffee ORDER BY id"
            )
            rows = cur.fetchall()
            con.close()

            self.tableWidget.setRowCount(len(rows))
            for r, row in enumerate(rows):
                for c, value in enumerate(row):
                    self.tableWidget.setItem(r, c, QTableWidgetItem(str(value)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка БД", str(e))

    def add_coffee(self):
        if AddEditCoffeeForm(coffee_id=None, parent=self).exec():
            self.load_data()

    def edit_coffee(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.information(self, "Информация",
                                    "Выберите запись для редактирования")
            return
        coffee_id = int(self.tableWidget.item(row, 0).text())
        if AddEditCoffeeForm(coffee_id=coffee_id, parent=self).exec():
            self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())