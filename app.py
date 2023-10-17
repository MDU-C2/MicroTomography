##
# Modules
##
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidgetItem, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import time
##
# Class files
##
from Spline import spline
from reshapeArr import reshapeArr
from Surface_Reconstruction import surface_Reconstruction
import ScanningSystem
import Robot_YUMI
import Button_MoveRobotArm
from Button_LOAD import load_model
from Button_SAVE import save_model
import robot_Control

#global variables
robot = None
#data = None #Global variable for store the data
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
        self.ui.btn_Calibration.pressed.connect(self.calibration)

        #spinbox function
        #self.ui.spb_SampleSteps.valueChanged.connect(self.changeSteps)

        # Create a layout for the plot viwer
        layout = QVBoxLayout(self.ui.viewer_scanning)
        self.figure = plt.figure(figsize=(700,700))

        ##########################
        # Create a Matplotlib figure and add a 3D subplot for Scanning
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax= self.figure.add_subplot(111, projection='3d')

        # Set axis labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Create a Matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self.ui.viewer_scanning)
        layout.addWidget(self.toolbar)

        self.laserPos(self.ax, 0, 0, 0)

        #table label names
        self.ui.tbw_default.setHorizontalHeaderLabels(["X", "Y", "Z"])
        self.ui.tbw_mylist.setHorizontalHeaderLabels(["X", "Y", "Z"])

        #print message in the text browser
        self.printLog(self.ui.tbx_log, "System open")

        #Read defalut data
        #self.readDefaultTable()
        #self.printLog(self.ui.tbx_log, "Default table read")

    #Set Calibration
    def calibration(self):
        global robot

        calibration_message = QMessageBox()
        calibration_message.setText("Press Ok when arm is in calibration position to set new calibration point...")
        calibration_message.setWindowTitle("Calibration")
        calibration_message.setStandardButtons(QMessageBox.Ok)
        calibration_message.exec_()

        if robot != None:
            robot_Control.set_Calibration(robot)
        else:
            self.printLog(self.ui.tbx_log, "No robot connect")
        

    #function load file
    def loadFile(self):
        global data
        data, message = load_model() # Load the data from .mat file

        self.printLog(self.ui.tbx_log, message)     

        try:
            data_X = data[:,0,:] #Reorganize the data into rows 
            data_Y = data[:,1,:]
            data_Z = data[:,2,:]

            self.writeDefaultTable()
            self.updatePlot() #Plot the figure after spline
            
            self.dataPreprocessing(data_X, data_Y, data_Z)
           
            #Open the Save option
            self.ui.btn_Save.setEnabled(True)
            
        except:
            pass

    #funciton: save file 
    def saveFile(self):
        global data

        message = save_model(data)
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

        self.ui.label_x_RobPos.setText(f"X: {laser_x}")
        self.ui.label_y_RobPos.setText(f"Y: {laser_y}")
        self.ui.label_z_RobPos.setText(f"Z: {laser_z}")

        self_redpoint.scatter(laser_x, laser_y, laser_z, color = "red")

    #functions: move robot arm position
    def MoveRobotArm_XUp(self):  
        global laser_x
        laser_x = Button_MoveRobotArm.MoveRobotArm_Up(laser_x)
        self.updatePlot()

    def MoveRobotArm_YUp(self):
        global laser_y
        laser_y = Button_MoveRobotArm.MoveRobotArm_Up(laser_y)
        self.updatePlot()

    def MoveRobotArm_ZUp(self):
        global laser_z
        laser_z = Button_MoveRobotArm.MoveRobotArm_Up(laser_z)
        self.updatePlot()

    def MoveRobotArm_XDown(self):
        global laser_x
        laser_x = Button_MoveRobotArm.MoveRobotArm_Down(laser_x)
        self.updatePlot()
    
    def MoveRobotArm_YDown(self):
        global laser_y
        laser_y = Button_MoveRobotArm.MoveRobotArm_Down(laser_y)
        self.updatePlot()

    def MoveRobotArm_ZDown(self):
        global laser_z
        laser_z = Button_MoveRobotArm.MoveRobotArm_Down(laser_z)
        self.updatePlot()

    #function: update the plot
    def updatePlot(self):
        global laser_x
        global laser_y
        global laser_z
        #global data

        #Clean the axis
        self.ax.cla()

        # Set axis labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.laserPos(self.ax, laser_x, laser_y, laser_z) #plot laser position
    
        try:
            tableData = self.readTable()

            data = pd.DataFrame(tableData, columns=['X_value', 'Y_value','Z_value'])

            data_X = data['X_value']  #Reorganize the data into rows 
            data_Y = data['Y_value']
            data_Z = data['Z_value']

            # Create a 3D scatter plot
            self.ax.scatter(data_X, data_Y, data_Z, c='b', marker='o')

        except:
            print("fail to read data")

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
            self.printLog(self.ui.tbx_log, "Error on input. Include alphabets or empty input")

    def clear_table(self):
        self.ui.tbw_mylist.setRowCount(0)  # Remove all rows from the table

    def writeDefaultTable(self):
        global data
        x_count = 0

        try: 
            (num_rows, num_cols, num_depth) = data.shape
            # Populate the table with X, Y, and Z values
            for depth in range(num_depth):
                for row in range(num_rows):
                    # Get the current number of rows in the tableWidget
                    current_row_count = self.ui.tbw_default.rowCount()

                    # Insert a new row at the end of the table
                    self.ui.tbw_default.insertRow(current_row_count) 
                    x_count = 0
                    for col in range(num_cols):                       
                        x_item = QTableWidgetItem(str(round(data[row, col, depth],2)))
                        self.ui.tbw_default.setItem(current_row_count, x_count, x_item)
                        x_count = x_count + 1
        except:
            self.printLog(self.ui.tbx_log, "fail to write data to the table")
            pass
    
    def readTable(self):
        tableData = []

        # read which tab is on now
        tabIndex = self.ui.twg_table.currentIndex()

        if tabIndex == 0:
            table = self.ui.tbw_default
        elif tabIndex == 1:
            table = self.ui.tbw_mylist

        try: 
             # Extract data from the QTableWidget
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
            
                return tableData
        except:
            self.printLog(self.ui.tbx_log, "fail to read data from the table")
            pass
            
    
    def scanModel(self):
        global laser_x
        global laser_y
        global laser_z
        global data
        global robot

        NonNumericExist = 0
    
        # read which tab is on now
        tabIndex = self.ui.twg_table.currentIndex()

        if tabIndex == 0:
            table = self.ui.tbw_default
        elif tabIndex == 1:
            table = self.ui.tbw_mylist

        self.printLog(self.ui.tbx_log, "Checking items in the table...")

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

            
            #connect Yumi
            connection_yumi = self.connectYumi()

            #initial the position of Yumi
            if(robot != None):
                initPos = Robot_YUMI.initialPos(robot)
                if initPos: 
                    self.printLog(self.ui.tbx_log, "Moving Yumi arm to initial position")
                else:
                    self.printLog(self.ui.tbx_log, "Not able to move Yumi arm to initial position")
            
            #if NonNumericExist == 0 and connection_yumi:  (use for robot studio simulation)
            if NonNumericExist == 0:
                #data = pd.DataFrame(tableData, columns=['X_value', 'Y_value','Z_value'])
                
                data = tableData
                #Can not be plot in real time. (this is a bug, may fix it in the future)
                self.updatePlot()   

                self.printLog(self.ui.tbx_log, "Scanning complete")
                #Open the Save option
                self.ui.btn_Save.setEnabled(True)
            else:
                self.printLog(self.ui.tbx_log, "Scanning fail")
        else:
            self.printLog(self.ui.tbx_log, "No item in the table")
        
    def isNumber(self, text):
        try:
            float(text)
            return True
        except ValueError:
            return False
        
    def connectYumi(self):
        global robot
        robot = Robot_YUMI.connectYumi()

        if (robot != None):
            self.printLog(self.ui.tbx_log, "Connect to the yumi robot arm")
            return True
        else:
            self.printLog(self.ui.tbx_log, "unable to connect to the robot arm")
            return False
        
    #def changeSteps(self):
        #for robot moves 

    def dataPreprocessing(self, data_X, data_Y, data_Z):
        global data
        step_down = 0.005  # Step size for spline interpolation with x,y in Z direction. The smaller this value is, the more values will be added, duh.
        totalTime = time.time()
        t = time.time()

        ##Runs the spline in z direction
        newData_X, newData_Y, newData_Z = spline.spline_xy(data_X, data_Y, data_Z, step_down)

        # newData_X,newData_Y,newData_Z = spline.cubic_spline(data_X,data_Y,data_Z,step_down) #Different spline

        elapsed = time.time() - t
        print("Time to do spline:", elapsed)


        nPoints = 10  # n*nPoints = number of new points
        n = data_X.shape[1]
        t = time.time()


        # Runs the spline in aximuth direction creates perfect circle slices
        newData_X, newData_Y, newData_Z = spline.splinePerfectCircle(
            newData_X, newData_Y, newData_Z, nPoints
        )

        print(newData_X)

        # Runs the spline in aximuth direction Change the data less
        """newData_X, newData_Y, newData_Z = spline.spline_circle(
            newData_X, newData_Y, newData_Z, nPoints
        )"""
        elapsed = time.time() - t
        print("Time to do horizontal spline:", elapsed)

        # Reshapes the array into a points array
        points = reshapeArr.fixPoints(newData_X, newData_Y, newData_Z)


        #################################################################################
        print("Number of datapoint :", len(points))

        save = False  # Save file? #Takes pretty long time to save .obj file, about 5-10 minutes
        saveImage = False  # Save plot image?

        surface_Reconstruction.delaunay_original(points, save)  ##tight cocone variant
        # surface_Reconstruction.alpha_Shape(points,save)
        # surface_Reconstruction.ball_Pivoting(points,save)
        # surface_Reconstruction.poisson_surfRecon(points, save)

        totalElapsed = time.time() - totalTime
        print("Time to complete Sample + reconstruction : ", totalElapsed)

        
app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())