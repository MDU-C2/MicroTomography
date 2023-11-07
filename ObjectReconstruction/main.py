##
# Modules
##


import numpy as np
import scipy as sp

import time
import sys
import os

##
# Class files
##

path = os.getcwd()

sys.path.append(path)

from spline_data import spline
from reshape_list import fix_points
from surface_reconstruction import surface_reconstruction
from load_cad_file import load_stl_file

# from trace_error import line_trace
# from choose_points_microwave import ray_cast_points
from read_save_csv import save_csv


fileName = "Data\surfacePoint12061105_5.625deg_10stepWITHOUTNAN.mat"
f = sp.io.loadmat(fileName, squeeze_me=False)
data = np.array(f["surfacePoint"])  # Gets the surface points from the .mat file

mesh, points = load_stl_file()

# Reshapes the array into a points array
points_2 = fix_points(data)


#################################################################################
print("Number of datapoint :", len(points))

save = False  # Save file? #Takes pretty long time to save .obj file, about 5-10 minutes
saveImage = False  # Save plot image?

t = time.time()
recon_mesh = surface_reconstruction.poisson_surface_reconstruction(points_2, save)
totalElapsed = time.time() - t
print("Time to complete reconstruction : ", totalElapsed)

t = time.time()
GT_mesh = surface_reconstruction.poisson_surface_reconstruction(points, save)
totalElapsed = time.time() - t
print("Time to complete reconstruction : ", totalElapsed)


# Error metric function.
# line_trace(GT_mesh, recon_mesh)

# ChosenPoints Functions gets the closes
# choosen_points = np.array([[10, 40, -50], [10, 10, -10], [50, 50, -70]], np.int32)

"""closestPoints, closestNormals = ray_cast_points(
    recon_mesh, choosen_points
)  # Recon mesh is reconstructed mesh, cP is the chosen points where to put the antenna. # closestPoints is the points on the mesh each correlating to their respective point in choosenPoints.
# closestNormals is the normals for each triangle which the points in closestPoints inhabit.
print(closestPoints)
print(closestNormals)"""
