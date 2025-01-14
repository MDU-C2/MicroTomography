## Author : Filip Lindhe


import numpy as np
from stl import mesh


def load_stl_file():
    your_mesh = mesh.Mesh.from_file(
        "stl_files/SimpleBreast_R62_centered_nonipple_surface_origin.STL"
    )

    points_x = your_mesh.x.flatten()
    points_y = your_mesh.y.flatten()
    points_z = your_mesh.z.flatten()
    points = np.empty([len(points_x), 3])
    points[:, 0] = points_x
    points[:, 1] = points_y
    points[:, 2] = points_z

    your_mesh.update_areas()
    your_mesh.update_max()
    your_mesh.update_min()
    your_mesh.update_normals()
    your_mesh.update_units()

    return your_mesh, points
