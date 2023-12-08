##
# Modules
##
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from threading import Semaphore

#Object reconstruction
from zvb.titi_bakonkadonk_brest_8008_GUI import *

from GUI import ScanningSystem
from GUI.GUIFunctions import *
from GUI import ClassGUI
from RobotArm.scan_breast_phantom import scan_points, calibration, microMoveForRobot
from RobotArm import generate_scan_points

#linear actuator
import LinearActuator.linearActuatorController as linearController

class Thread_Scanning(QThread):
    finished = pyqtSignal()
    printText = pyqtSignal(str)
    disableButtons = pyqtSignal(bool)
    displayPointClound = pyqtSignal()

    def __init__(self,
                ScanSetting,
                scanModeIndex,
                classdata,
                radius,
                z_stepsize,
                azimuth_points,
                z_offset,
                elevation_points,
                z_min,
                laser_angle,
                laser_distance,
                resultTable,
                positionTable,
                log,
                spb_laser_distance, 
                label_x_RobPos, 
                label_y_RobPos,
                label_z_RobPos,
                label_dist_laser,
                label_x_Surface,
                label_y_Surface,
                label_z_Surface,
                network_ax, 
                canvasNetwork, 
                cbx_S33, 
                cbx_S32, 
                cbx_S23, 
                cbx_S22
                ):
        super().__init__()
        self.ScanSetting = ScanSetting
        self.scanModeIndex = scanModeIndex
        self.classdata = classdata
        self.radius = radius
        self.z_stepsize = z_stepsize
        self.azimuth_points = azimuth_points
        self.z_offset = z_offset
        self.elevation_points = elevation_points
        self.z_min = z_min
        self.laser_angle = laser_angle
        self.distance = laser_distance
        self.tableResult = resultTable
        self.tablePosition = positionTable
        self.logbox = log
        self.spb_laser_distance = spb_laser_distance
        self.label_x_RobPos = label_x_RobPos
        self.label_y_RobPos = label_y_RobPos
        self.label_z_RobPos = label_z_RobPos
        self.label_dist_laser = label_dist_laser
        self.label_x_Surface = label_x_Surface
        self.label_y_Surface = label_y_Surface
        self.label_z_Surface = label_z_Surface
        self.network_ax = network_ax
        self.canvasNetwork = canvasNetwork
        self.cbx_S33 = cbx_S33
        self.cbx_S32 = cbx_S32
        self.cbx_S23 = cbx_S23
        self.cbx_S22 = cbx_S22

    def run(self):
        self.scanMode()
        self.finished.emit()
    
    def stopNow(self):
        self.terminate()
        self.wait()

    def scanMode(self):
        i = 0
        
        # read which scanning mode tab is on now
        tabIndex = self.ScanSetting

        #Disable buttons
        self.disableButtons.emit(True)
        
        # Generate points for laser scanning if no item in the table or read data from table
        if tabIndex == 0:

            self.printText.emit("Auto generate scanning points and scanning...")

            if self.scanModeIndex == 0:  # Cylinder   
                self.printText.emit(f"Cylinder scan with quaternion: {self.classdata.quaternion}")
   
                result = scan_points(self.classdata.quaternion, self.radius, self.z_stepsize, self.z_min, self.azimuth_points, self.z_offset, self.laser_angle)

            elif self.scanModeIndex == 1:  # halve sphere
                self.printText.emit(f"Halve sphere scan with quaternion: {self.classdata.quaternion}")

                result = scan_points(self.classdata.quaternion, self.radius, self.azimuth_points, self.elevation_points, self.z_min, self.z_offset)
            
            writeResultToTable(result, self.tableResult)
            self.printText.emit("Scanning Finished.")
            self.displayPointClound.emit()
            self.classdata.mesh = recon3D(result)
            self.printText.emit("3D mesh created.")
        else:
            
            Visa_instrument= mw_init()  #initial visa instrument

            # Check if it is empty in the position list or not
            if not self.tablePosition.rowCount() == 0:
                self.printText.emit("Reading position list...")

                #read items in the manual input position table
                positions = readDataFromTable(self.tablePosition, self.logbox)

                #Generate moving data and move robot
                antenna_points, antenna_q = mw_boob(self.classdata.mesh, positions, self.distance, self.classdata.quaternion)

                robot = connectRobot(self.classdata.quaternion)

                for point, q in zip(antenna_points, antenna_q):
                    MoveRobotLinear(robot, point, q)             
                    freq, data_33, data_32, data_23, data_22 = networkMeasure(Visa_instrument,  i)
                    plotNetworkAnalyserDiagram(self.network_ax, self.canvasNetwork, self.cbx_S33, self.cbx_S32, self.cbx_S23, self.cbx_S22, freq, data_33, data_32, data_23, data_22)
                                 
                    changeLabels(antenna_points, [positions[i]],self.spb_laser_distance.value(), 
                        self.label_x_RobPos, self.label_y_RobPos, self.label_z_RobPos, self.label_dist_laser,
                        self.label_x_Surface, self.label_y_Surface,self.label_z_Surface)

                    i += 1

                closeRobot(robot)

                self.printText.emit("Moving Finished.")
                self.displayPointClound.emit()
            else:
                self.printText.emit("Perform microwave measurement without moving.")
                freq, data_33, data_32, data_23, data_22 = networkMeasure(Visa_instrument)
                plotNetworkAnalyserDiagram(self.network_ax, self.canvasNetwork, self.cbx_S33, self.cbx_S32, self.cbx_S23, self.cbx_S22, freq, data_33, data_32, data_23, data_22)

        #Enable buttons
        self.disableButtons.emit(False)
     
