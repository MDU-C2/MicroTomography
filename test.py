import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import numpy as np

class TableToNumpyExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Table to NumPy Example')

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout to hold the table
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create a QTableWidget
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Add some data to the table (you can replace this with your data)
        self.table.setRowCount(3)
        self.table.setColumnCount(3)

        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for i in range(3):
            for j in range(3):
                item = QTableWidgetItem(str(data[i][j]))
                self.table.setItem(i, j, item)

        # Convert the QTableWidget data to a NumPy array
        numpy_array = self.table_to_numpy(self.table)
        print(numpy_array)

    def table_to_numpy(self, table):
        rows = table.rowCount()
        cols = table.columnCount()
        data = np.empty((rows, cols), dtype=object)

        for row in range(rows):
            for col in range(cols):
                item = table.item(row, col)
                if item is not None:
                    data[row, col] = item.text()
                else:
                    data[row, col] = ""

        return data

def main():
    app = QApplication(sys.argv)
    ex = TableToNumpyExample()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
