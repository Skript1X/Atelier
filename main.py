import sys
import mysql.connector as con
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt5.uic import loadUi
from re import fullmatch
from configparser import ConfigParser
from os.path import isfile


class LoginApp(QDialog):
    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi("forms/login-form.ui", self)
        if isfile('db_config.ini'):
            pass
        else:
            config = ConfigParser()
            config["mysql_database"] = {
                "host": "",
                "user": "",
                "password": "",
                "db": ""
            }
            with open('db_config.ini', 'w') as conf:
                config.write(conf)
            QMessageBox.information(self, "Atelier", "Fill in the config file!")
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)

    def login(self):
        un = self.tb1.text()
        pw = self.tb2.text()

        if len(un) < 6:
            QMessageBox.information(self, "Atelier", "The minimum length of the user name is 6 characters!")
        elif len(un) > 30:
            QMessageBox.information(self, "Atelier", "The maximum length of the user name is 30 characters!")
        elif len(pw) < 6:
            QMessageBox.information(self, "Atelier", "The minimum password length is 6 characters!")
        elif len(pw) > 100:
            QMessageBox.information(self, "Atelier", "The maximum password length is 100 characters!")
        else:
            config = ConfigParser()
            config.read("db_config.ini")
            database = config["mysql_database"]
            db_host = database["host"]
            db_user = database["user"]
            db_password = database["password"]
            db_db = database["db"]
            try:
                db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
                cur = db.cursor()
                cur.execute("select pass from users where username='" + un + "'")
                result_pw = cur.fetchone()
                try:
                    if pw == str(result_pw[0]):
                        QMessageBox.information(self, "Atelier", "You have successfully logged in!")
                        self.tb1.setText("")
                        self.tb2.setText("")
                        w.setCurrentIndex(2)
                except:
                    QMessageBox.information(self, "Atelier", "There is no such user!")
            except:
                QMessageBox.information(self, "Atelier", "There is no connection in the database, fill in the config file!")

    def show_reg(self):
        w.setCurrentIndex(1)


class RegApp(QDialog):
    def __init__(self):
        super(RegApp, self).__init__()
        loadUi("forms/register-form.ui", self)
        if isfile('db_config.ini'):
            pass
        else:
            config = ConfigParser()
            config["mysql_database"] = {
                "host": "",
                "user": "",
                "password": "",
                "db": ""
            }
            with open('db_config.ini', 'w') as conf:
                config.write(conf)
            QMessageBox.information(self, "Atelier", "Fill in the config file!")
        self.b3.clicked.connect(self.reg)
        self.b4.clicked.connect(self.show_login)

    def reg(self):
        un = self.tb3.text()
        pw = self.tb4.text()
        em = self.tb5.text()

        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if len(un) < 6:
            QMessageBox.information(self, "Atelier", "The minimum length of the user name is 6 characters!")
        elif len(un) > 30:
            QMessageBox.information(self, "Atelier", "The maximum length of the user name is 30 characters!")
        elif len(pw) < 6:
            QMessageBox.information(self, "Atelier", "The minimum password length is 6 characters!")
        elif len(pw) > 100:
            QMessageBox.information(self, "Atelier", "The maximum password length is 100 characters!")
        elif not fullmatch(regex, em):
            QMessageBox.information(self, "Atelier", "Invalid email!")
        elif len(em.split("@")[0]) < 5:
            QMessageBox.information(self, "Atelier", "The minimum length of the mail is 5 characters!")
        elif len(em.split("@")[0]) > 100:
            QMessageBox.information(self, "Atelier", "The maximum length of the mail is 100 characters!")
        else:
            config = ConfigParser()
            config.read("db_config.ini")
            database = config["mysql_database"]
            db_host = database["host"]
            db_user = database["user"]
            db_password = database["password"]
            db_db = database["db"]
            try:
                db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
                cur = db.cursor()
                cur.execute("select username from users where username='" + un + "'")
                result_un = cur.fetchone()
                if result_un:
                    QMessageBox.information(self, "Atelier", "Such a user is already registered")
                else:
                    cur.execute("insert into users (username, pass, email) values('" + un + "', '" + pw + "', '" + em + "')")
                    db.commit()
                    QMessageBox.information(self, "Atelier", "You have successfully registered!")
                    self.tb3.setText("")
                    self.tb4.setText("")
                    self.tb5.setText("")
                    w.setCurrentIndex(0)
            except Exception as e:
                print(e)
                QMessageBox.information(self, "Atelier", "There is no connection in the database, fill in the config file!")

    def show_login(self):
        w.setCurrentIndex(0)

