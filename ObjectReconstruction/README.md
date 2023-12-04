
# [IMPORTANT] 
This guide will help the user run scripts related to object reconstruction.
The program requiers Open3d which is a python library for handling 3D data processing. 
Open3d in turn requires python 3.10- . To install open3d make sure python 3.10 is installed, then run "pip3.10 install open3d"
More information on Open3d can be found on the official website : http://www.open3d.org/

You can also run "pip3.10 install -r requirements.txt" to install all required packages for the micro Tomography project.

## [main.py]:
Open the file main.py

The fileName variable holds the path to the file where the data is located. 
Change this variable name to the correct file.

In the file load_cad_file.py enter the correct name of the choosen CAD File. 

the variable test changes which surface reconstruction to run, either Poisson or Delaunay.

re_resolution and gt_resolution indicates the Depth of the oc tree of the poisson surface reconstruction. Change this for different results.

Run the program.

## [surface_reconstuction.py]:

### [delaunay]:
This algorithm takes one input argument. 
Points, which is the desired point cloud. 
The program will return the delaunay triangulation mesh object.

### [alpha_shape]:

This algorithm takes two input arguments.
Points which is the desired point cloud and Save which is a bool where True indicates that the mesh should be saved. Or False which indicates that it should not be saved.

Inside the script there are four important variables which desicdes the results of the algorithm.

alpha : This changes the alpha parameter, which is important for the alpha_shape. Basically it's the radius of the sphere that "rolls" around each point.
norm_Radius : The radius of the circle which decides what points should be used to approximate the normal
norm_NN : how many points inside the circle with radius norm_Radius should be used to approximate the normal.
orient_Norm_Knn : Descides the direction of the mesh. Higher value the more normals are used to change all normals to the same direction.

The script returns a special open3D mesh obj.

### [ball_pivoting]:

This algorithm takes two input arguments.
Points which is the desired point cloud and Save which is a bool where True indicates that the mesh should be saved. Or False which indicates that it should not be saved.

There is one important variable inside this script. 

radii : This includes the list of radii which are used in the ball_pivoting algorithm. Basically it's the radii of the sphere's that rolls around each point.

The script returns a special open3D mesh obj.

### [poisson_surface_reconstruction]:

This algorithm takes three input arguments.
Points which is the desired point cloud and Save which is a bool where True indicates that the mesh should be saved. Or False which indicates that it should not be saved and re_resolution which decides the depth of the oc tree used in the poisson algorithm.


Inside the script there are five important variables which desicdes the results of the algorithm.

mask : removes all points in the point cloud above the mask value. It's only used if needed
norm_Radius : The radius of the circle which decides what points should be used to approximate the normal
norm_NN : how many points inside the circle with radius norm_Radius should be used to approximate the normal.
orient_Norm_Knn : Descides the direction of the mesh. Higher value the more normals are used to change all normals to the same direction.
bounding_additions : Adds the values (mm) to the bounding box to remove unwanted meshes outside of the point cloud. (This might be needed depending on what object is reconstructed. Poisson forces itself to create a watertight mesh, and if the point cloud is not meant to form a watertight mesh(i.e there are areas where alot of points are missing ) the mesh will look a bit weird. This will basically remove the weird part of the mesh.)

The script returns a special open3D mesh obj.

### [how to draw]:

uncomment the line : o3d.visualization.draw_geometries([pcd,mesh], mesh_show_back_face=True)
If there's no line like that, just add it. 
the pcd part draws the point cloud, the mesh part draws the mesh

This works for all except delaunay. If you need to print delaunay it's trivial using python libraries.

## [choosen_points_microwave.py]:

The script takes three arguments.

recon_mesh : The reconstructed mesh (i.e from scanned point cloud.).
choosenPoints : A list of arbitrary points (Where the you want the microwave antenna to be placed.).
distance_from_mesh : The distance in mm from the mesh where you want the antenna to be placed.


The script returns closestPoints, quaternion where : 
closestPoints : is a list of the points where the antenna should be placed. 
quaternion : a list of quaternions for the end effector. 

### [plot_chosen_points.py]

This script works the same as choosen_points_microwave.py but it is used to plot the points in 3D.
It takes the same input arguments.

## [trace_error.py]:

The script takes five arguments.

GT_mesh : The reconstructed ground truth mesh. (i.e CAD object mesh)
reconstruced_mesh : The reconstructed mesh. (from scanned point cloud)
test : indicates wether or not delaunay triangular mesh should be used(1 for poisson,ball_point or alpha_shape, 2 for delaunay)
points : point cloud
save : true of false

The script will raycast from each point in GT_mesh and compute the distance to the reconstructed_mesh.

The script will also plot a 3d point cloud with colours indicated based on the distances of each point in the GT_mesh. 
The point cloud shown will be the GT_mesh's point cloud and the colours indicate the distance to the reconstructed_mesh.

The script will return a the max distance. 






## [move_pointcloud.py]:

This script takes one input 

points : a point cloud (i.e scanned data)

Centers the pointcloud around [0,0,0]
returns the centered point cloud.


## [interpolate_up.py]: 

The script takes two input arguments. 

points : a point cloud (i.e scanned data)
step_size : a step size in mm

The script copies the top "row" of the scanned point cloud (In our case it's the top circle of the scanned data. I.e all aizumuth points in the with the highest Z value.) 15/stepsize times. 

(It's used to make the poisson surface reconstruction better, since poisson does not like that there are no scanned points on the top of the breast.)

## [Misc]:

There are some scripts that are not used in the final project. 
They include some spline scripts which can be used to interpolate the data to get a higher amount of data points.
It also includes some Reshape scripts which can be used to reshape the data (This was used in the beginning when we were using data from previous years project with a different data structure.)

read_save_csv.py is used to read or save csv files.

load_cad_file.py is used to load a cad file it's used in the main.py script and explained in that section of this readme.

