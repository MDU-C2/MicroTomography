import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


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
        o3d.visualization.draw_geometries(
            [reconstructed_mesh], mesh_show_back_face=True
        )
        o3d.visualization.draw_geometries([GT_mesh], mesh_show_back_face=True)
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
            print(
                ans["t_hit"].numpy(),
                ans["geometry_ids"].numpy(),
                ans["primitive_uvs"].numpy(),
            )

            # print(rayTraceArray)

            """rays = o3d.core.Tensor(
                rayTraceArray,
                dtype=o3d.core.Dtype.Float32,
            )"""

        print(np.sum(errorDist) / len(errorDist))
