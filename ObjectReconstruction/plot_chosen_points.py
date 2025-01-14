import numpy as np
import open3d as o3d
from mayavi import mlab
from scipy.spatial.transform import Rotation as R


def plot_choosen(
    closestPoints, closestNormals, choosenPoints, recon_mesh, distance_from_mesh
):
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
        closestPoints[:, 0] + distance_from_mesh * closestNormals[:, 0],
        closestPoints[:, 1] + distance_from_mesh * closestNormals[:, 1],
        closestPoints[:, 2] + distance_from_mesh * closestNormals[:, 2],
        s2,
        scale_factor=4.0,
        scale_mode="none",
        color=(0.1, 0.9, 0.1),
    )
    choosenPlot = mlab.points3d(
        choosenPoints[:, 0],
        choosenPoints[:, 1],
        choosenPoints[:, 2],
        s1,
        scale_factor=4.0,
        scale_mode="none",
        color=(0.9, 0.1, 0.1),
    )
    if len(closestPoints[:, 0]) < 2:
        ColorBar = np.full((2, 4), [255, 0, 0, 255])
        ColorSet = np.full((2, 4), [0, 255, 0, 255])
    elif len(closestPoints[:, 0]) >= 2:
        ColorBar = np.full((len(closestPoints[:, 0]), 4), [255, 0, 0, 255])
        ColorSet = np.full((len(choosenPoints[:, 0]), 4), [0, 255, 0, 255])

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

    choosenPlot.module_manager.scalar_lut_manager.lut.number_of_colors = 2
    setPoint.module_manager.scalar_lut_manager.lut.number_of_colors = 2

    choosenPlot.module_manager.scalar_lut_manager.lut.table = ColorBar
    setPoint.module_manager.scalar_lut_manager.lut.table = ColorSet
    # mlab.axes(xlabel="X", ylabel="Y")
    mlab.draw()
    mlab.show()


### Run the raycasting from a specific point, with the normal pointing towards the mesh, This will results in barycemtric coordinates,
### Which can then be converted to cartesian coordinates using formula found online
