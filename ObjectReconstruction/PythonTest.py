from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import scipy
from mayavi import mlab


def spline_xy(data_x, data_y):
    tck_X = np.full_like(data_X, 1)
    plt.plot(data_X[:, 1], data_Z[:, 1])
    plt.show()

    for i in range(data_X.shape[1]):  # Splines and resamples the data in x,z and y,z
        a = data_X[:, i]
        b = data_Z[:, i]
        new_order = np.lexsort([b, a])
        a = a[new_order]
        b = b[new_order]
        tck_X, myu = scipy.interpolate.splprep([b, a])
        xnew, znew = scipy.interpolate.splev(np.linspace(0, 1, 1000), tck_X)
        plt.plot(xnew, znew)
        plt.show()

    return xnew, znew


f = scipy.io.loadmat(
    "Data\surfacePoint12061105_5.625deg_10stepWITHOUTNAN.mat", squeeze_me=False
)
data = np.array(f["surfacePoint"])  # Gets the surface points from the .mat file

data_X = data[:, 0, :]  # Reorganize the data into rows
data_Y = data[:, 1, :]
data_Z = data[:, 2, :]


newData_X, newData_Y = spline_xy(data_X, data_Z)


data_X = data_X[~np.isnan(data_X)]  # Removes all nan values
data_Y = data_Y[~np.isnan(data_Y)]
data_Z = data_Z[~np.isnan(data_Z)]

length_Data = data_X.shape[0]  # Gets the length of the data (Number of data points)


points = np.empty(
    [resampled_X.shape[0], 3]
)  # Creates empty array to store the surface points to be used in the Delaunay function (Needs specific array format)
points[:, 0] = resampled_X  # Adds all points to the new array
points[:, 1] = resampled_Y
points[:, 2] = resampled_Z


delaunay_tri = Delaunay(points)
# Gets the Delaunay triangulation of the points

h = scipy.spatial.ConvexHull(points)

faces = h.simplices  # Gets the faces of the Delaunay triangulation

mlab.triangular_mesh(
    points[:, 0], points[:, 1], points[:, 2], faces
)  # Creates mesh from the Delaunay triangulation
mlab.show()  # Shows the mesh
