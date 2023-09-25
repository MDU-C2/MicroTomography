import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import ScanningSystem
from Button_LOAD import load_on_click
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ScanningSystem.Ui_MainWindow()
        self.ui.setupUi(self)
        #button functions
        self.ui.btn_Load.pressed.connect(self.loadFile)

        # Create a layout for the plot viwer
        layout = QVBoxLayout(self.ui.viewer_3d)

        # Create a Matplotlib figure and add a 3D subplot
        self.figure = plt.figure(figsize=(700,700))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111, projection='3d')

        # Set axis labels
        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')

        # Limit the rotation by adjusting the elevation and azimuth angles
        self.ax.dist = 8  # Adjust the distance from the plot

    def loadFile(self):
        file_path = load_on_click()
        print(f"Selected file: {file_path}")

        if(file_path != None):
            # Read data from CSV file
            data = pd.read_csv(file_path)

            # Extract X, Y, and Z coordinates from the CSV columns
            x = data['X_value']  # Replace 'X_column_name' with the actual column name for X coordinates
            y = data['Y_value']  # Replace 'Y_column_name' with the actual column name for Y coordinates
            z = data['Z_value']  # Replace 'Z_column_name' with the actual column name for Z coordinates

            # Create a 3D scatter plot
            self.ax.scatter(x, y, z, c='b', marker='o')
            self.canvas.draw()


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())