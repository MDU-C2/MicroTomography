import numpy as np
import open3d as o3d

### Set parameters to create a scanning pattern.
### Enter a point, choose closest point on mesh.


#### Function returns the closes point on the mesh to the choosen points cP
def ChoosePoints(recon_mesh, cP):
    points = []

    distance = []

    for vP in np.asarray(recon_mesh.vertices)[:, :]:
        distance.append(
            np.sqrt((cP[0] - vP[0]) ** 2 + (cP[1] - vP[1]) ** 2 + (cP[2] - vP[2]) ** 2)
        )

        points = np.asarray(recon_mesh.vertices)[np.argmin(distance), :]

    return points


def rayCastPoints(recon_mesh, cP):
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

    # normalized_v = normal / np.sqrt(np.sum(normal**2))
    rays = o3d.core.Tensor(
        [
            [
                cP[0],
                cP[1],
                cP[2],
            ],
        ],
        dtype=o3d.core.Dtype.Float32,
    )
    ans = scene.compute_closest_points(rays)

    print(ans)

    closestPoints = ans["points"].numpy()
    return closestPoints


### Run the raycasting from a specific point, with the normal pointing towards the mesh, This will results in barycemtric coordinates,
### Which can then be converted to cartesian coordinates using formula found online
