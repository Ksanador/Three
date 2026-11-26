import os
import sqlite3
from PyQt6.QtWidgets import QDialog, QMessageBox

from UI.ui_addEditCoffeeForm import Ui_AddEditCoffeeForm


def db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'data', 'coffee.sqlite')


class AddEditCoffeeForm(QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, coffee_id=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.coffee_id = coffee_id

        if coffee_id is None:
            self.setWindowTitle("Добавление кофе")
        else:
            self.setWindowTitle("Редактирование кофе")
            self.load_existing()

        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)

    def load_existing(self):
        con = sqlite3.connect(db_path())
        cur = con.cursor()
        cur.execute(
            "SELECT name, roast, ground, description, price, volume "
            "FROM coffee WHERE id = ?", (self.coffee_id,)
        )
        row = cur.fetchone()
        con.close()

        if row is None:
            QMessageBox.warning(self, "Ошибка", "Запись не найдена")
            self.reject()
            return

        name, roast, ground, description, price, volume = row
        self.nameEdit.setText(name)
        self.roastCombo.setCurrentText(roast)
        self.groundCombo.setCurrentText(ground)
        self.descEdit.setPlainText(description)
        self.priceSpin.setValue(price)
        self.volumeSpin.setValue(volume)

    def save(self):
        name = self.nameEdit.text().strip()
        description = self.descEdit.toPlainText().strip()

        if not name or not description:
            QMessageBox.warning(self, "Ошибка",
                                "Заполните название и описание вкуса")
            return

        con = sqlite3.connect(db_path())
        cur = con.cursor()

        if self.coffee_id is None:
            cur.execute(
                "INSERT INTO coffee (name, roast, ground, description, price, volume) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (name, self.roastCombo.currentText(),
                 self.groundCombo.currentText(), description,
                 self.priceSpin.value(), self.volumeSpin.value())
            )
        else:
            cur.execute(
                "UPDATE coffee SET name=?, roast=?, ground=?, description=?, "
                "price=?, volume=? WHERE id=?",
                (name, self.roastCombo.currentText(),
                 self.groundCombo.currentText(), description,
                 self.priceSpin.value(), self.volumeSpin.value(),
                 self.coffee_id)
            )
        con.commit()
        con.close()
        self.accept()
