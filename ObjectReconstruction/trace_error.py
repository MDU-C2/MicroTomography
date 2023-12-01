## ## Author : Filip Lindhe


import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import math

from mayavi import mlab


def line_trace(GT_mesh, reconstructed_mesh, test, points):
    if test == 1:
        GT_vertices = np.asarray(GT_mesh.vertices)
        GT_triangles = np.asarray(GT_mesh.triangles)
        recon_vertices = np.asarray(reconstructed_mesh.vertices)
        recon_triangles = np.asarray(reconstructed_mesh.triangles)
    if test == 2:
        GT_vertices = np.asarray(GT_mesh.vertices)
        GT_triangles = np.asarray(GT_mesh.triangles)
        recon_vertices = np.asarray(points[reconstructed_mesh.simplices])
        recon_vertices = recon_vertices.reshape(-1, recon_vertices.shape[-1])
        recon_vert_plot = recon_vertices.reshape(-1, recon_vertices.shape[-1])
        recon_triangles = np.asarray(reconstructed_mesh.simplices)[:, 0:3]

    GT_vertices = o3d.core.Tensor(
        GT_vertices,
        dtype=o3d.core.Dtype.Float32,
    )

    GT_triangles = o3d.core.Tensor(
        GT_triangles,
        dtype=o3d.core.Dtype.UInt32,
    )
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

    errorDist = []

    errorList = []

    for i in range(np.asarray(GT_mesh.vertices).shape[0]):
        vertex_points = np.asarray(GT_mesh.vertices)[i, :]
        normal = np.asarray(GT_mesh.vertex_normals)[i, :]

        rays = o3d.core.Tensor(
            [
                [
                    vertex_points[0].item(),
                    vertex_points[1].item(),
                    vertex_points[2].item(),
                    normal[0].item(),
                    normal[1].item(),
                    normal[2].item(),
                ],
                [
                    vertex_points[0].item(),
                    vertex_points[1].item(),
                    vertex_points[2].item(),
                    -normal[0].item(),
                    -normal[1].item(),
                    -normal[2].item(),
                ],
            ],
            dtype=o3d.core.Dtype.Float32,
        )

        ans = scene.cast_rays(rays)

        query_point = o3d.core.Tensor(
            [
                [
                    vertex_points[0].item(),
                    vertex_points[1].item(),
                    vertex_points[2].item(),
                ]
            ],
            dtype=o3d.core.Dtype.Float32,
        )

        unsigned_distance = scene.compute_distance(query_point)
        errorDist.append(unsigned_distance.numpy())
        occupancy = scene.compute_occupancy(query_point)

    print("Distance average error (mm): ", np.sum(errorDist) / len(errorDist))

    newList = []
    # print(len(np.asarray(GT_mesh.vertices)[:, 0]))
    """if test == 1:
        print(len(np.asarray(reconstructed_mesh.vertices)[:, 0]))
    if test == 2:
        print(len(recon_vertices[:, 0]))"""

    Color = np.full((len(np.asarray(GT_mesh.vertices)[:, 0]), 4), [255, 0, 0, 255])
    newList = np.interp(errorDist, (np.min(errorDist), np.max(errorDist)), (1, 255))
    x_new = 255 / len(newList)

    sort_index = np.argsort(newList, axis=0)
    test_list = newList.copy()

    for i in range(len(test_list)):
        test_list[sort_index[i]] = x_new * i

    for i in range(len(test_list)):
        Color[i, 0] = test_list[i]
        Color[i, 1] = 255 - test_list[i]
        Color[i, 2] = 0

    s = np.arange(len(np.asarray(GT_mesh.vertices)[:, 0]))
    mlab.figure()
    p3d = mlab.points3d(
        np.asarray(GT_mesh.vertices)[:, 0],
        np.asarray(GT_mesh.vertices)[:, 1],
        np.asarray(GT_mesh.vertices)[:, 2],
        s,
        scale_factor=3.0,
        scale_mode="none",
    )

    if test == 1:
        mlab.points3d(
            np.asarray(reconstructed_mesh.vertices)[:, 0],
            np.asarray(reconstructed_mesh.vertices)[:, 1],
            np.asarray(reconstructed_mesh.vertices)[:, 2],
            scale_factor=0,
            scale_mode="none",
        )

    if test == 2:
        mlab.points3d(
            recon_vert_plot[:, 0],
            recon_vert_plot[:, 1],
            recon_vert_plot[:, 2],
            scale_factor=2.0,
            scale_mode="none",
        )
    p3d.module_manager.scalar_lut_manager.lut.number_of_colors = len(s)
    p3d.module_manager.scalar_lut_manager.lut.table = Color  # / 255 Color

    ##############################Create colorbar
    errorDistSorted = []
    ColorBar = np.full((len(np.asarray(GT_mesh.vertices)[:, 0]), 4), [255, 0, 0, 1])
    errorDistSorted = np.sort(errorDist, axis=None)

    listColorBar = np.interp(
        errorDistSorted,
        (np.min(errorDistSorted), np.max(errorDistSorted)),
        (1, len(errorDistSorted)),
    )

    x_new = 255 / len(errorDistSorted)
    x = x_new
    for i in range(len(listColorBar)):
        ColorBar[i, 0] = x
        ColorBar[i, 1] = 255 - x
        ColorBar[i, 2] = 0
        x = x + x_new

    p3d2 = mlab.points3d(
        np.asarray(GT_mesh.vertices)[:, 0],
        np.asarray(GT_mesh.vertices)[:, 1],
        np.asarray(GT_mesh.vertices)[:, 2],
        errorDistSorted,
        scale_factor=0,
        scale_mode="none",
    )
    p3d2.module_manager.scalar_lut_manager.lut.number_of_colors = len(errorDistSorted)
    p3d2.module_manager.scalar_lut_manager.lut.table = ColorBar

    ########################Show mlab plot

    mlab.colorbar(object=p3d2, title="Error(mm)", orientation="vertical")
    # mlab.axes(xlabel="X", ylabel="Y")
    # mlab.savefig("test.png", size=[2000, 2000], magnification=10)
    mlab.draw()
    mlab.show()
    print("test")
    print("MAX : ", np.max(errorDist))
    return np.max(errorDist)
