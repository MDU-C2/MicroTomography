import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import math


class TraceError:
    def lineTrace(GT_mesh, reconstructed_mesh):
        GT_vertices = np.asarray(GT_mesh.vertices)
        GT_triangles = np.asarray(GT_mesh.triangles)
        recon_vertices = np.asarray(reconstructed_mesh.vertices)
        recon_triangles = np.asarray(reconstructed_mesh.triangles)

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
        # GT_id = scene.add_triangles(GT_vertices, GT_triangles)
        recond_id = scene.add_triangles(recon_vertices, recon_triangles)
        # test = o3d.visualization.Visualizer()
        """test.create_window(
            window_name="Open3D",
            width=1920,
            height=1080,
            left=50,
            top=50,
            visible=True,
        )"""

        errorDist = []
        """o3d.visualization.draw_geometries(
            [reconstructed_mesh], mesh_show_back_face=True
        )"""
        errorList = []
        # o3d.visualization.draw_geometries([GT_mesh], mesh_show_back_face=True)
        for i in range(np.asarray(GT_mesh.vertices).shape[0]):
            vertex_points = np.asarray(GT_mesh.vertices)[i, :]
            normal = np.asarray(GT_mesh.vertex_normals)[i, :]

            # VP = VP.item[0]
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
            # print("unsigned distance", unsigned_distance.numpy())
            # print("occupancy", occupancy.numpy())
            """print(
                ans["t_hit"].numpy(),
                ans["primitive_uvs"].numpy(),
            )"""  # ans["geometry_ids"].numpy(),
            if math.isinf(ans["t_hit"].numpy()[0]) == 0:
                errorList.append(ans["t_hit"].numpy()[0])
            # print(rayTraceArray)

            """rays = o3d.core.Tensor(
                rayTraceArray,
                dtype=o3d.core.Dtype.Float32,
            )"""
        print("Raycast : ", np.sum(errorList) / len(errorList))
        print("Distance : ", np.sum(errorDist) / len(errorDist))

        # Plot each point in GT.Vertices with different colour based on the error.
        # Error : errorDist, : smallest GREEN , Highest RED
        # ax.scatter(X[i], Y[i], Z[i], color=colors[i])
        # Colors = np.array([255,255,255],[255,255,255] etc...)
        # Need to convert distance to color. Highest = [255,0,0] , Lowest = [0,255,0]

        newList = []
        print(len(np.asarray(GT_mesh.vertices)[:, 0]))
        print(len(np.asarray(reconstructed_mesh.vertices)[:, 0]))

        Color = np.full((len(np.asarray(GT_mesh.vertices)[:, 0]), 3), [255, 0, 0])
        newList = np.interp(errorDist, (np.min(errorDist), np.max(errorDist)), (1, 255))

        for i in range(len(newList)):
            if newList[i] < 50:
                Color[i, :] = [0, 255, 0]
            if newList[i] >= 50 and newList[i] < 100:
                Color[i, :] = [50, 200, 0]
            if newList[i] >= 100 and newList[i] < 150:
                Color[i, :] = [100, 150, 0]
            if newList[i] >= 150 and newList[i] < 200:
                Color[i, :] = [150, 100, 0]
            if newList[i] >= 200:
                Color[i, :] = [255, 0, 0]

        # Color2 = Color / newList
        # Color2 = Color / np.max(Color)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter3D(
            np.asarray(GT_mesh.vertices)[:, 0],
            np.asarray(GT_mesh.vertices)[:, 1],
            np.asarray(GT_mesh.vertices)[:, 2],
            c=Color / 255,
            alpha=1,
        )
        ax.scatter3D(
            np.asarray(reconstructed_mesh.vertices)[:, 0],
            np.asarray(reconstructed_mesh.vertices)[:, 1],
            np.asarray(reconstructed_mesh.vertices)[:, 2],
            c="white",
            alpha=1,
        )
        plt.show()
