import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

#My files
import ScanningSystem
from Button_LOAD import load_model
from Button_SAVE import save_model_to_csv

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
        self.ui.btn_input.pressed.connect(self.insert_row)
        self.ui.btn_xUp.pressed.connect(self.MoveRobotArm_XUp)
        self.ui.btn_xDown.pressed.connect(self.MoveRobotArm_XDown)
        self.ui.btn_yUp.pressed.connect(self.MoveRobotArm_YUp)
        self.ui.btn_yDown.pressed.connect(self.MoveRobotArm_YDown)
        self.ui.btn_zUp.pressed.connect(self.MoveRobotArm_ZUp)
        self.ui.btn_zDown.pressed.connect(self.MoveRobotArm_ZDown)
        self.ui.btn_clearTable.pressed.connect(self.clear_table)
        self.ui.btn_Scan.pressed.connect(self.scanModel)

        # Create a layout for the plot viwer
        layout = QVBoxLayout(self.ui.viewer_3d)

        # Create a Matplotlib figure and add a 3D subplot
        self.figure = plt.figure(figsize=(700,700))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create a Matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self.ui.viewer_3d)
        layout.addWidget(self.toolbar)

        self.ax= self.figure.add_subplot(111, projection='3d')

        # Set axis labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        #Initial laser position (change it later after we connect the robot arm)
        self.laserPos(self.ax,0,0,0)

        #table label names
        self.ui.tbw_default.setHorizontalHeaderLabels(["X", "Y", "Z"])
        self.ui.tbw_mylist.setHorizontalHeaderLabels(["X", "Y", "Z"])

        #print message in the text browser
        self.printLog(self.ui.tbx_log, "System open")

        #Read defalut data
        self.readDefaultTable()
        self.printLog(self.ui.tbx_log, "Default table read")

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

            #update the plot
            self.updatePlot()

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
    def laserPos(self, self_redpoint, value_x, value_y, value_z):
        global laser_x
        global laser_y
        global laser_z

        laser_x = value_x
        laser_y = value_y
        laser_z = value_z

        self_redpoint.scatter(laser_x, laser_y, laser_z, color='red', marker='o')

        self.ui.label_x_RobPos.setText(f"X: {laser_x}")
        self.ui.label_y_RobPos.setText(f"Y: {laser_y}")
        self.ui.label_z_RobPos.setText(f"Z: {laser_z}")

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
        global laser_x
        global laser_y
        global laser_z
    
        self.ax.cla()

        # Set axis labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.laserPos(self.ax, laser_x, laser_y, laser_z)

        if data.empty != True:
            # Extract X, Y, and Z coordinates from the CSV columns
            x = data['X_value']  # Replace 'X_column_name' with the actual column name for X coordinates
            y = data['Y_value']  # Replace 'Y_column_name' with the actual column name for Y coordinates
            z = data['Z_value']  # Replace 'Z_column_name' with the actual column name for Z coordinates

            # Create a 3D scatter plot
            self.ax.scatter(x, y, z, c='b', marker='o')

        self.canvas.draw()

    def insert_row(self):
        #get number from text editor
        insert_x = self.ui.ted_x.toPlainText()
        insert_y = self.ui.ted_y.toPlainText()
        insert_z = self.ui.ted_z.toPlainText()

        if insert_x.replace(".", "").replace("-", "").isdigit() and insert_y.replace(".", "").replace("-", "").isdigit() and insert_z.replace(".", "").replace("-", "").isdigit():
            # Get the current number of rows in the tableWidget
            current_row_count = self.ui.tbw_mylist.rowCount()

            # Insert a new row at the end of the table
            self.ui.tbw_mylist.insertRow(current_row_count)

            # Create items for each cell in the new row
            itemX = QTableWidgetItem(insert_x)
            itemY = QTableWidgetItem(insert_y)
            itemZ = QTableWidgetItem(insert_z)

            # Set the items for each cell in the new row
            self.ui.tbw_mylist.setItem(current_row_count, 0, itemX)
            self.ui.tbw_mylist.setItem(current_row_count, 1, itemY)
            self.ui.tbw_mylist.setItem(current_row_count, 2, itemZ)

            #change tab in the tab table from default to my list
            self.ui.twg_table.setCurrentIndex(1)
        else:
            message = "Error on input. Include alphabets or empty input"
            self.printLog(self.ui.tbx_log, message)

    def clear_table(self):
        self.ui.tbw_mylist.setRowCount(0)  # Remove all rows from the table

    def readDefaultTable(self):
        df = pd.read_csv('testCSV.csv')
                
        # Set the number of rows and columns in the table
        self.ui.tbw_default.setRowCount(df.shape[0])
        self.ui.tbw_default.setColumnCount(df.shape[1])

         # Populate the table with DataFrame data
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.ui.tbw_default.setItem(i, j, item)

        #change tab in the tab table to default
        self.ui.twg_table.setCurrentIndex(0)
    
    def scanModel(self):
        global laser_x
        global laser_y
        global laser_z
        global data

        NonNumericExist = 0
    
        # read which tab is on now
        tabIndex = self.ui.twg_table.currentIndex()

        if tabIndex == 0:
            table = self.ui.tbw_default
        elif tabIndex == 1:
            table = self.ui.tbw_mylist

        message = "Checking items in the table..."
        self.printLog(self.ui.tbx_log, message)

        # Extract data from the QTableWidget
        tableData = []

        if table.rowCount() != 0:
            for row in range(table.rowCount()):
                row_data = []
                for column in range(table.columnCount()):
                    item = table.item(row, column)


                    if item is not None:
                        if self.isNumber(item.text()):
                            row_data.append(float(item.text()))
                        else:
                            message = f"The item [{row + 1},{column + 1}] include is non-numeric value. Scanning breaks."
                            self.printLog(self.ui.tbx_log, message)
                            NonNumericExist = 1
                            break

                tableData.append(row_data)

            if NonNumericExist == 0:
                data = pd.DataFrame(tableData, columns=['X_value', 'Y_value','Z_value'])

                #Can not be plot in real time. (this is a bug, may fix it in the future)
                self.updatePlot()   

                message = "Scanning complete"
                self.printLog(self.ui.tbx_log, message)

        else:
            message = "No item in the table"
            self.printLog(self.ui.tbx_log, message)
        

    def isNumber(self, text):
        try:
            float(text)
            return True
        except ValueError:
            return False

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())