#Thread for calibration    
class Thread_Calibration(QThread):
    #connect functions from main thread
    finished = pyqtSignal()
    printText = pyqtSignal(str)
    disableButtons = pyqtSignal(bool)

    #Get values from main thread
    def __init__(self, classdata, log):
        super().__init__()
        self.classdata = classdata
        self.logbox = log

    def run(self):
        #run calibration
        self.disableButtons.emit(True)
        self.printText.emit("Calibration runs.")
        Newquaternion = calibration()
        self.classdata.quaternion = self.classdata.changeQua(Newquaternion)
        self.printText.emit(f"New calibration: {self.classdata.quaternion}")
        self.printText.emit("Calibration finished!")
        self.disableButtons.emit(False)
    
    def stopNow(self):
        self.terminate() #Close the thread
        self.wait()

class Thread_LinearAcutator(QThread):
    sem_protection = Semaphore(1)

    def __init__(self, label_linear_pos,spb_LinearMoveTo):
        super().__init__()
        self.label_PosNow = label_linear_pos
        self.spb_PosGoal = spb_LinearMoveTo
        self.actuator = linearController.linear_actuator()
        
    def run(self):
        pass

    def MoveLinearActuatorToPosition(self):
        self.sem_protection.acquire()
        total_steps_changes = self.spb_PosGoal.value() 
        current_position = int(self.label_PosNow.text())
        
        if total_steps_changes > current_position:
            UpOrDown = 1
        else:
            UpOrDown = 2

        self.actuator.move_to_desired_location(current_position, total_steps_changes, UpOrDown)
        steps = total_steps_changes
        changeLinearActuatorSteps(steps, self.label_PosNow, self.spb_PosGoal)

        self.sem_protection.release()

    def MoveLinearActuatorDown(self):
        self.sem_protection.acquire()
        
        steps = self.actuator.move_down_1mm(self.spb_PosGoal.value())
        changeLinearActuatorSteps(steps, self.label_PosNow, self.spb_PosGoal)

        self.sem_protection.release()

    def MoveLinearActuatorUp(self):
        self.sem_protection.acquire()

        steps = self.actuator.move_up_1mm(self.spb_PosGoal.value())
        changeLinearActuatorSteps(steps, self.label_PosNow, self.spb_PosGoal)

        self.sem_protection.release()

    def setStepToZero(self):
        self.sem_protection.acquire()
        changeLinearActuatorSteps(0, self.label_PosNow, self.spb_PosGoal)
        self.sem_protection.release()

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ScanningSystem.Ui_MainWindow()
        self.ui.setupUi(self)

        # button functions
        self.ui.btn_Load.pressed.connect(self.loadButton)
        self.ui.btn_Save.pressed.connect(self.saveButton)
        self.ui.btn_Scan.pressed.connect(self.scanButton)
        self.ui.btn_Stop.pressed.connect(self.stopButton)
        self.ui.btn_Calibration.pressed.connect(self.calibrationButton)

        self.ui.btn_input.pressed.connect(self.inputButton)
        self.ui.btn_clearTable.pressed.connect(self.clearButton)

        self.ui.btn_xUp.pressed.connect(self.MoveRobotArm_XUp)
        self.ui.btn_xDown.pressed.connect(self.MoveRobotArm_XDown)
        self.ui.btn_yUp.pressed.connect(self.MoveRobotArm_YUp)
        self.ui.btn_yDown.pressed.connect(self.MoveRobotArm_YDown)
        self.ui.btn_zUp.pressed.connect(self.MoveRobotArm_ZUp)
        self.ui.btn_zDown.pressed.connect(self.MoveRobotArm_ZDown)

        self.ui.btn_linear_moveto.pressed.connect(self.moveLinearToPositionButton)
        self.ui.btn_linear_up.pressed.connect(self.moveLinearUpButton)
        self.ui.btn_linear_down.pressed.connect(self.moveLinearDownButton)
        self.ui.btn_LinearCalibration.pressed.connect(self.linearCalibrationButton)

        self.ui.btn_Plot.pressed.connect(self.plotButton)

        # Add matplotlib in scanning viewer
        self.ax, self.canvas = add3DPlotInGUI(self.ui.viewer_scanning)

        # Add matplotlib in scanning viewer
        self.network_ax, self.canvasNetwork = add2DDiagramInGUI(self.ui.viewer_network)

        #Linear actuator
        self.LinearActuator_thread = Thread_LinearAcutator(self.ui.label_linear_pos, self.ui.spb_linearMoveTo)
        self.LinearActuator_thread.start()

        #Class
        self.classdata = ClassGUI.class_GUI()

        # print message in the text browser
        self.ui.tbx_log.append("System open")

    # function: print message in the text browser
    def printLog(self, message):
        self.ui.tbx_log.append(message)
    

    #######Button Functions###########
    #function load file
    def loadButton(self):
        load_model(self.ui.tbw_result, self.ui.tbx_log)  # Load the data from .mat file

        if self.ui.tbw_result.rowCount() != 0:
            result = readDataFromTable(self.ui.tbw_result, self.ui.tbx_log)
            self.updatePlot()  # Plot the figure after spline
            self.classdata.mesh = recon3D(result)

    #funciton: save file
    def saveButton(self):
        save_model(self.ui.tbw_result, self.ui.tbx_log)

    #function: add item to table and display the positions
    def inputButton(self):
        insertDataToTable(self.ui.ted_x, self.ui.ted_y, self.ui.ted_z, self.ui.tbw_positionlist, self.ui.twg_table, self.ui.tbx_log)
        self.updatePlot()
        
    #function: clear the positions list
    def clearButton(self):
        # Remove all positions from the positions list table
        self.ui.tbw_positionlist.setRowCount(0)

    #function: start scanning
    def scanButton(self):
        #start scanning (new thread)
        #Create a worker object
        self.worker_thread = Thread_Scanning(
            self.ui.twg_scanSetting.currentIndex(),
            self.ui.twg_scanningMode.currentIndex(),
            self.classdata,
            self.ui.spb_circle_radius.value(),
            self.ui.spb_z_stepsize.value(),
            self.ui.spb_azimuthPoints.value(),
            self.ui.spb_offset.value(),
            self.ui.spb_elevationPoints.value(),
            self.ui.spb_zMin.value(),
            self.ui.spb_laser_angle.value(),
            self.ui.spb_laser_distance.value(),
            self.ui.tbw_result,
            self.ui.tbw_positionlist,
            self.ui.tbx_log,
            self.ui.spb_laser_distance, 
            self.ui.label_x_RobPos, 
            self.ui.label_y_RobPos,
            self.ui.label_z_RobPos,
            self.ui.label_dist_laser,
            self.ui.label_x_Surface, 
            self.ui.label_y_Surface,
            self.ui.label_z_Surface,
            self.network_ax, 
            self.canvasNetwork, 
            self.ui.cbx_S33, 
            self.ui.cbx_S32, 
            self.ui.cbx_S23, 
            self.ui.cbx_S22
        )

        #Connect signals and slots
        self.worker_thread.printText.connect(self.printLog)
        self.worker_thread.displayPointClound.connect(self.updatePlot)
        self.worker_thread.disableButtons.connect(self.disableButton)
        
        #Delete the thread after work is done
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        
        self.worker_thread.start()

    #function: stop scanning
    def stopButton(self):
        self.worker_thread.stopNow()
        self.ui.tbx_log.append("Emergency Stop!")

    #function: calibration
    def calibrationButton(self):
        #start calibration (new thread)
        self.worker_thread = Thread_Calibration(self.classdata, self.ui.tbx_log)

        self.worker_thread.disableButtons.connect(self.disableButton)
        self.worker_thread.printText.connect(self.printLog)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def MoveRobotArm_XUp(self):
        self.MicroMovement(1)

    def MoveRobotArm_YUp(self):
        self.MicroMovement(3)

    def MoveRobotArm_ZUp(self):
        self.MicroMovement(5)

    def MoveRobotArm_XDown(self):
        self.MicroMovement(2)

    def MoveRobotArm_YDown(self):
        self.MicroMovement(4)

    def MoveRobotArm_ZDown(self):
        self.MicroMovement(6)
    
    def moveLinearToPositionButton(self):
        self.LinearActuator_thread.MoveLinearActuatorToPosition()

    def moveLinearUpButton(self):
        self.LinearActuator_thread.MoveLinearActuatorUp()
    
    def moveLinearDownButton(self):
        self.LinearActuator_thread.MoveLinearActuatorDown()

    def linearCalibrationButton(self):
        self.LinearActuator_thread.setStepToZero()

    def plotButton(self):       
        freq, data_33, data_32, data_23, data_22 = loadMWMeasurement()
        plotNetworkAnalyserDiagram(self.network_ax, self.canvasNetwork, self.ui.cbx_S33, self.ui.cbx_S32, self.ui.cbx_S23, self.ui.cbx_S22, freq, data_33, data_32, data_23, data_22)

    #Function for disable all buttons affect robot arm expect stop button 
    def disableButton(self, ONorOFF):
        self.ui.btn_Scan.setDisabled(ONorOFF)
        self.ui.btn_Save.setDisabled(ONorOFF)
        self.ui.btn_Load.setDisabled(ONorOFF)
        self.ui.btn_Calibration.setDisabled(ONorOFF)
        self.ui.btn_input.setDisabled(ONorOFF)
        self.ui.btn_clearTable.setDisabled(ONorOFF)
        self.ui.btn_xUp.setDisabled(ONorOFF)
        self.ui.btn_xDown.setDisabled(ONorOFF)
        self.ui.btn_xUp.setDisabled(ONorOFF)
        self.ui.btn_xDown.setDisabled(ONorOFF)
        self.ui.btn_yUp.setDisabled(ONorOFF)
        self.ui.btn_yDown.setDisabled(ONorOFF)
        self.ui.btn_zUp.setDisabled(ONorOFF)
        self.ui.btn_zDown.setDisabled(ONorOFF)
        self.ui.btn_Plot.setDisabled(ONorOFF)
        
    # functions: move robot arm position
    def MicroMovement(self, buttonNumber):
        surfacepoint = [float(self.ui.label_x_Surface.text()), float(self.ui.label_y_Surface.text()), float(self.ui.label_z_Surface.text())]
        #antenna_points, antenna_q, surfacePos = microMoveForRobot(decision, self.classdata.mesh, point, self.ui.spb_laser_distance.value())

        # increase or decrease values
        if buttonNumber == 1:  # X_up
            surfacepoint[0] = surfacepoint[0] + 1.0
        elif buttonNumber == 2:  # X_down
            surfacepoint[0] = surfacepoint[0] - 1.0
        elif buttonNumber == 3:  # Y_up
            surfacepoint[1] = surfacepoint[1] + 1.0
        elif buttonNumber == 4:  # Y_down
            surfacepoint[1] = surfacepoint[1] - 1.0
        elif buttonNumber == 5:  # Z_up
            surfacepoint[2] = surfacepoint[2] + 1.0
        elif buttonNumber == 6:  # Z_down
            surfacepoint[2] = surfacepoint[2] - 1.0

        Newpoint = [surfacepoint]



        antenna_points, antenna_q = mw_boob(self.classdata.mesh, Newpoint, self.ui.spb_laser_distance.value(), self.classdata.quaternion)

        for point, q in zip(antenna_points, antenna_q):
         #   mw_micromovement(point, q)
        
        #MoveRobotLinear(robot, antenna_points, antenna_q)  
  
            changeLabels([point], Newpoint, self.ui.spb_laser_distance.value(), 
                        self.ui.label_x_RobPos, self.ui.label_y_RobPos,self.ui.label_z_RobPos, self.ui.label_dist_laser,
                        self.ui.label_x_Surface, self.ui.label_y_Surface,self.ui.label_z_Surface)
        
        #closeRobot(robot)
        # Clean the axis
        self.ax.cla()

        # Set axis labels
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        #plot result
        plotData(self.ui.tbw_result, self.ax, "b", self.ui.tbx_log)

        #plot positions in manually inputs
        plotData(self.ui.tbw_positionlist, self.ax, "g", self.ui.tbx_log)
        
        self.ax.scatter(point[0], point[1],point[2], "r")

        self.canvas.draw()
 
    # function: laser position
    def endEffectorPos(self, robpos, surfacepos):
        #display robot value and laser distance
        self.ui.label_x_RobPos.setText(str(robpos[0][0]))
        self.ui.label_y_RobPos.setText(str(robpos[0][1]))
        self.ui.label_z_RobPos.setText(str(robpos[0][2]))
        self.ui.label_dist_laser.setText(str(self.ui.spb_laser_distance.value()))

        #display surface point
        self.ui.label_x_Surface.setText(str(surfacepos[0]))
        self.ui.label_y_Surface.setText(str(surfacepos[1]))
        self.ui.label_z_Surface.setText(str(surfacepos[2]))
    
    #function: update the plot
    def updatePlot(self):
        # Clean the axis
        self.ax.cla()

        # Set axis labels
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        #plot result
        plotData(self.ui.tbw_result, self.ax, "b", self.ui.tbx_log)

        #plot positions in manually inputs
        plotData(self.ui.tbw_positionlist, self.ax, "g", self.ui.tbx_log)

        self.canvas.draw()

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())