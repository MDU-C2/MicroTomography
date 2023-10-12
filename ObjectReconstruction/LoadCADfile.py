import numpy as np
from stl import mesh


def loadSTLFile():
    your_mesh = mesh.Mesh.from_file("Data\Symmetric-test.STL")

    your_mesh.rotate(np.array([1, 0, 0]), -np.pi / 2)
    your_mesh.translate(
        np.array(
            [
                -your_mesh.max_[0] / 2,
                -your_mesh.min_[1] / 2,
                -your_mesh.max_[2] + 13.922,
            ]
        )
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
