

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QVBoxLayout

from RobotArm.scan_breast_phantom import scan_points
from ObjectReconstruction.surface_reconstruction import poisson_surface_reconstruction

#function: save data in result table to csv
def save_model(table, log):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog

    data = readDataFromTable(table, log)

    try:
        file_path, _ = QFileDialog.getSaveFileName(None, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
    except:
        pass

    if file_path:
        with open(file_path + '.csv', "w", newline="") as csvfile:
            df = pd.DataFrame(data, columns=["X", "Y", "Z"])

            # Save the DataFrame to a CSV file
            df.to_csv(csvfile, index=False)  # Specify index=False to avoid writing row numbers as a column
            log.append(f"Model saved to: {file_path}")
    else:
        log.append("Saving cancel")


#function: read csv and add items to result table
def load_model(table, log):
    # Open a file dialog window for selecting a file
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog

    try:
        file_path, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
    except:
        pass

    # Check if a file was selected
    if file_path:
        data = pd.read_csv(file_path)
        log.append(f"Open model from: {file_path}")
        writeResultToTable(data, table)
    else:
        log.append("None file selected")

#function: read data from a table
def readDataFromTable(table, log):
    tableData = []
    
    # Extract data from the QTableWidget
    if table.rowCount() != 0:
        for row in range(table.rowCount()):
            row_data = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                try:
                    row_data.append(float(item.text()))
                except:
                    log.append(f"[{row}, {column}]is not a number. Please go and check it")

            tableData.append(row_data)
    else:
        log.append("No iteam in the table")

    return tableData

#function: write result to table
def writeResultToTable(data, table):

    # Remove all data in the result table before input new data
    table.setRowCount(0)
    
    df = pd.DataFrame(data, columns=["X", "Y", "Z"])

    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])

    # Populate the table with DataFrame data
    for i, row in df.iterrows():
        for j, value in enumerate(row):
            item = QTableWidgetItem(str(value))
            table.setItem(i, j, item)

#function: plot data by reading values from table
def plotData(table, figure, color, log):
    #Plot maunal positions
    
    tableData = readDataFromTable(table, log)

    data = pd.DataFrame(tableData, columns=["X", "Y", "Z"])

    data_X = data["X"]  # Reorganize the data into rows
    data_Y = data["Y"]
    data_Z = data["Z"]

    #Create a 3D scatter plot
    figure.scatter(data_X, data_Y, data_Z, c = color, marker="o")

#function: add item to table
def insertDataToTable(value_x, value_y, value_z, table, tab, log):
    # get number from text editor
    insert_x = value_x.value()
    insert_y = value_y.value()
    insert_z = value_z.value()

    # Get the current number of rows in the tableWidget
    current_row_count = table.rowCount()

    # Insert a new row at the end of the table
    table.insertRow(current_row_count)

    # Create items for each cell in the new row
    itemX = QTableWidgetItem(str(insert_x))
    itemY = QTableWidgetItem(str(insert_y))
    itemZ = QTableWidgetItem(str(insert_z))
    
    # Set the items for each cell in the new row
    table.setItem(current_row_count, 0, itemX)
    table.setItem(current_row_count, 1, itemY)
    table.setItem(current_row_count, 2, itemZ)

    # change tab in the tab table from default to my list
    tab.setCurrentIndex(1)

#function:connect matplotlib plot with scanning viewer
def add3DPlotInGUI(viewer):
    # Create a layout for the plot viwer
    layout = QVBoxLayout(viewer)
    figure = Figure()

    # Create a Matplotlib figure and add a 3D subplot for Scanning
    canvas = FigureCanvas(figure)
    layout.addWidget(canvas)
    ax = figure.add_subplot(111, projection="3d")

    # Set axis labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Create a Matplotlib toolbar
    toolbar = NavigationToolbar(canvas, viewer)
    layout.addWidget(toolbar)

    return ax, canvas

