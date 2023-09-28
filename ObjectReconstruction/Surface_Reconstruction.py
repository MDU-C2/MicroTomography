##
# Modules
##
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import scipy as sp
from mayavi import mlab
import numpy as np
import pyvista as pv
import open3d as o3d


class surface_Reconstruction():
    
    def delaunay_original(points):

        ############ Works fine but it's not perfect. Requires very good data to provide good results.#############

        delaunay_tri = Delaunay(points); # Gets the Delaunay triangulation of the points 

        h = sp.spatial.ConvexHull(points) #Gets convexhull object from Points

        faces = h.simplices # Gets the faces of the Delaunay triangulation


        Triangular = pv.PolyData(points,force_float=False) #Uses poly data ?

        mesh = Triangular.delaunay_3d() # Creates mesh using delaunay 3d triangles
        #mesh = delaunay_tri
        #Plot the mesh
        plotter = pv.Plotter()
        plotter.add_mesh(mesh,show_edges=False, color='white')
        plotter.add_points(mesh.points,color='red',point_size=5)
        plotter.show()
        

    def alpha_Shape(points):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.estimate_normals()
        alpha = 5
        o3d.visualization.draw_geometries([pcd])
        #print(pcd)
        tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd,alpha)
        #print(np.asarray(tetra_mesh.vertices))
        mesh.compute_vertex_normals()
        #o3d.visualization.draw_geometries([pcd,tetra_mesh], mesh_show_back_face=True)
        o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
        o3d.visualization.draw_geometries([pcd], point_show_normal=True)

    def ball_Pivoting(points):
        ############ Not very good for unstructured data. Need to find good radius of the balls, which is hard?.#############
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.estimate_normals()
        radii = [1,2,3,4,5,10]
        rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            pcd, o3d.utility.DoubleVector(radii))
        o3d.visualization.draw_geometries([pcd, rec_mesh])

    def poisson_surfRecon(points):

        ############ Works the best. Need to figure out how to mesh the top of the object where triangles are "too long".#############
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.estimate_normals()
        
       
        ##Orient normals to point "outward"
        o3d.geometry.PointCloud.orient_normals_to_align_with_direction( 
            pcd, 
            orientation_reference=np.array([0., 0., -1.])
        )
        o3d.visualization.draw_geometries([pcd], point_show_normal=True)

        with o3d.utility.VerbosityContextManager(
                o3d.utility.VerbosityLevel.Debug) as cm:
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd, depth=5)
        print(mesh)
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color(np.array([[0.5],[0.5],[0.5]]))
        o3d.visualization.draw_geometries([mesh],mesh_show_back_face=True)
        densities = np.asarray(densities)
        density_colors = plt.get_cmap('plasma')(
            (densities - densities.min()) / (densities.max() - densities.min()))
        density_colors = density_colors[:, :3]
        density_mesh = o3d.geometry.TriangleMesh()
        density_mesh.vertices = mesh.vertices
        density_mesh.triangles = mesh.triangles
        density_mesh.triangle_normals = mesh.triangle_normals
        density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
        o3d.visualization.draw_geometries([density_mesh])                                       
        vertices_to_remove = densities < np.quantile(densities, 0.1)
        mesh.remove_vertices_by_mask(vertices_to_remove)
        print(mesh)
        o3d.visualization.draw_geometries([mesh],mesh_show_back_face=True)