## Author : Filip Lindhe

import numpy as np
import open3d as o3d
from mayavi import mlab

#### Function returns the closes point on the mesh to the choosen points cP


def ray_cast_points(recon_mesh, choosenPoints):
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

        print(ans)
        closestNormals.append(ans["primitive_normals"].numpy())
        closestPoints.append(ans["points"].numpy())

    closestPoints = np.vstack(closestPoints)
    closestNormals = np.vstack(closestNormals)

    s1 = np.arange(len(choosenPoints))
    s2 = np.arange(len(closestPoints))
    mlab.figure()
    mlab.points3d(
        np.asarray(recon_mesh.vertices)[:, 0],
        np.asarray(recon_mesh.vertices)[:, 1],
        np.asarray(recon_mesh.vertices)[:, 2],
        scale_factor=2.0,
        scale_mode="none",
    )
    setPoint = mlab.points3d(
        closestPoints[:, 0],
        closestPoints[:, 1],
        closestPoints[:, 2],
        s2,
        scale_factor=4.0,
        scale_mode="none",
    )
    choosenPlot = mlab.points3d(
        choosenPoints[:, 0],
        choosenPoints[:, 1],
        choosenPoints[:, 2],
        s1,
        scale_factor=4.0,
        scale_mode="none",
    )
    ColorBar = np.full((len(closestPoints[:, 0]), 4), [255, 0, 0, 255])
    ColorSet = np.full((len(choosenPoints[:, 0]), 4), [0, 255, 0, 255])
    choosenPlot.module_manager.scalar_lut_manager.lut.number_of_colors = 2
    src = mlab.quiver3d(
        closestPoints[:, 0],
        closestPoints[:, 1],
        closestPoints[:, 2],
        closestNormals[:, 0],
        closestNormals[:, 1],
        closestNormals[:, 2],
        scale_factor=20,
    )
    # mlab.pipeline.vectors(src, mask_points=20, scale_factor=10.0)
    setPoint.module_manager.scalar_lut_manager.lut.number_of_colors = 2

    choosenPlot.module_manager.scalar_lut_manager.lut.table = ColorBar
    setPoint.module_manager.scalar_lut_manager.lut.table = ColorSet
    mlab.draw()
    mlab.show()
    return closestPoints, closestNormals


### Run the raycasting from a specific point, with the normal pointing towards the mesh, This will results in barycemtric coordinates,
### Which can then be converted to cartesian coordinates using formula found online
