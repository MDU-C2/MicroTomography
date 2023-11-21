## Author : Filip Lindhe

import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation as R
from pytransform3d.rotations import plot_basis, matrix_from_quaternion
import matplotlib.pyplot as plt

#### Function returns the closes point on the mesh to the choosen points cP


def ray_cast_points(recon_mesh, choosenPoints, distance_from_mesh):
    recon_vertices = np.asarray(recon_mesh.vertices)
    recon_triangles = np.asarray(recon_mesh.triangles)
    recon_vertices = o3d.core.Tensor(
        recon_vertices,
        dtype=o3d.core.Dtype.Float32,
    )

    recon_triangles = o3d.core.Tensor(
        recon_triangles,
        dtype=o3d.core.Dtype.UInt32,
    )

    scene = o3d.t.geometry.RaycastingScene()

    recond_id = scene.add_triangles(recon_vertices, recon_triangles)

    # normal = np.asarray([0, 0, 0]) - np.asarray(cP)
    closestPoints = []
    closestNormals = []
    # normalized_v = normal / np.sqrt(np.sum(normal**2))
    for points in choosenPoints:
        rays = o3d.core.Tensor(
            [
                [
                    points[0],
                    points[1],
                    points[2],
                ],
            ],
            dtype=o3d.core.Dtype.Float32,
        )
        ans = scene.compute_closest_points(rays)

        normal = ans["primitive_normals"].numpy() / np.linalg.norm(
            ans["primitive_normals"].numpy()
        )
        print(normal)
        print(np.linalg.norm(normal))
        closestNormals.append(-normal)
        closestPoints.append(ans["points"].numpy())

    closestPoints = np.vstack(closestPoints)
    closestNormals = np.vstack(closestNormals)

    quat = []

    vector = [0, 0, 1]
    temp = []
    quaternion = []

    for n in closestNormals:  ## -normal to get the correct direction
        theta = np.arccos(np.dot(vector, -n))
        b = np.cross(vector, -n)
        b_hat = b / np.linalg.norm(b)
        q = np.cos(theta / 2)

        q = np.append(q, np.sin(theta / 2) * b_hat[0])

        q = np.append(q, np.sin(theta / 2) * b_hat[1])

        q = np.append(q, np.sin(theta / 2) * b_hat[2])
        quat.append(q)
        plot_basis(R=matrix_from_quaternion(q))
        plt.show()

    return closestPoints, quat


### Run the raycasting from a specific point, with the normal pointing towards the mesh, This will results in barycemtric coordinates,
### Which can then be converted to cartesian coordinates using formula found online
