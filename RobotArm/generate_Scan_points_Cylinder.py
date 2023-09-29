import numpy as np

from pytransform3d.rotations import (
    matrix_from_axis_angle,
    quaternion_from_matrix,
)

def generate_scan_points_cylinder(diameter, zStepSize, zMax):
    R1 = matrix_from_axis_angle(np.array([0, 1, 0, np.pi / 2]))
    azimuth = (np.pi * np.linspace(0, 360, 20)) / 180
    points = []
    quaternions = []
    z = [h for h in reversed(range(zMax, 0+zStepSize, zStepSize))]

    for angle in azimuth:
        for h in z:
            x = diameter * np.cos(angle)
            y = diameter * np.sin(angle)
            R2 = matrix_from_axis_angle(np.array([1, 0, 0, np.pi - angle]))
            R = np.matmul(R1, R2)

            points.append([[x, y, h], quaternion_from_matrix(R)])

    
    return points
