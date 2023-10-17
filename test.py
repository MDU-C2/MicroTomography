import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error Message Example")
        self.setGeometry(100, 100, 400, 200)

        button = QPushButton("Show Error Message", self)
        button.setGeometry(150, 75, 200, 50)
        button.clicked.connect(self.show_error_message)

    def show_error_message(self):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setText("An error has occurred!")
        error_message.setWindowTitle("Error")
        error_message.setStandardButtons(QMessageBox.Ok)
        error_message.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
