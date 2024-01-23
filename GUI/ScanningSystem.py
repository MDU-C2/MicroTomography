# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI\ScanningSystem_ver_1.0.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1763, 1232)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_x_RobPos = QtWidgets.QLabel(self.centralwidget)
        self.label_x_RobPos.setGeometry(QtCore.QRect(250, 570, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_x_RobPos.setFont(font)
        self.label_x_RobPos.setObjectName("label_x_RobPos")
        self.label_y_RobPos = QtWidgets.QLabel(self.centralwidget)
        self.label_y_RobPos.setGeometry(QtCore.QRect(410, 570, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_y_RobPos.setFont(font)
        self.label_y_RobPos.setObjectName("label_y_RobPos")
        self.label_z_RobPos = QtWidgets.QLabel(self.centralwidget)
        self.label_z_RobPos.setGeometry(QtCore.QRect(570, 570, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_z_RobPos.setFont(font)
        self.label_z_RobPos.setObjectName("label_z_RobPos")
        self.label_d = QtWidgets.QLabel(self.centralwidget)
        self.label_d.setGeometry(QtCore.QRect(720, 570, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_d.setFont(font)
        self.label_d.setObjectName("label_d")
        self.tbx_log = QtWidgets.QTextBrowser(self.centralwidget)
        self.tbx_log.setGeometry(QtCore.QRect(30, 670, 351, 421))
        self.tbx_log.setObjectName("tbx_log")
        self.label_nonvalue_Log = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_Log.setGeometry(QtCore.QRect(30, 640, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_nonvalue_Log.setFont(font)
        self.label_nonvalue_Log.setWordWrap(False)
        self.label_nonvalue_Log.setObjectName("label_nonvalue_Log")
        self.btn_Scan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Scan.setGeometry(QtCore.QRect(920, 10, 111, 71))
        self.btn_Scan.setObjectName("btn_Scan")
        self.btn_Save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Save.setEnabled(True)
        self.btn_Save.setGeometry(QtCore.QRect(1160, 10, 111, 71))
        self.btn_Save.setObjectName("btn_Save")
        self.btn_Load = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Load.setGeometry(QtCore.QRect(1280, 10, 111, 71))
        self.btn_Load.setObjectName("btn_Load")
        self.btn_Stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Stop.setEnabled(True)
        self.btn_Stop.setGeometry(QtCore.QRect(1040, 10, 111, 71))
        self.btn_Stop.setAutoFillBackground(False)
        self.btn_Stop.setStyleSheet("")
        self.btn_Stop.setObjectName("btn_Stop")
        self.twg_table = QtWidgets.QTabWidget(self.centralwidget)
        self.twg_table.setGeometry(QtCore.QRect(910, 410, 621, 481))
        self.twg_table.setMinimumSize(QtCore.QSize(621, 0))
        self.twg_table.setObjectName("twg_table")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tbw_result = QtWidgets.QTableWidget(self.tab)
        self.tbw_result.setGeometry(QtCore.QRect(0, 0, 610, 450))
        self.tbw_result.setColumnCount(3)
        self.tbw_result.setObjectName("tbw_result")
        self.tbw_result.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbw_result.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbw_result.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbw_result.setHorizontalHeaderItem(2, item)
        self.twg_table.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tbw_positionlist = QtWidgets.QTableWidget(self.tab_2)
        self.tbw_positionlist.setGeometry(QtCore.QRect(0, 0, 610, 450))
        self.tbw_positionlist.setColumnCount(3)
        self.tbw_positionlist.setObjectName("tbw_positionlist")
        self.tbw_positionlist.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbw_positionlist.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbw_positionlist.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbw_positionlist.setHorizontalHeaderItem(2, item)
        self.twg_table.addTab(self.tab_2, "")
        self.viewer_scanning = QtWidgets.QWidget(self.centralwidget)
        self.viewer_scanning.setGeometry(QtCore.QRect(30, 9, 811, 551))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.viewer_scanning.setFont(font)
        self.viewer_scanning.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.viewer_scanning.setAutoFillBackground(False)
        self.viewer_scanning.setObjectName("viewer_scanning")
        self.btn_Calibration = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Calibration.setGeometry(QtCore.QRect(1400, 10, 111, 71))
        self.btn_Calibration.setObjectName("btn_Calibration")
        self.label_ScanningSetting = QtWidgets.QLabel(self.centralwidget)
        self.label_ScanningSetting.setGeometry(QtCore.QRect(910, 100, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ScanningSetting.setFont(font)
        self.label_ScanningSetting.setObjectName("label_ScanningSetting")
        self.label_RobotPosition = QtWidgets.QLabel(self.centralwidget)
        self.label_RobotPosition.setGeometry(QtCore.QRect(30, 570, 170, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_RobotPosition.setFont(font)
        self.label_RobotPosition.setObjectName("label_RobotPosition")
        self.label_SurfacePosition = QtWidgets.QLabel(self.centralwidget)
        self.label_SurfacePosition.setGeometry(QtCore.QRect(30, 610, 170, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_SurfacePosition.setFont(font)
        self.label_SurfacePosition.setObjectName("label_SurfacePosition")
        self.label_x_Surface = QtWidgets.QLabel(self.centralwidget)
        self.label_x_Surface.setGeometry(QtCore.QRect(250, 610, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_x_Surface.setFont(font)
        self.label_x_Surface.setObjectName("label_x_Surface")
        self.label_z_Surface = QtWidgets.QLabel(self.centralwidget)
        self.label_z_Surface.setGeometry(QtCore.QRect(570, 610, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_z_Surface.setFont(font)
        self.label_z_Surface.setObjectName("label_z_Surface")
        self.label_y_Surface = QtWidgets.QLabel(self.centralwidget)
        self.label_y_Surface.setGeometry(QtCore.QRect(410, 610, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_y_Surface.setFont(font)
        self.label_y_Surface.setObjectName("label_y_Surface")
        self.twg_ManualController = QtWidgets.QTabWidget(self.centralwidget)
        self.twg_ManualController.setGeometry(QtCore.QRect(950, 920, 541, 181))
        self.twg_ManualController.setObjectName("twg_ManualController")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.btn_zDown = QtWidgets.QPushButton(self.tab_5)
        self.btn_zDown.setGeometry(QtCore.QRect(310, 90, 93, 28))
        self.btn_zDown.setObjectName("btn_zDown")
        self.btn_yDown = QtWidgets.QPushButton(self.tab_5)
        self.btn_yDown.setGeometry(QtCore.QRect(170, 90, 93, 28))
        self.btn_yDown.setObjectName("btn_yDown")
        self.btn_xDown = QtWidgets.QPushButton(self.tab_5)
        self.btn_xDown.setGeometry(QtCore.QRect(30, 90, 93, 28))
        self.btn_xDown.setObjectName("btn_xDown")
        self.label_nonvalue_rob_x = QtWidgets.QLabel(self.tab_5)
        self.label_nonvalue_rob_x.setGeometry(QtCore.QRect(70, 10, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_rob_x.setFont(font)
        self.label_nonvalue_rob_x.setObjectName("label_nonvalue_rob_x")
        self.btn_xUp = QtWidgets.QPushButton(self.tab_5)
        self.btn_xUp.setGeometry(QtCore.QRect(30, 40, 93, 28))
        self.btn_xUp.setObjectName("btn_xUp")
        self.label_nonvalue_robz = QtWidgets.QLabel(self.tab_5)
        self.label_nonvalue_robz.setGeometry(QtCore.QRect(350, 10, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_robz.setFont(font)
        self.label_nonvalue_robz.setObjectName("label_nonvalue_robz")
        self.btn_zUp = QtWidgets.QPushButton(self.tab_5)
        self.btn_zUp.setGeometry(QtCore.QRect(310, 37, 93, 31))
        self.btn_zUp.setObjectName("btn_zUp")
        self.label_nonvalue_roby = QtWidgets.QLabel(self.tab_5)
        self.label_nonvalue_roby.setGeometry(QtCore.QRect(210, 10, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_roby.setFont(font)
        self.label_nonvalue_roby.setObjectName("label_nonvalue_roby")
        self.btn_yUp = QtWidgets.QPushButton(self.tab_5)
        self.btn_yUp.setGeometry(QtCore.QRect(170, 40, 93, 28))
        self.btn_yUp.setObjectName("btn_yUp")
        self.label_nonvalue_LinearActuator_2 = QtWidgets.QLabel(self.tab_5)
        self.label_nonvalue_LinearActuator_2.setGeometry(QtCore.QRect(440, 0, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_nonvalue_LinearActuator_2.setFont(font)
        self.label_nonvalue_LinearActuator_2.setObjectName("label_nonvalue_LinearActuator_2")
        self.twg_ManualController.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.label_linear_pos = QtWidgets.QLabel(self.tab_6)
        self.label_linear_pos.setGeometry(QtCore.QRect(170, 60, 141, 16))
        self.label_linear_pos.setObjectName("label_linear_pos")
        self.label_nonvalue_position = QtWidgets.QLabel(self.tab_6)
        self.label_nonvalue_position.setGeometry(QtCore.QRect(30, 60, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_position.setFont(font)
        self.label_nonvalue_position.setObjectName("label_nonvalue_position")
        self.spb_linearMoveTo = QtWidgets.QSpinBox(self.tab_6)
        self.spb_linearMoveTo.setGeometry(QtCore.QRect(170, 10, 161, 31))
        self.spb_linearMoveTo.setMaximum(100)
        self.spb_linearMoveTo.setObjectName("spb_linearMoveTo")
        self.label_nonvalue_LinearActuator = QtWidgets.QLabel(self.tab_6)
        self.label_nonvalue_LinearActuator.setGeometry(QtCore.QRect(470, 0, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_nonvalue_LinearActuator.setFont(font)
        self.label_nonvalue_LinearActuator.setObjectName("label_nonvalue_LinearActuator")
        self.btn_linear_moveto = QtWidgets.QPushButton(self.tab_6)
        self.btn_linear_moveto.setGeometry(QtCore.QRect(350, 10, 93, 28))
        self.btn_linear_moveto.setObjectName("btn_linear_moveto")
        self.label_nonvalue_linear_updown = QtWidgets.QLabel(self.tab_6)
        self.label_nonvalue_linear_updown.setGeometry(QtCore.QRect(30, 100, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_linear_updown.setFont(font)
        self.label_nonvalue_linear_updown.setObjectName("label_nonvalue_linear_updown")
        self.btn_linear_down = QtWidgets.QPushButton(self.tab_6)
        self.btn_linear_down.setGeometry(QtCore.QRect(260, 100, 93, 28))
        self.btn_linear_down.setObjectName("btn_linear_down")
        self.label_nonvalue_linear_moveto = QtWidgets.QLabel(self.tab_6)
        self.label_nonvalue_linear_moveto.setGeometry(QtCore.QRect(30, 10, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_linear_moveto.setFont(font)
        self.label_nonvalue_linear_moveto.setObjectName("label_nonvalue_linear_moveto")
        self.btn_linear_up = QtWidgets.QPushButton(self.tab_6)
        self.btn_linear_up.setGeometry(QtCore.QRect(140, 100, 93, 28))
        self.btn_linear_up.setObjectName("btn_linear_up")
        self.btn_LinearCalibration = QtWidgets.QPushButton(self.tab_6)
        self.btn_LinearCalibration.setGeometry(QtCore.QRect(350, 50, 93, 28))
        self.btn_LinearCalibration.setObjectName("btn_LinearCalibration")
        self.twg_ManualController.addTab(self.tab_6, "")
        self.label_robotMove = QtWidgets.QLabel(self.centralwidget)
        self.label_robotMove.setGeometry(QtCore.QRect(910, 890, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_robotMove.setFont(font)
        self.label_robotMove.setObjectName("label_robotMove")
        self.twg_scanSetting = QtWidgets.QTabWidget(self.centralwidget)
        self.twg_scanSetting.setGeometry(QtCore.QRect(900, 130, 651, 251))
        self.twg_scanSetting.setObjectName("twg_scanSetting")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.label_nonvalue_azimuthpoints = QtWidgets.QLabel(self.tab_7)
        self.label_nonvalue_azimuthpoints.setGeometry(QtCore.QRect(200, 10, 121, 31))
        self.label_nonvalue_azimuthpoints.setObjectName("label_nonvalue_azimuthpoints")
        self.twg_scanningMode = QtWidgets.QTabWidget(self.tab_7)
        self.twg_scanningMode.setGeometry(QtCore.QRect(20, 90, 521, 121))
        self.twg_scanningMode.setObjectName("twg_scanningMode")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_nonvalue_laser_angle = QtWidgets.QLabel(self.tab_3)
        self.label_nonvalue_laser_angle.setGeometry(QtCore.QRect(170, 0, 121, 31))
        self.label_nonvalue_laser_angle.setObjectName("label_nonvalue_laser_angle")
        self.spb_laser_angle = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.spb_laser_angle.setGeometry(QtCore.QRect(170, 40, 131, 41))
        self.spb_laser_angle.setDecimals(2)
        self.spb_laser_angle.setMinimum(-90.0)
        self.spb_laser_angle.setMaximum(90.0)
        self.spb_laser_angle.setSingleStep(1.0)
        self.spb_laser_angle.setProperty("value", 0.0)
        self.spb_laser_angle.setObjectName("spb_laser_angle")
        self.label_nonvalue_zstepsize = QtWidgets.QLabel(self.tab_3)
        self.label_nonvalue_zstepsize.setGeometry(QtCore.QRect(20, 0, 121, 31))
        self.label_nonvalue_zstepsize.setObjectName("label_nonvalue_zstepsize")
        self.spb_z_stepsize = QtWidgets.QSpinBox(self.tab_3)
        self.spb_z_stepsize.setGeometry(QtCore.QRect(20, 40, 131, 41))
        self.spb_z_stepsize.setMaximum(30)
        self.spb_z_stepsize.setProperty("value", 5)
        self.spb_z_stepsize.setObjectName("spb_z_stepsize")
        self.twg_scanningMode.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.spb_elevationPoints = QtWidgets.QSpinBox(self.tab_4)
        self.spb_elevationPoints.setGeometry(QtCore.QRect(20, 40, 131, 41))
        self.spb_elevationPoints.setMinimum(1)
        self.spb_elevationPoints.setMaximum(300)
        self.spb_elevationPoints.setProperty("value", 5)
        self.spb_elevationPoints.setObjectName("spb_elevationPoints")
        self.label_elevationPoints = QtWidgets.QLabel(self.tab_4)
        self.label_elevationPoints.setGeometry(QtCore.QRect(20, 0, 121, 31))
        self.label_elevationPoints.setObjectName("label_elevationPoints")
        self.twg_scanningMode.addTab(self.tab_4, "")
        self.label_nonvalue_offset = QtWidgets.QLabel(self.tab_7)
        self.label_nonvalue_offset.setGeometry(QtCore.QRect(350, 10, 121, 31))
        self.label_nonvalue_offset.setObjectName("label_nonvalue_offset")
        self.spb_azimuthPoints = QtWidgets.QSpinBox(self.tab_7)
        self.spb_azimuthPoints.setGeometry(QtCore.QRect(200, 40, 131, 41))
        self.spb_azimuthPoints.setMinimum(0)
        self.spb_azimuthPoints.setMaximum(359)
        self.spb_azimuthPoints.setProperty("value", 16)
        self.spb_azimuthPoints.setObjectName("spb_azimuthPoints")
        self.spb_circle_radius = QtWidgets.QDoubleSpinBox(self.tab_7)
        self.spb_circle_radius.setGeometry(QtCore.QRect(30, 40, 131, 41))
        self.spb_circle_radius.setDecimals(2)
        self.spb_circle_radius.setMinimum(10.0)
        self.spb_circle_radius.setMaximum(300.0)
        self.spb_circle_radius.setSingleStep(10.0)
        self.spb_circle_radius.setProperty("value", 120.0)
        self.spb_circle_radius.setObjectName("spb_circle_radius")
        self.spb_offset = QtWidgets.QDoubleSpinBox(self.tab_7)
        self.spb_offset.setGeometry(QtCore.QRect(350, 40, 131, 41))
        self.spb_offset.setDecimals(2)
        self.spb_offset.setMinimum(-300.0)
        self.spb_offset.setMaximum(300.0)
        self.spb_offset.setSingleStep(1.0)
        self.spb_offset.setProperty("value", -20.0)
        self.spb_offset.setObjectName("spb_offset")
        self.label_nonvalue_circleradius = QtWidgets.QLabel(self.tab_7)
        self.label_nonvalue_circleradius.setGeometry(QtCore.QRect(30, 10, 121, 31))
        self.label_nonvalue_circleradius.setObjectName("label_nonvalue_circleradius")
        self.label_nonvalue_zMin = QtWidgets.QLabel(self.tab_7)
        self.label_nonvalue_zMin.setGeometry(QtCore.QRect(500, 10, 121, 31))
        self.label_nonvalue_zMin.setObjectName("label_nonvalue_zMin")
        self.spb_zMin = QtWidgets.QDoubleSpinBox(self.tab_7)
        self.spb_zMin.setGeometry(QtCore.QRect(500, 40, 131, 41))
        self.spb_zMin.setMinimum(-200.0)
        self.spb_zMin.setMaximum(0.0)
        self.spb_zMin.setSingleStep(0.1)
        self.spb_zMin.setProperty("value", -60.0)
        self.spb_zMin.setObjectName("spb_zMin")
        self.twg_scanSetting.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.btn_clearTable = QtWidgets.QPushButton(self.tab_8)
        self.btn_clearTable.setGeometry(QtCore.QRect(490, 110, 93, 28))
        self.btn_clearTable.setObjectName("btn_clearTable")
        self.btn_input = QtWidgets.QPushButton(self.tab_8)
        self.btn_input.setGeometry(QtCore.QRect(490, 60, 91, 31))
        self.btn_input.setObjectName("btn_input")
        self.label_nonvalue_x = QtWidgets.QLabel(self.tab_8)
        self.label_nonvalue_x.setGeometry(QtCore.QRect(50, 60, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_x.setFont(font)
        self.label_nonvalue_x.setObjectName("label_nonvalue_x")
        self.label_nonvalue_y = QtWidgets.QLabel(self.tab_8)
        self.label_nonvalue_y.setGeometry(QtCore.QRect(180, 50, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_y.setFont(font)
        self.label_nonvalue_y.setObjectName("label_nonvalue_y")
        self.label_nonvalue_z = QtWidgets.QLabel(self.tab_8)
        self.label_nonvalue_z.setGeometry(QtCore.QRect(330, 50, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_z.setFont(font)
        self.label_nonvalue_z.setObjectName("label_nonvalue_z")
        self.ted_x = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.ted_x.setGeometry(QtCore.QRect(70, 50, 91, 41))
        self.ted_x.setDecimals(2)
        self.ted_x.setMinimum(-300.0)
        self.ted_x.setMaximum(300.0)
        self.ted_x.setSingleStep(10.0)
        self.ted_x.setProperty("value", 120.0)
        self.ted_x.setObjectName("ted_x")
        self.ted_y = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.ted_y.setGeometry(QtCore.QRect(210, 50, 91, 41))
        self.ted_y.setDecimals(2)
        self.ted_y.setMinimum(-300.0)
        self.ted_y.setMaximum(300.0)
        self.ted_y.setSingleStep(10.0)
        self.ted_y.setProperty("value", 120.0)
        self.ted_y.setObjectName("ted_y")
        self.ted_z = QtWidgets.QDoubleSpinBox(self.tab_8)
        self.ted_z.setGeometry(QtCore.QRect(350, 50, 91, 41))
        self.ted_z.setDecimals(2)
        self.ted_z.setMinimum(-100.0)
        self.ted_z.setMaximum(0.0)
        self.ted_z.setSingleStep(10.0)
        self.ted_z.setProperty("value", -30.0)
        self.ted_z.setObjectName("ted_z")
        self.twg_scanSetting.addTab(self.tab_8, "")
        self.label_ScanningSetting_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_ScanningSetting_2.setGeometry(QtCore.QRect(910, 380, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ScanningSetting_2.setFont(font)
        self.label_ScanningSetting_2.setObjectName("label_ScanningSetting_2")
        self.label_nonvalue_distance = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_distance.setGeometry(QtCore.QRect(1320, 110, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_distance.setFont(font)
        self.label_nonvalue_distance.setObjectName("label_nonvalue_distance")
        self.spb_laser_distance = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spb_laser_distance.setGeometry(QtCore.QRect(1400, 100, 131, 41))
        self.spb_laser_distance.setDecimals(2)
        self.spb_laser_distance.setMinimum(0.0)
        self.spb_laser_distance.setMaximum(100.0)
        self.spb_laser_distance.setSingleStep(1.0)
        self.spb_laser_distance.setProperty("value", 2.0)
        self.spb_laser_distance.setObjectName("spb_laser_distance")
        self.label_nonvalue_netwrok = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_netwrok.setGeometry(QtCore.QRect(410, 640, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_nonvalue_netwrok.setFont(font)
        self.label_nonvalue_netwrok.setWordWrap(False)
        self.label_nonvalue_netwrok.setObjectName("label_nonvalue_netwrok")
        self.viewer_network = QtWidgets.QWidget(self.centralwidget)
        self.viewer_network.setGeometry(QtCore.QRect(410, 670, 471, 421))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.viewer_network.setFont(font)
        self.viewer_network.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.viewer_network.setAutoFillBackground(False)
        self.viewer_network.setObjectName("viewer_network")
        self.label_nonvalue_x_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_x_2.setGeometry(QtCore.QRect(220, 570, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_x_2.setFont(font)
        self.label_nonvalue_x_2.setObjectName("label_nonvalue_x_2")
        self.label_nonvalue_y_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_y_3.setGeometry(QtCore.QRect(380, 610, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_y_3.setFont(font)
        self.label_nonvalue_y_3.setObjectName("label_nonvalue_y_3")
        self.label_nonvalue_x_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_x_3.setGeometry(QtCore.QRect(220, 610, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_x_3.setFont(font)
        self.label_nonvalue_x_3.setObjectName("label_nonvalue_x_3")
        self.label_nonvalue_y_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_y_2.setGeometry(QtCore.QRect(380, 570, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_y_2.setFont(font)
        self.label_nonvalue_y_2.setObjectName("label_nonvalue_y_2")
        self.label_nonvalue_z_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_z_3.setGeometry(QtCore.QRect(540, 610, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_z_3.setFont(font)
        self.label_nonvalue_z_3.setObjectName("label_nonvalue_z_3")
        self.label_nonvalue_z_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_nonvalue_z_2.setGeometry(QtCore.QRect(540, 570, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_nonvalue_z_2.setFont(font)
        self.label_nonvalue_z_2.setObjectName("label_nonvalue_z_2")
        self.label_dist_laser = QtWidgets.QLabel(self.centralwidget)
        self.label_dist_laser.setGeometry(QtCore.QRect(800, 570, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_dist_laser.setFont(font)
        self.label_dist_laser.setObjectName("label_dist_laser")
        self.cbx_S33 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_S33.setGeometry(QtCore.QRect(510, 650, 51, 16))
        self.cbx_S33.setChecked(True)
        self.cbx_S33.setTristate(False)
        self.cbx_S33.setObjectName("cbx_S33")
        self.cbx_S32 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_S32.setGeometry(QtCore.QRect(570, 650, 51, 16))
        self.cbx_S32.setChecked(True)
        self.cbx_S32.setObjectName("cbx_S32")
        self.cbx_S23 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_S23.setGeometry(QtCore.QRect(630, 650, 51, 16))
        self.cbx_S23.setChecked(True)
        self.cbx_S23.setObjectName("cbx_S23")
        self.cbx_S22 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_S22.setGeometry(QtCore.QRect(690, 650, 51, 16))
        self.cbx_S22.setChecked(True)
        self.cbx_S22.setObjectName("cbx_S22")
        self.btn_Plot = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Plot.setGeometry(QtCore.QRect(740, 650, 81, 21))
        self.btn_Plot.setObjectName("btn_Plot")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.twg_table.setCurrentIndex(0)
        self.twg_ManualController.setCurrentIndex(1)
        self.twg_scanSetting.setCurrentIndex(1)
        self.twg_scanningMode.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_x_RobPos.setText(_translate("MainWindow", "0"))
        self.label_y_RobPos.setText(_translate("MainWindow", "0"))
        self.label_z_RobPos.setText(_translate("MainWindow", "0"))
        self.label_d.setText(_translate("MainWindow", "Distance:"))
        self.label_nonvalue_Log.setText(_translate("MainWindow", "Log:"))
        self.btn_Scan.setText(_translate("MainWindow", "Scan"))
        self.btn_Save.setText(_translate("MainWindow", "Save"))
        self.btn_Load.setText(_translate("MainWindow", "Load"))
        self.btn_Stop.setText(_translate("MainWindow", "Stop"))
        item = self.tbw_result.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "X"))
        item = self.tbw_result.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Y"))
        item = self.tbw_result.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Z"))
        self.twg_table.setTabText(self.twg_table.indexOf(self.tab), _translate("MainWindow", "Scanning Result"))
        item = self.tbw_positionlist.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "X"))
        item = self.tbw_positionlist.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Y"))
        item = self.tbw_positionlist.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Z"))
        self.twg_table.setTabText(self.twg_table.indexOf(self.tab_2), _translate("MainWindow", "Scanning Position list"))
        self.btn_Calibration.setText(_translate("MainWindow", "Calibration"))
        self.label_ScanningSetting.setText(_translate("MainWindow", "Scanning Settings:"))
        self.label_RobotPosition.setText(_translate("MainWindow", "Robot position:"))
        self.label_SurfacePosition.setText(_translate("MainWindow", "Surface position:"))
        self.label_x_Surface.setText(_translate("MainWindow", "0"))
        self.label_z_Surface.setText(_translate("MainWindow", "0"))
        self.label_y_Surface.setText(_translate("MainWindow", "0"))
        self.btn_zDown.setText(_translate("MainWindow", "Down"))
        self.btn_yDown.setText(_translate("MainWindow", "Down"))
        self.btn_xDown.setText(_translate("MainWindow", "Down"))
        self.label_nonvalue_rob_x.setText(_translate("MainWindow", "x:"))
        self.btn_xUp.setText(_translate("MainWindow", "Up"))
        self.label_nonvalue_robz.setText(_translate("MainWindow", "z:"))
        self.btn_zUp.setText(_translate("MainWindow", "Up"))
        self.label_nonvalue_roby.setText(_translate("MainWindow", "y:"))
        self.btn_yUp.setText(_translate("MainWindow", "Up"))
        self.label_nonvalue_LinearActuator_2.setText(_translate("MainWindow", "(+- 1 )"))
        self.twg_ManualController.setTabText(self.twg_ManualController.indexOf(self.tab_5), _translate("MainWindow", "Robotic Arm movement"))
        self.label_linear_pos.setText(_translate("MainWindow", "0"))
        self.label_nonvalue_position.setText(_translate("MainWindow", "position:"))
        self.label_nonvalue_LinearActuator.setText(_translate("MainWindow", "(mm)"))
        self.btn_linear_moveto.setText(_translate("MainWindow", "Move"))
        self.label_nonvalue_linear_updown.setText(_translate("MainWindow", "Move 1 mm:"))
        self.btn_linear_down.setText(_translate("MainWindow", "Down"))
        self.label_nonvalue_linear_moveto.setText(_translate("MainWindow", "Move to:"))
        self.btn_linear_up.setText(_translate("MainWindow", "Up"))
        self.btn_LinearCalibration.setText(_translate("MainWindow", "Calibration"))
        self.twg_ManualController.setTabText(self.twg_ManualController.indexOf(self.tab_6), _translate("MainWindow", "Linear actuator movement"))
        self.label_robotMove.setText(_translate("MainWindow", "Manual Controller:"))
        self.label_nonvalue_azimuthpoints.setText(_translate("MainWindow", "azimuthPoints:"))
        self.label_nonvalue_laser_angle.setText(_translate("MainWindow", "laser_angle:"))
        self.label_nonvalue_zstepsize.setText(_translate("MainWindow", "z_stepsize:"))
        self.twg_scanningMode.setTabText(self.twg_scanningMode.indexOf(self.tab_3), _translate("MainWindow", "Cylinder Scan"))
        self.label_elevationPoints.setText(_translate("MainWindow", "elevationPoints:"))
        self.twg_scanningMode.setTabText(self.twg_scanningMode.indexOf(self.tab_4), _translate("MainWindow", "Halve Sphere Scan"))
        self.label_nonvalue_offset.setText(_translate("MainWindow", "offset:"))
        self.label_nonvalue_circleradius.setText(_translate("MainWindow", "circle_radius:"))
        self.label_nonvalue_zMin.setText(_translate("MainWindow", "zMin:"))
        self.twg_scanSetting.setTabText(self.twg_scanSetting.indexOf(self.tab_7), _translate("MainWindow", "Laser measurement"))
        self.btn_clearTable.setText(_translate("MainWindow", "Clear all"))
        self.btn_input.setText(_translate("MainWindow", "Input"))
        self.label_nonvalue_x.setText(_translate("MainWindow", "x:"))
        self.label_nonvalue_y.setText(_translate("MainWindow", "y:"))
        self.label_nonvalue_z.setText(_translate("MainWindow", "z:"))
        self.twg_scanSetting.setTabText(self.twg_scanSetting.indexOf(self.tab_8), _translate("MainWindow", "Microwave Measurement"))
        self.label_ScanningSetting_2.setText(_translate("MainWindow", "Result:"))
        self.label_nonvalue_distance.setText(_translate("MainWindow", "distance:"))
        self.label_nonvalue_netwrok.setText(_translate("MainWindow", "Network:"))
        self.label_nonvalue_x_2.setText(_translate("MainWindow", "x:"))
        self.label_nonvalue_y_3.setText(_translate("MainWindow", "y: "))
        self.label_nonvalue_x_3.setText(_translate("MainWindow", "x:"))
        self.label_nonvalue_y_2.setText(_translate("MainWindow", "y: "))
        self.label_nonvalue_z_3.setText(_translate("MainWindow", "z:"))
        self.label_nonvalue_z_2.setText(_translate("MainWindow", "z:"))
        self.label_dist_laser.setText(_translate("MainWindow", "2"))
        self.cbx_S33.setText(_translate("MainWindow", "S33"))
        self.cbx_S32.setText(_translate("MainWindow", "S32"))
        self.cbx_S23.setText(_translate("MainWindow", "S23"))
        self.cbx_S22.setText(_translate("MainWindow", "S22"))
        self.btn_Plot.setText(_translate("MainWindow", "Plot"))
