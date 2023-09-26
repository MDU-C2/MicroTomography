import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import ScanningSystem
from Button_LOAD import load_model
from Button_SAVE import save_model_to_csv
import pandas as pd
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
 

#global variables
data = pd.DataFrame() #Global variable for store the data
laser_x = 0 #laser position x
laser_y = 0 #laser position y
laser_z = 0 #laser position z


class AppWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = ScanningSystem.Ui_MainWindow()
        self.ui.setupUi(self)

        #button functions 
        self.ui.btn_Load.pressed.connect(self.loadFile)
        self.ui.btn_Save.pressed.connect(self.saveFile)
        self.ui.btn_xUp.pressed.connect(self.MoveRobotArm_XUp)
        self.ui.btn_xDown.pressed.connect(self.MoveRobotArm_XDown)
        self.ui.btn_yUp.pressed.connect(self.MoveRobotArm_YUp)
        self.ui.btn_yDown.pressed.connect(self.MoveRobotArm_YDown)
        self.ui.btn_zUp.pressed.connect(self.MoveRobotArm_ZUp)
        self.ui.btn_zDown.pressed.connect(self.MoveRobotArm_ZDown)

        # Create a layout for the plot viwer
        layout = QVBoxLayout(self.ui.viewer_3d)

        # Create a Matplotlib figure and add a 3D subplot
        self.figure = plt.figure(figsize=(700,700))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax= self.figure.add_subplot(111, projection='3d')

        # Set axis labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        #laser position
        self.laserPos(self.ax, self.ui.label_x_RobPos,self.ui.label_y_RobPos, self.ui.label_z_RobPos)

        #print message in the text browser
        self.printLog(self.ui.tbx_log, "System open")


    #function load file
    def loadFile(self):
        file_path = load_model()
  
        if(file_path != None):
            #print the message in the text browser
            message = f"Open model from: {file_path}"
            self.printLog(self.ui.tbx_log, message)
           
            # Read data from CSV file
            global data
            data = pd.read_csv(file_path)

            # Extract X, Y, and Z coordinates from the CSV columns
            x = data['X_value']  # Replace 'X_column_name' with the actual column name for X coordinates
            y = data['Y_value']  # Replace 'Y_column_name' with the actual column name for Y coordinates
            z = data['Z_value']  # Replace 'Z_column_name' with the actual column name for Z coordinates

            # Create a 3D scatter plot
            self.ax.scatter(x, y, z, c='b', marker='o')
            self.canvas.draw()

            #Open the Save option
            self.ui.btn_Save.setEnabled(True)
        else:
            message = "None file selected"
            self.printLog(self.ui.tbx_log, message)


    #funciton: save file 
    def saveFile(self):
        global data
        file_path = save_model_to_csv(data)
        if(file_path != None):
            message = f"Model saved to: {file_path}"
            self.printLog(self.ui.tbx_log, message)
        else:
            message = "Saving cancel"
            self.printLog(self.ui.tbx_log, message)


    #function: print message in the text browser
    def printLog(self, txt_box, message):
        txt_box.append(message)

    
    #function: laser position
    def laserPos(self, self_redpoint, label_x, label_y, label_z):
        global laser_x
        global laser_y
        global laser_z

        self_redpoint.scatter(laser_x, laser_y, laser_z, color='red', marker='o')
        label_x.setText(f"X: {laser_x}")
        label_y.setText(f"Y: {laser_y}")
        label_z.setText(f"Z: {laser_z}")

    #functions: move robot arm position
    def MoveRobotArm_XUp(self):
        global laser_x
        laser_x = laser_x + 10
        self.updatePlot()

    def MoveRobotArm_YUp(self):
        global laser_y
        laser_y = laser_y + 10
        self.updatePlot()

    def MoveRobotArm_ZUp(self):
        global laser_z
        laser_z = laser_z + 10
        self.updatePlot()

    def MoveRobotArm_XDown(self):
        global laser_x
        laser_x = laser_x - 10
        self.updatePlot()
    
    def MoveRobotArm_YDown(self):
        global laser_y
        laser_y = laser_y - 10
        self.updatePlot()

    def MoveRobotArm_ZDown(self):
        global laser_z
        laser_z = laser_z - 10
        self.updatePlot()

    #function: update the plot
    def updatePlot(self):
        self.ax.cla()

        # Set axis labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.laserPos(self.ax, self.ui.label_x_RobPos,self.ui.label_y_RobPos, self.ui.label_z_RobPos)

        if data.empty != True:
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