class SelectApp(QDialog):
    def __init__(self):
        super(SelectApp, self).__init__()
        loadUi("forms/select-form.ui", self)
        self.b5.clicked.connect(self.select_data)
        self.pushButton.clicked.connect(self.add_data)
        self.pushButton_3.clicked.connect(self.del_data)
        self.pushButton_2.clicked.connect(self.update_result)
        self.pushButton_4.clicked.connect(self.save_results)
        self.modified = {}
        self.titles = None


    def select_data(self):
        config = ConfigParser()
        config.read("db_config.ini")
        database = config["mysql_database"]
        db_host = database["host"]
        db_user = database["user"]
        db_password = database["password"]
        db_db = database["db"]
        try:
            table = self.tableWidget
            table.setHorizontalHeaderLabels(['id', 'First name', 'Tel. number', 'Order description', 'Order price'])
            db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
            cur = db.cursor()
            cur.execute("select id, first_name, phone_number, description, price from customer_orders")
            result = cur.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except:
            QMessageBox.information(self, "Atelier", "Unknown database or table name!")


    def update_result(self):
        config = ConfigParser()
        config.read("db_config.ini")
        database = config["mysql_database"]
        db_host = database["host"]
        db_user = database["user"]
        db_password = database["password"]
        db_db = database["db"]
        self.tableWidget.itemChanged.connect(self.item_changed)
        try:
            table = self.tableWidget
            table.setHorizontalHeaderLabels(['id', 'First name', 'Tel. number', 'Order description', 'Order price'])
            db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
            cur = db.cursor()
            cur.execute("select id, first_name, phone_number, description, price from customer_orders where id='" + self.spinBox.text() + "'")
            result = cur.fetchall()
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            self.titles = [description[0] for description in cur.description]
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}
        except:
            QMessageBox.information(self, "Atelier", "There was no such record!")


    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()


    def save_results(self):
        config = ConfigParser()
        config.read("db_config.ini")
        database = config["mysql_database"]
        db_host = database["host"]
        db_user = database["user"]
        db_password = database["password"]
        db_db = database["db"]
        try:
            if self.modified:
                db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
                cur = db.cursor()
                que = "UPDATE customer_orders SET\n"
                que += ", ".join([f"{key}='{self.modified.get(key)}'"
                                  for key in self.modified.keys()])
                que += "WHERE id = '" + self.spinBox.text() + "'"
                cur.execute(que)
                db.commit()
                self.modified.clear()
        except:
            QMessageBox.information(self, "Atelier", "Unable to save changes!")

    def del_data(self):
        config = ConfigParser()
        config.read("db_config.ini")
        database = config["mysql_database"]
        db_host = database["host"]
        db_user = database["user"]
        db_password = database["password"]
        db_db = database["db"]
        try:
            db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
            cur = db.cursor()
            chosenRow = self.tableWidget.currentRow()
            item = self.tableWidget.item(chosenRow, 1)
            item2 = self.tableWidget.item(chosenRow, 2)
            item3 = self.tableWidget.item(chosenRow, 3)
            item4 = self.tableWidget.item(chosenRow, 4)
            first_name = str(item.text())
            phone_number = str(item2.text())
            description = str(item3.text())
            price = str(item4.text())
            self.tableWidget.removeRow(chosenRow)
            cur.execute("DELETE FROM customer_orders WHERE first_name='" + first_name + "' AND phone_number='" + phone_number + "' AND description='" + description + "' AND price='" + price + "'")
            db.commit()
        except:
            QMessageBox.information(self, "Atelier", "Select the line you want to delete!")


    def add_data(self):
        config = ConfigParser()
        config.read("db_config.ini")
        database = config["mysql_database"]
        db_host = database["host"]
        db_user = database["user"]
        db_password = database["password"]
        db_db = database["db"]
        try:
            first_name = self.lineEdit.text()
            phone_number = self.lineEdit_2.text()
            description = self.lineEdit_3.text()
            price = self.lineEdit_4.text()
            db = con.connect(host=f"{db_host}", user=f"{db_user}", password=f"{db_password}", db=f"{db_db}")
            cur = db.cursor()
            query = "insert into customer_orders (first_name, phone_number, description, price) VALUES (%s, %s, %s, %s)"
            value = (first_name, phone_number, description, price)
            cur.execute(query, value)
            db.commit()
        except:
            QMessageBox.information(self, "Atelier", "Select the id record to change it!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QtWidgets.QStackedWidget()
    w.setWindowTitle("Atelier")
    loginform = LoginApp()
    registrationform = RegApp()
    selectform = SelectApp()
    w.addWidget(loginform)
    w.addWidget(registrationform)
    w.addWidget(selectform)
    w.setCurrentIndex(0)
    w.setFixedWidth(400)
    w.setFixedHeight(500)
    w.show()
    sys.exit(app.exec_())
