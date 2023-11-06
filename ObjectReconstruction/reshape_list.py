## Author : Filip Lindhe


import numpy as np


def fix_points(data):  # Fix points for delaunay triangle func
    data_x = data[:, 0, :]
    data_y = data[:, 1, :]
    data_z = data[:, 2, :]
    newData_X = data_x.reshape(
        (data_x.shape[0] * data_x.shape[1], 1)
    )  # Reshapes the arrays from (size,size) to (size*size,1)
    newData_Z = data_z.reshape((data_x.shape[0] * data_x.shape[1], 1))
    newData_Y = data_y.reshape((data_x.shape[0] * data_x.shape[1], 1))

    points = np.full(
        (newData_X.shape[0], 3), 0
    )  # Creates empty array with correct shape

    for i in range(newData_X.shape[0]):  # Puts the values into the new array
        points[i, 0] = newData_X[i]
        points[i, 1] = newData_Y[i]
        points[i, 2] = newData_Z[i]

    return points
