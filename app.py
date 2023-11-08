linearActuator = 0
laserON = 0

##
# Modules
##
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QTableWidgetItem,
    QMessageBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd

import time
from time import sleep

##
# Class files
##
from ObjectReconstruction.Spline import spline
from ObjectReconstruction.reshapeArr import reshapeArr

# from ObjectReconstruction.Surface_Reconstruction import surface_Reconstruction
from GUI import ScanningSystem
from GUI.ButtonCode import Button_MoveRobotArm
from GUI.ButtonCode.Button_LOAD import load_model
from GUI.ButtonCode.Button_SAVE import save_model
from RobotArm import robot_Control
from RobotArm import generate_scan_points
from RobotArm import abb

if laserON == 1:
    from Laser import optoNCDT1402
    from RaspberryPi import transistor

if linearActuator == 1:
    import LinearActuator.linearActuatorController as linearController

# global variables
robot = None
# data = None #Global variable for store the data
laser_x = 0  # laser position x
laser_y = 0  # laser position y
laser_z = 0  # laser position z


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ScanningSystem.Ui_MainWindow()
        self.ui.setupUi(self)

        # button functions
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
        self.ui.btn_Stop.pressed.connect(self.stopScan)
        self.ui.btn_Calibration.pressed.connect(self.calibration)

        if linearActuator == 1:
            self.ui.btn_linear_moveto.pressed.connect(self.MoveLinearActuator(1))
            self.ui.btn_linear_zero_pos.pressed.connect(self.MoveLinearActuator(2))
            self.ui.btn_linear_up.pressed.connect(self.MoveLinearActuator(3))
            self.ui.btn_linear_down.pressed.connect(self.MoveLinearActuator(4))

        # Create a layout for the plot viwer
        layout = QVBoxLayout(self.ui.viewer_scanning)
        self.figure = plt.figure(figsize=(700, 700))

        ##########################
        # Create a Matplotlib figure and add a 3D subplot for Scanning
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111, projection="3d")

        # Set axis labels
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        # Create a Matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self.ui.viewer_scanning)
        layout.addWidget(self.toolbar)

        self.endEffectorPos(self.ax, 0, 0, 0, None)

        # table label names
        self.ui.tbw_default.setHorizontalHeaderLabels(["X", "Y", "Z"])
        self.ui.tbw_mylist.setHorizontalHeaderLabels(["X", "Y", "Z"])

        # Linear Actuator

        # print message in the text browser
        self.printLog(self.ui.tbx_log, "System open")

    # Set Calibration
    def calibration(self):
        global robot

        calibration_message = QMessageBox()
        calibration_message.setText(
            "Press Ok when arm is in calibration position to set new calibration point..."
        )
        calibration_message.setWindowTitle("Calibration")
        calibration_message.setStandardButtons(QMessageBox.Ok)
        calibration_message.exec_()

        if robot != None:
            robot_Control.set_Calibration(robot)
        else:
            self.printLog(self.ui.tbx_log, "No robot connect")

    # function load file
    def loadFile(self):
        global data
        data, message = load_model()  # Load the data from .mat file

        self.printLog(self.ui.tbx_log, message)

        try:
            self.writeDefaultTable(data)
            self.updatePlot()  # Plot the figure after spline

            self.reconstruction3D(data)

        except:
            pass

    # funciton: save file
    def saveFile(self):
        data = self.readTable()

        message = save_model(data)
        self.printLog(self.ui.tbx_log, message)

    # function: print message in the text browser
    def printLog(self, txt_box, message):
        txt_box.append(message)

    # function: laser position
    def endEffectorPos(self, self_redpoint, value_x, value_y, value_z, distance):
        global laser_x
        global laser_y
        global laser_z

        laser_x = value_x
        laser_y = value_y
        laser_z = value_z

        self.ui.label_x_RobPos.setText(f"X: {laser_x}")
        self.ui.label_y_RobPos.setText(f"Y: {laser_y}")
        self.ui.label_z_RobPos.setText(f"Z: {laser_z}")

        if distance != None:
            self.ui.label_dist_laser.setText(f"Distance: {distance}")
        else:
            self.ui.label_dist_laser.setText("Distance: ")

        self_redpoint.scatter(laser_x, laser_y, laser_z, color="red")

    # functions: move robot arm position
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

    # function: update the plot
    def updatePlot(self):
        global laser_x
        global laser_y
        global laser_z

        # Clean the axis
        self.ax.cla()

        # Set axis labels
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.endEffectorPos(
            self.ax, laser_x, laser_y, laser_z, None
        )  # plot the end-effector position

        try:
            tableData = self.readTable()

            data = pd.DataFrame(tableData, columns=["X_value", "Y_value", "Z_value"])

            data_X = data["X_value"]  # Reorganize the data into rows
            data_Y = data["Y_value"]
            data_Z = data["Z_value"]

            # Create a 3D scatter plot
            self.ax.scatter(data_X, data_Y, data_Z, c="b", marker="o")

        except:
            print("fail to read data in the table")

        self.canvas.draw()

    def insert_row(self):
        # get number from text editor
        insert_x = self.ui.ted_x.toPlainText()
        insert_y = self.ui.ted_y.toPlainText()
        insert_z = self.ui.ted_z.toPlainText()

        if (
            insert_x.replace(".", "").replace("-", "").isdigit()
            and insert_y.replace(".", "").replace("-", "").isdigit()
            and insert_z.replace(".", "").replace("-", "").isdigit()
        ):
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

            # change tab in the tab table from default to my list
            self.ui.twg_table.setCurrentIndex(1)
        else:
            self.printLog(
                self.ui.tbx_log, "Error on input. Include alphabets or empty input"
            )

    def clear_table(self):
        # read which tab is on now
        tabIndex = self.ui.twg_table.currentIndex()

        if tabIndex == 0:
            table = self.ui.tbw_default
        elif tabIndex == 1:
            table = self.ui.tbw_mylist

        table.setRowCount(0)  # Remove all rows from the table

    def writeDefaultTable(self, data):
        df = pd.DataFrame(data)

        try:
            self.ui.tbw_default.setRowCount(df.shape[0])
            self.ui.tbw_default.setColumnCount(df.shape[1])

            # Populate the table with DataFrame data
            for i, row in df.iterrows():
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.ui.tbw_default.setItem(i, j, item)

            # change tab in the tab table to default
            self.ui.twg_table.setCurrentIndex(0)
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
        global robot

        NonNumericExist = 0
        robotSpeed = [75, 25, 50, 25]
        points = []
        laser_data = []
        visitedOrigin = False

        self.ui.btn_Stop.setEnabled(True)

        # connect Yumi
        robot = self.connectYumi()

        # connect Laser
        if laserON == 1:
            laser = self.connectLaser()

        # read which tab is on now
        tabIndex = self.ui.twg_table.currentIndex()

        if tabIndex == 0:
            table = self.ui.tbw_default
        elif tabIndex == 1:
            table = self.ui.tbw_mylist

        # Generate points for laser scanning if no item in the table or read data from table
        if table.rowCount() == 0:
            points = self.autoGenPoints()
        else:
            self.printLog(self.ui.tbx_log, "Checking items in the table...")

            for row in range(table.rowCount()):
                row_data = []
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    if item is not None:
                        if self.isNumber(item.text()):
                            row_data.append(float(item.text()))
                        else:
                            message = f"The item [{row + 1},{column + 1}] include is non-numeric value."
                            self.printLog(self.ui.tbx_log, message)
                            NonNumericExist = 1
                            break

            points.append(row_data)

        self.writeDefaultTable(points)

        # check status before start scanning
        if (NonNumericExist == 0) and (robot != None):
            # Robot setting
            robot_Control.set_Reference_Coordinate_System(robot, [0, 0, 758.01])

            robot_Control.set_Robot_Tool(robot, 1)

            robot_Control.set_Robot_Speed(robot, robotSpeed)

            # move to default position (initial position)
            robot_Control.return_Robot_To_Start(robot)

            # move robot to scanning points
            for point in points:
                if round(point[0][0], 4) != 0 or round(point[0][1], 4):
                    print(point)
                    robot_Control.move_Robot_Linear(robot, point)
                    sleep(0.5)
                    print(
                        "Robot Coordinate: ",
                        robot_Control.fetch_Robot_Coordinates(robot),
                    )

                elif not visitedOrigin:
                    print(point)
                    robot_Control.move_Robot_Linear(robot, point)
                    sleep(0.5)
                    print(
                        "Robot Coordinate: ",
                        robot_Control.fetch_Robot_Coordinates(robot),
                    )
                    visitedOrigin = True
                else:
                    print("Skipping origin...")

                if laserON == 1:
                    while not laser.laserOn():
                        continue

                    laser_point = laser.measure()
                    if isinstance(laser_point, float):
                        laser_data.append(
                            generate_scan_points.transform_laser_distance(
                                point, laser_point
                            )
                        )

                    while not laser.laserOff():
                        continue

                    self.endEffectorPos(
                        self.ax, laser_x, laser_y, laser_z, laser_point
                    )  # plot the end-effector position
                else:
                    self.endEffectorPos(
                        self.ax, laser_x, laser_y, laser_z, None
                    )  # plot the end-effector position

            robot_Control.return_Robot_To_Start(robot)

            # Write laser data to the default table
            self.writeDefaultTable(laser_data)

            # Plot the point cloud
            self.updatePlot()

            # 3D reconstruction
            # self.reconstruction3D(laser_data)

            self.printLog(self.ui.tbx_log, "Scanning complete")

        else:
            self.printLog(self.ui.tbx_log, "Scanning breaks.")

    def isNumber(self, text):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def connectYumi(self):
        try:
            robot = abb.Robot()
            self.printLog(self.ui.tbx_log, "Connect to the yumi robot arm")
            return robot
        except:
            self.printLog(self.ui.tbx_log, "unable to connect to the robot arm")
            return None

    def connectLaser(self):
        try:
            laser = optoNCDT1402.optoNCDT1402(
                "/dev/ttyUSB0"
            )  # Serial port of the Raspberry
            transistor.init()
            self.printLog(self.ui.tbx_log, "Connect to the laser")
            return laser
        except:
            self.printLog(self.ui.tbx_log, "unable to connect to the laser")
            return None

    def reconstruction3D(self, data):
        step_down = 0.005  # Step size for spline interpolation with x,y in Z direction. The smaller this value is, the more values will be added, duh.
        totalTime = time.time()
        t = time.time()

        data_X = data["X_value"]  # Reorganize the data into rows
        data_Y = data["Y_value"]
        data_Z = data["Z_value"]

        try:
            ##Runs the spline in z direction
            newData_X, newData_Y, newData_Z = spline.spline_xy(
                data_X, data_Y, data_Z, step_down
            )
        except:
            self.printLog(self.ui.tbx_log, "No newData")
            return None

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

        # surface_Reconstruction.delaunay_original(points, save)  ##tight cocone variant
        # surface_Reconstruction.alpha_Shape(points,save)
        # surface_Reconstruction.ball_Pivoting(points,save)
        # surface_Reconstruction.poisson_surfRecon(points, save)

        totalElapsed = time.time() - totalTime
        print("Time to complete Sample + reconstruction : ", totalElapsed)

    def autoGenPoints(self):
        circle_radius = self.ui.spb_circle_radius.value()
        z_stepsize = self.ui.spb_z_stepsize.value()
        max_depth = self.ui.spb_max_depth.value()
        azimuthPoints = self.ui.spb_azimuthPoints.value()
        offset = self.ui.spb_offset.value()
        elevationPoints = self.ui.spb_elevationPoints.value()
        zMin = self.ui.spb_zMin.value()
        laser_angle = self.ui.spb_laser_angle.value()

        while not -90 <= laser_angle <= 90:
            if laser_angle < 0:
                laser_angle = get_numeric_input(
                    "The angle of the end effector to point the laser upwards by:",
                    negative=True,
                    allow_float=True,
                )
            else:
                laser_angle = get_numeric_input(
                    "The angle of the end effector to point the laser upwards by:",
                    negative=False,
                    allow_float=True,
                )

        """
        circle_radius = 120
        z_stepsize = 10
        max_depth = -60
        azimuthPoints = 16
        offset = -60
        elevationPoints = 5
        zMin = -90
        laser_angle = 60
        """

        if self.ui.cbx_scanningMode.currentText() == "Cylinder":
            points = generate_scan_points.generate_scan_points_cylinder(
                circle_radius, z_stepsize, max_depth, azimuthPoints, offset, laser_angle
            )
            return points
        elif self.ui.cbx_scanningMode.currentText() == "Halve sphere":
            points = generate_scan_points.generate_scan_points_halfsphere(
                circle_radius, azimuthPoints, elevationPoints, zMin, offset
            )
            return points

    def MoveLinearActuator(self, choice):
        if linearActuator == 1:
            total_steps_changes = self.ui.spb_linearMoveTo.value() * 100

            # For control the values between 0 < x < 10000
            if total_steps_changes < 0:
                total_steps_changes = 0
            elif total_steps_changes > 10000:
                total_steps_changes = 10000

            if choice == "1":
                total_steps_changes = linearController.move_to_desired_location_upwards(
                    total_steps_changes
                )

            elif choice == "2":
                linearController.move_to_zeroLocation(total_steps_changes)
                total_steps_changes = 0

            elif choice == "3":
                linearController.move_up_1mm()
                total_steps_changes = total_steps_changes + 100

                # for every move_up function the total_steps_changes are added with 100 steps = 1mm
            elif choice == "4":
                linearController.move_down_1mm()
                total_steps_changes = total_steps_changes - 100

            self.ui.label_linear_pos.setText(f"position: {total_steps_changes/100} mm")
            self.ui.spb_linearMoveTo.setValue(total_steps_changes / 100)

    def stopScan(self):
        global robot

        if not robot == None:
            robot.close()


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
