import numpy as np
import scipy as sp
from statistics import mean
from math import sqrt
import math


class spline:
    def cubic_spline(data_X, data_Y, data_Z, step_down):
        N = int(len(data_Z[:, 0]) / 100 / step_down)
        znew = np.linspace(data_Z[-1, :], data_Z[0, :] / 100, N)
        newData_X = np.empty(
            [znew.shape[0], data_X.shape[1]]
        )  # Creates new Arrays for the data.
        newData_Y = np.empty([znew.shape[0], data_Y.shape[1]])
        newData_Z = np.empty([znew.shape[0], data_Z.shape[1]])

        for i in range(data_X.shape[1]):
            test_z = data_Z[:, i]
            test_x = data_X[:, i]
            test_y = data_Y[:, i]

            tck_X = sp.interpolate.splrep(test_z[::-1], test_x[::-1], s=1)
            tck_Y = sp.interpolate.splrep(test_z[::-1], test_y[::-1], s=1)
            xnew = sp.interpolate.splev(znew[:, i], tck_X, der=0)
            ynew = sp.interpolate.splev(znew[:, i], tck_Y, der=0)

            newData_X[:, i] = xnew[::-1]
            newData_Y[:, i] = ynew[::-1]
            newData_Z[:, i] = znew[::-1, i]

        return newData_X, newData_Y, newData_Z

    def spline_xy(data_X, data_Y, data_Z, step_down):
        try:
            N = int(len(data_Z[:, 0]) / 100 / step_down)  # Number of steps
        except:
            print("no N")

        znew = np.linspace(
            data_Z[-1, :], data_Z[0, :] / 100, N
        )  # Creates new Z array (Only used for getting the shapes of x and y arrays, need to be changed.)§
        newData_X = np.empty(
            [znew.shape[0], data_X.shape[1]]
        )  # Creates new Arrays for the data.
        newData_Y = np.empty([znew.shape[0], data_Y.shape[1]])
        newData_Z = np.empty([znew.shape[0], data_Z.shape[1]])

        for i in range(data_X.shape[1]):
            f_x = sp.interpolate.interp1d(data_Z[:, i], data_X[:, i])
            f_y = sp.interpolate.interp1d(data_Z[:, i], data_Y[:, i])

            xnew = f_x(znew[:, i])
            ynew = f_y(znew[:, i])

            newData_X[:, i] = xnew[::-1]
            newData_Y[:, i] = ynew[::-1]
            newData_Z[:, i] = znew[::-1, i]

        return newData_X, newData_Y, newData_Z

    def spline_circle(data_x, data_y, data_z, nPoints):
        n = data_x.shape[1]  # Number of points around the complete circle,
        # theta = 36/n #degrees between the points
        thetaArray = np.linspace(0, 360, n)
        # newTheta = 360/(n*nPoints)
        newThetaArray = np.linspace(0, 360, n * nPoints)

        newData_X = np.empty(
            [data_x.shape[0], n * nPoints]
        )  # Creates new Arrays for the data.
        newData_Y = np.empty([data_y.shape[0], n * nPoints])
        newData_Z = np.empty([data_z.shape[0], n * nPoints])

        for i in range(data_x.shape[0]):
            cx = sp.interpolate.CubicSpline(thetaArray, data_x[i, :])
            cy = sp.interpolate.CubicSpline(thetaArray, data_y[i, :])
            newData_Y[i, :] = cy(newThetaArray)
            newData_X[i, :] = cx(newThetaArray)
            newData_Z[i, :] = mean(data_z[i, :])

        return newData_Y, newData_X, newData_Z

    def splinePerfectCircle(data_x, data_y, data_z, nPoints):
        ######## Splines the data by finding the average radius of each "circle". Might change the data too much? but it handles bad data pretty decently.
        n = data_x.shape[1]  # Number of points around the complete circle,
        # theta = 36/n #degrees between the points
        thetaArray = np.linspace(0, 360, n)
        # newTheta = 360/(n*nPoints)
        newThetaArray = np.linspace(0, 360, n * nPoints)
        r_1 = np.empty([data_x.shape[0], 1])
        r_2 = np.empty([data_x.shape[1], 1])
        for i in range(data_x.shape[0]):
            for j in range(data_x.shape[1]):
                r_2[j] = sqrt(data_x[i, j] ** 2 + data_y[i, j] ** 2)

            r_1[i] = np.mean(r_2)

        newData_X = np.empty(
            [data_x.shape[0], n * nPoints]
        )  # Creates new Arrays for the data.
        newData_Y = np.empty([data_y.shape[0], n * nPoints])
        newData_Z = np.empty([data_z.shape[0], n * nPoints])

        for j in range(data_x.shape[0]):
            for i in range(n * nPoints):
                newData_X[j, i] = r_1[j] * math.cos(newThetaArray[i])
                newData_Y[j, i] = r_1[j] * math.sin(newThetaArray[i])
            newData_Z[j, :] = mean(data_z[j, :])

        return newData_X, newData_Y, newData_Z