#function:connect matplotlib plot with network viewer
def add2DDiagramInGUI(viewer):
    # Create a layout for the plot viwer
    layoutNetwork = QVBoxLayout(viewer)
    figureNetwork = Figure()

    # Create a Matplotlib figure and add a 3D subplot for Scanning
    canvasNetwork = FigureCanvas(figureNetwork)
    layoutNetwork.addWidget(canvasNetwork)
    network_ax = figureNetwork.add_subplot(111)
    
    # Set axis labels
    network_ax.set_xlabel("Frequency")
    network_ax.set_ylabel("Abs Complex")

    return network_ax, canvasNetwork

#function: generate scanning points and peform scanning
def autoScan(currentIndex, quaternion, radius, z_stepsize, azimuth_points, z_offset, elevation_points, z_min, laser_angle, log):

    if not -90 < laser_angle < 90:
        log.append("Laser_angle must be -90 < laser_angle < 90")
        return None
    
    if currentIndex == 0:  # Cylinder
        log.append(f"Cylinder scan with quaternion: {quaternion}")
        result = scan_points(quaternion, radius, z_stepsize, z_min, azimuth_points, z_offset, laser_angle)
        return result
    elif currentIndex == 1:  # halve sphere
        log.append(f"Halve sphere scan with quaternion: {quaternion}")
        result = scan_points(quaternion, radius, azimuth_points, elevation_points, z_min, z_offset)
        return result
    
#functions: plot network analyser diagram
def plotNetworkAnalyserDiagram(network_ax, canvasNetwork, cbx_S33, cbx_S32, cbx_S23, cbx_S22, freq, data_33, data_32, data_23, data_22):   
    # Clean the axis
    network_ax.cla()

    # Set axis labels
    network_ax.set_xlabel("Frequency")
    network_ax.set_ylabel("Abs Complex")

    #X-value
    freq_simp = [x / 1000000 for x in freq]

    #y-values
    if cbx_S33.isChecked():
        complex_S33 = list(map(abs, data_33))
        network_ax.plot(freq_simp, complex_S33, label='S33')
        network_ax.legend()

    if cbx_S32.isChecked():
        complex_S32 = list(map(abs, data_32))
        network_ax.plot(freq_simp, complex_S32, label='S32')
        network_ax.legend()
    
    if cbx_S23.isChecked():
        complex_S23 = list(map(abs, data_23))
        network_ax.plot(freq_simp, complex_S23, label='S23')
        network_ax.legend()

    if cbx_S22.isChecked():
        complex_S22 = list(map(abs, data_22))
        network_ax.plot(freq_simp, complex_S22, label='S22')
        network_ax.legend()

    # Create a 3D scatter plot
    canvasNetwork.draw()

#function: load network analyser data from csv file 
def loadMWMeasurement():
    # Open a file dialog window for selecting a file
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog

    try:
        file_path, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
    except:
        pass

    data = pd.read_csv(file_path)

    #X-value
    frequency = np.complex_(data["Frequency"])
    freq = frequency.real

    #y-values
    string_S33 = data["S33"]
    data_33 = np.complex_(string_S33)

    string_S32 = data["S32"]
    data_32 = np.complex_(string_S32)

    string_S23 = data["S23"]
    data_23 = np.complex_(string_S23)

    string_S22 = data["S22"]
    data_22 = np.complex_(string_S22)

    return freq, data_33, data_32, data_23, data_22

# function: change value in label antenn position and surface postion
def changeLabels(robpos, surfacepos, spb_laser_distance, label_x_RobPos, label_y_RobPos,label_z_RobPos, label_dist_laser, label_x_Surface, label_y_Surface, label_z_Surface):
    #display antenn and laser distance
    label_x_RobPos.setText(str(robpos[0][0]))
    label_y_RobPos.setText(str(robpos[0][1]))
    label_z_RobPos.setText(str(robpos[0][2]))
    label_dist_laser.setText(str(spb_laser_distance))

    #display surface point
    label_x_Surface.setText(str(surfacepos[0][0]))
    label_y_Surface.setText(str(surfacepos[0][1]))
    label_z_Surface.setText(str(surfacepos[0][2]))

#function: change value label and spinbox 
def changeLinearActuatorSteps(stepValueNow, label_PosNow, spb_PosGoal):
    label_PosNow.setText(str(stepValueNow))
    spb_PosGoal.setValue(stepValueNow)

def recon3D(result):
    mesh = poisson_surface_reconstruction(result, save=False)
    return mesh