## Author : Filip Lindhe

import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation as R
from pytransform3d.rotations import plot_basis, matrix_from_quaternion
import matplotlib.pyplot as plt
from mathutils import Matrix, Vector


#### Function returns the closes point on the mesh to the choosen points cP
def get_quaternions(closestNormals):
    quat = []

    vector = [0, 0, 1]
    temp = []
    quaternion = []
    quaternions_test = []

    for n in closestNormals:  ##
        theta = np.arccos(np.dot(vector, n))
        b = np.cross(vector, n)
        b_hat = b / np.linalg.norm(b)
        q = np.cos(theta / 2)

        q = np.append(q, np.sin(theta / 2) * b_hat[0])

        q = np.append(q, np.sin(theta / 2) * b_hat[1])

        q = np.append(q, np.sin(theta / 2) * b_hat[2])
        quat.append(q)
        vector = [0, 0, -1]
        y_vector = np.cross(n, vector)
        x_vector = np.cross(y_vector, n)

        # Initialise matrix
        mat = Matrix.Identity(3)

        # Set matrix values
        mat.col[0] = x_vector
        mat.col[1] = y_vector
        mat.col[2] = n

        # Make the quaternion from the matrix
        quaternions_test = mat.to_quaternion()
        quaternion.append(quaternions_test)
        #plot_basis(R=matrix_from_quaternion(q))
        #plot_basis(R=matrix_from_quaternion(quaternions_test))
        #plt.show()

    return quaternion


def get_points(recon_mesh, choosenPoints, distance_from_mesh):
    recon_vertices = np.asarray(recon_mesh.vertices)
    recon_triangles = np.asarray(recon_mesh.triangles)

    recon_vertices_o3d = o3d.core.Tensor(
        recon_vertices,
        dtype=o3d.core.Dtype.Float32,
    )

    recon_triangles_o3d = o3d.core.Tensor(
        recon_triangles,
        dtype=o3d.core.Dtype.UInt32,
    )
    scene = o3d.t.geometry.RaycastingScene()

    recond_id = scene.add_triangles(recon_vertices_o3d, recon_triangles_o3d)

    closestPoints = []
    closestNormals = []
    # normalized_v = normal / np.sqrt(np.sum(normal**2))
    for points in choosenPoints:
        normal = [0, 0, points[2]] - points
        normal = normal / np.linalg.norm(normal)
        rays = o3d.core.Tensor(
            [
                [
                    points[0],
                    points[1],
                    points[2],
                    normal[0],
                    normal[1],
                    normal[2],
                ],
                [
                    points[0],
                    points[1],
                    points[2],
                    -normal[0],
                    -normal[1],
                    -normal[2],
                ],
            ],
            dtype=o3d.core.Dtype.Float32,
        )

        ans = scene.cast_rays(rays)
        distance = ans["t_hit"].numpy()
        idx = np.argmin(distance)
        triangle_id = ans["primitive_ids"].numpy()[idx]
        barycentric_coords = ans["primitive_uvs"].numpy()[idx]
        normal = ans["primitive_normals"].numpy()[idx]
        barycentric_coords = np.append(
            barycentric_coords, 1 - barycentric_coords[0] - barycentric_coords[1]
        )

        triangle_vert = recon_triangles[triangle_id]
        p_one = recon_vertices[triangle_vert[0]]
        p_two = recon_vertices[triangle_vert[1]]
        p_three = recon_vertices[triangle_vert[2]]

        b = np.array(barycentric_coords)  # Barycentric coordinates
        t = np.transpose([p_one, p_two, p_three])  # Triangle
        c = np.dot(t, b)

        c = c - distance_from_mesh * normal
        closestPoints.append(c)
        closestNormals.append(normal)
        print(ans)
        print(c)

    closestPoints = np.vstack(closestPoints)
    closestNormals = np.vstack(closestNormals)

    quaternion = get_quaternions(closestNormals)

    return closestPoints, quaternion, closestNormals


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
        closestNormals.append(normal)
        closestPoints.append(ans["points"].numpy())

    closestPoints = np.vstack(closestPoints)
    closestNormals = np.vstack(closestNormals)

    quaternion = get_quaternions(closestNormals)

    # plt.show()"""
    closestPoints[:, 0] = (
        closestPoints[:, 0] - distance_from_mesh * closestNormals[:, 0]
    )
    closestPoints[:, 1] = (
        closestPoints[:, 1] - distance_from_mesh * closestNormals[:, 1]
    )
    closestPoints[:, 2] = (
        closestPoints[:, 2] - distance_from_mesh * closestNormals[:, 2]
    )

    return closestPoints, quaternion


### Run the raycasting from a specific point, with the normal pointing towards the mesh, This will results in barycemtric coordinates,
### Which can then be converted to cartesian coordinates using formula found online
