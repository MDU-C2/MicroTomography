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

from ChoosePoints import rayCastPoints as rcP


fileName = "Data\surfacePoint12061105_5.625deg_10stepWITHOUTNAN.mat"
f = sp.io.loadmat(fileName, squeeze_me=False)
data = np.array(f["surfacePoint"])  # Gets the surface points from the .mat file

mesh, points = lstl()

newData_X = data[:, 0, :]
newData_Y = data[:, 1, :]
newData_Z = data[:, 2, :]


# Reshapes the array into a points array
points_2 = reshapeArr.fixPoints(newData_X, newData_Y, newData_Z)


#################################################################################
print("Number of datapoint :", len(points))

save = False  # Save file? #Takes pretty long time to save .obj file, about 5-10 minutes
saveImage = False  # Save plot image?

t = time.time()
recon_mesh = surface_Reconstruction.poisson_surfRecon(points_2, save)
totalElapsed = time.time() - t
print("Time to complete reconstruction : ", totalElapsed)

t = time.time()
GT_mesh = surface_Reconstruction.poisson_surfRecon(points, save)
totalElapsed = time.time() - t
print("Time to complete reconstruction : ", totalElapsed)


# Error metric function.
TE.lineTrace(GT_mesh, recon_mesh)

# ChosenPoints Functions gets the closes
choosenPoints = np.array([[10, 40, -50], [10, 10, -10], [50, 50, -70]], np.int32)

newPoints = rcP(
    recon_mesh, choosenPoints
)  # Recon mesh is reconstructed mesh, cP is the chosen points where to put the antenna. # newPoints is the points on the mesh each correlating to their respective point in choosenPoints.
