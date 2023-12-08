##
# Modules
##


import numpy as np
import scipy as sp
import pandas as pd

# from mayavi import mlab

import time
import sys
import os

##
# Class files
##

path = os.getcwd()

sys.path.append(path)
sys.path.append("~/Downloads/glfw-master")

from spline_data import spline
from reshape_list import fix_points
from surface_reconstruction import (
    poisson_surface_reconstruction,
    delaunay_original,
    alpha_shape,
    ball_pivoting,
)
from load_cad_file import load_stl_file

# from plot_chosen_points import plot_choosen

from trace_error import line_trace
from choose_points_microwave import ray_cast_points, get_points
from read_save_csv import save_csv
from interpolate_up import interpolate_up as int_up
from move_pointcloud import move_pointcloud
from plot_chosen_points import plot_choosen
from RobotArm.generate_scan_points import generate_scan_points_cylinder


filename = "scanned_data/2023-11-16-1329-filip.csv"
# f = sp.io.loadmat(fileName, squeeze_me=False)
data = pd.read_csv(filename)  # Gets the surface points from the .mat file
# data_2 = pd.read_csv(filename_2)
data = data.to_numpy()


# data = np.append(data, data_2.to_numpy(), axis=0)
mesh, points = load_stl_file()
# data[:, 2] = data[:, 2] + 15
# Reshapes the array into a points array
# points_2 = fix_points(data)

step_size = 2
data = int_up(data, step_size)
data = move_pointcloud(data)

### Plot pointcloud
"""mlab.figure()
s = np.arange(len(np.asarray(data)[:, 0]))
p3d = mlab.points3d(
    np.asarray(data)[:, 0],
    np.asarray(data)[:, 1],
    np.asarray(data)[:, 2],
    s,
    scale_factor=1,
    scale_mode="none",
)

mlab.draw()
mlab.show()"""
###

#################################################################################
# print("Number of datapoint :", len(points))

save = False  # Save file? # IMPORTANT! High amount of data increases the save time significantly

test = 1

if test == 1:
    t = time.time()
    re_resolution = 5
    save = False
    recon_mesh = poisson_surface_reconstruction(data, save, re_resolution)
    totalElapsed = time.time() - t
    print("Time to complete reconstruction : ", totalElapsed)

if test == 2:
    t = time.time()
    save = True
    recon_mesh = delaunay_original(data)
    totalElapsed = time.time() - t
    print("Time to complete reconstruction : ", totalElapsed)

gt_resolution = 5
t = time.time()
save = False
GT_mesh = poisson_surface_reconstruction(points, save, gt_resolution)

totalElapsed = time.time() - t
# print("Time to complete reconstruction : ", totalElapsed)

# Error metric function.

average_error_1 = line_trace(GT_mesh, recon_mesh, test, data)


# ChosenPoints Functions gets the closest points on the mesh
choosen_points = generate_scan_points_cylinder(60, 1, -100, 16, -100, 0)
choosen_points = [point[0] for point in choosen_points]
distance_from_mesh = 2  # in mm
# closestPoints, quats = ray_cast_points(recon_mesh, choosen_points, distance_from_mesh)
closestPoints, quats, closestNormals = get_points(
    recon_mesh, choosen_points, distance_from_mesh
)
# Recon mesh is reconstructed mesh, cP is the chosen points where to put the antenna. # closestPoints is the points on the mesh each correlating to their respective point in choosenPoints.
# closestNormals is the normals for each triangle which the points in closestPoints inhabit.
print(closestPoints)
print("Quaternions : ", quats)
plot_choosen(closestPoints, closestNormals, choosen_points, recon_mesh)
