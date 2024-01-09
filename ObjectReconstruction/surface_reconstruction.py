## ## Author : Filip Lindhe

# Modules
##
from scipy.spatial import Delaunay
import scipy as sp
import numpy as np


import open3d as o3d
import time
import copy


def delaunay_original(points, save):
    t = time.time()
    # Creates the delaunay triangulation mesh
    mesh = Delaunay(points)

    return mesh


def alpha_shape(points, save):
    t = time.time()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.estimate_normals()
    alpha = 50

    norm_Radius = 500
    norm_NN = 1000

    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(norm_Radius, norm_NN)
    )

    orient_Norm_Knn = 10
    pcd.orient_normals_consistent_tangent_plane(orient_Norm_Knn)
    tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)

    mesh.compute_vertex_normals()
    elapsed = time.time() - t
    # print("Time to do surface reconstruction:", elapsed)

    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

    if save == True:
        mesh.triangle_normals = o3d.utility.Vector3dVector([])
        o3d.io.write_triangle_mesh(
            "mesh.obj", mesh, print_progress=True
        )  # Writes the file without any warnings.


def ball_pivoting(points, save):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.estimate_normals()
    radii = np.linspace(0.0001, 20, num=200)
    rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii)
    )
    o3d.visualization.draw_geometries([pcd, rec_mesh], mesh_show_back_face=True)
    if save == True:
        rec_mesh.triangle_normals = o3d.utility.Vector3dVector([])
        o3d.io.write_triangle_mesh("mesh.obj", rec_mesh, print_progress=True)


def poisson_surface_reconstruction(points, save, re_resolution):
    t = time.time()

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    points = np.asarray(pcd.points)
    mask = points[:, 2] < -15
    pcd.points = o3d.utility.Vector3dVector(
        points[mask]
    )  # normals and colors are unchanged

    # alternative
    pcd = pcd.select_by_index(np.where(points[:, 2] < -15)[0])

    norm_Radius = 30
    norm_NN = 20

    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(norm_Radius, norm_NN)
    )

    ##Orient normals to point "outward"

    orient_Norm_Knn = 20
    pcd.orient_normals_consistent_tangent_plane(
        orient_Norm_Knn
    )  ##Very expensive time and resource wise.

    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=re_resolution, linear_fit=True
    )

    mesh = mesh.compute_vertex_normals()
    bounding_additions = [5, 5, 5]
    # Creates a bounding box around the point cloud and crops the mesh based on this bounding box
    bounding_box = pcd.get_axis_aligned_bounding_box()
    bounding_box.max_bound = bounding_box.max_bound + bounding_additions
    bounding_box.min_bound = bounding_box.min_bound - bounding_additions
    mesh = mesh.crop(bounding_box)

    mesh.paint_uniform_color(np.array([[0.5], [0.5], [0.5]]))

    #o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

    elapsed = time.time() - t
    # print("Time to do surface reconstruction:", elapsed)

    if save == True:
        mesh.triangle_normals = o3d.utility.Vector3dVector([])
        o3d.io.write_triangle_mesh(
            "meshNew.obj", mesh, print_progress=True
        )  # Writes the file without any warnings.
    return mesh
