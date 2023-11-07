## ## Author : Filip Lindhe

# Modules
##
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
#import pyvista as pv
import open3d as o3d
import time


class surface_reconstruction:
    def delaunay_original(points, save):
        t = time.time()
        ############ Works fine but it's not perfect. Requires very good data to provide good results.#############

        # delaunay_tri = Delaunay(points); # Gets the Delaunay triangulation of the points

        # h = sp.spatial.ConvexHull(points) #Gets convexhull object from Points

        # faces = h.simplices # Gets the faces of the Delaunay triangulation

        Triangular = pv.PolyData(points, force_float=False)  # Uses poly data ?

        mesh = Triangular.delaunay_3d()  # Creates mesh using delaunay 3d triangles

        points = mesh.GetPoints().GetData()
        triangles = mesh.cell_data_to_point_data()
        # mesh = delaunay_tri
        # Plot the mesh
        elapsed = time.time() - t
        print("Time to do surface reconstruction:", elapsed)
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, show_edges=False, color="white")
        plotter.add_points(mesh.points, color="red", point_size=10)
        plotter.show()
        if save == True:
            mesh.triangle_normals = o3d.utility.Vector3dVector([])
            o3d.io.write_triangle_mesh(
                "mesh.obj", mesh, print_progress=True
            )  # Writes the file without any warnings.
        return mesh

    def alpha_shape(points, save):
        t = time.time()
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.estimate_normals()
        alpha = 50
        # o3d.visualization.draw_geometries([pcd])
        # print(pcd)
        norm_Radius = 100
        norm_NN = 500

        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(norm_Radius, norm_NN)
        )
        """o3d.geometry.PointCloud.orient_normals_to_align_with_direction( 
            pcd, 
            orientation_reference=np.array([0., 0., 1.])
        )"""

        ##Orient normals to point "outward"

        orient_Norm_Knn = 10
        pcd.orient_normals_consistent_tangent_plane(
            orient_Norm_Knn
        )  ##Very expensive time and resource wise.
        tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)

        # print(np.asarray(tetra_mesh.vertices))
        mesh.compute_vertex_normals()
        elapsed = time.time() - t
        print("Time to do surface reconstruction:", elapsed)
        # o3d.visualization.draw_geometries([pcd,tetra_mesh], mesh_show_back_face=True)
        o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
        # o3d.visualization.draw_geometries([pcd], point_show_normal=True)

        if save == True:
            mesh.triangle_normals = o3d.utility.Vector3dVector([])
            o3d.io.write_triangle_mesh(
                "mesh.obj", mesh, print_progress=True
            )  # Writes the file without any warnings.

    def ball_pivoting(points, save):
        ############ Not very good for unstructured data. Need to find good radius of the balls, which is hard?. (Super slow cause looping radius)#############
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
            o3d.io.write_triangle_mesh(
                "mesh.obj", rec_mesh, print_progress=True
            )  # Writes the file without any warnings.

    def poisson_surface_reconstruction(points, save):
        t = time.time()
        ############ Works the best. Need to figure out how to mesh the top of the object where triangles are "too long".#############
        ############ Needs sufficient enough data ###############
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        norm_Radius = 100
        norm_NN = 500

        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(norm_Radius, norm_NN)
        )

        ##Orient normals to point "outward"

        orient_Norm_Knn = 10
        pcd.orient_normals_consistent_tangent_plane(
            orient_Norm_Knn
        )  ##Very expensive time and resource wise.

        with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug
        ) as cm:
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd, depth=5, linear_fit=True
            )  ## Depth increases the octree depth, basically giving more detail. Good data with many data points can have higher depth
            ## It gives a resolution of 2^depth
        print(mesh)
        # mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh).fill_holes().to_legacy() Can be used to fill large holes with a mesh. Not really usefull
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color(np.array([[0.5], [0.5], [0.5]]))
        o3d.visualization.draw_geometries([pcd, rec_mesh], mesh_show_back_face=True)
        elapsed = time.time() - t
        print("Time to do surface reconstruction:", elapsed)

        if save == True:
            mesh.triangle_normals = o3d.utility.Vector3dVector([])
            o3d.io.write_triangle_mesh(
                "meshNew.obj", mesh, print_progress=True
            )  # Writes the file without any warnings.
        return mesh
