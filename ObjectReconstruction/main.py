##
# Modules
##
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import matplotlib as mpl
import time
import open3d as o3d

##
# Class files
##
from Spline import spline
from reshapeArr import reshapeArr
from Surface_Reconstruction import surface_Reconstruction
from LoadCADfile import loadSTLFile as lstl
from TraceError import TraceError as TE


fileName = "Data\surfacePoint12061105_5.625deg_10stepWITHOUTNAN.mat"
f = sp.io.loadmat(fileName, squeeze_me=False)
data = np.array(f["surfacePoint"])  # Gets the surface points from the .mat file

mesh, points = lstl()

newData_X = data[:, 0, :]
newData_Y = data[:, 1, :]
newData_Z = data[:, 2, :]
#
print(np.max(newData_Z))
# Stepdown : 0.0005
# nPoints : 50
# Gives 704000

"""fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter(points[:, 0], points[:, 1], points[:, 2])


ax.scatter(newData_X, newData_Y, newData_Z)
plt.show()"""

step_down = 0.005  # Step size for spline interpolation with x,y in Z direction. The smaller this value is, the more values will be added, duh.
totalTime = time.time()
t = time.time()

##Runs the spline in z direction
# newData_X, newData_Y, newData_Z = spline.spline_xy(data_X, data_Y, data_Z, step_down)


# newData_X,newData_Y,newData_Z = spline.cubic_spline(data_X,data_Y,data_Z,step_down) #Different spline

elapsed = time.time() - t
print("Time to do spline:", elapsed)


nPoints = 10  # n*nPoints = number of new points

# n = data_X.shape[1]

t = time.time()


# Runs the spline in aximuth direction creates perfect circle slices
"""newData_X, newData_Y, newData_Z = spline.splinePerfectCircle(
    newData_X, newData_Y, newData_Z, nPoints
)"""


# Runs the spline in aximuth direction Change the data less
"""newData_X, newData_Y, newData_Z = spline.spline_circle(
    newData_X, newData_Y, newData_Z, nPoints
)"""
elapsed = time.time() - t
print("Time to do horizontal spline:", elapsed)

# Reshapes the array into a points array
points_2 = reshapeArr.fixPoints(newData_X, newData_Y, newData_Z)


#################################################################################
print("Number of datapoint :", len(points))

save = False  # Save file? #Takes pretty long time to save .obj file, about 5-10 minutes
saveImage = False  # Save plot image?

"""recon_mesh = surface_Reconstruction.delaunay_original(
    points, save
)"""  ##tight cocone variant
#
# surface_Reconstruction.alpha_Shape(points, save)
# surface_Reconstruction.ball_Pivoting(points,save)
recon_mesh = surface_Reconstruction.poisson_surfRecon(points_2, save)

totalElapsed = time.time() - totalTime
print("Time to complete Sample + reconstruction : ", totalElapsed)

GT_mesh = surface_Reconstruction.poisson_surfRecon(points, save)
TE.lineTrace(GT_mesh, recon_mesh)

if saveImage:
    fig2 = plt.figure(dpi=400)
    ax = plt.axes(projection="3d")
    ax.scatter3D(data_X, data_Y, data_Z, c=data_Z, cmap="Blues")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig("H:\MicroTomography\Images\plot.png", dpi=2000)
