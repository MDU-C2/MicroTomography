##
# Modules
##
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from mayavi import mlab
import pyvista as pv
##
# Class files
##
from Spline import spline
from reshapeArr import reshapeArr





fileName = "Data\surfacePoint12061105_5.625deg_10stepWITHOUTNAN.mat"
f = sp.io.loadmat(fileName,squeeze_me=False)
data = np.array(f["surfacePoint"]) # Gets the surface points from the .mat file 

data_X = data[:,0,:] #Reorganize the data into rows 
data_Y = data[:,1,:]
data_Z = data[:,2,:]

step_down = 0.01 #Step size for spline interpolation with x,y in Z direction. The smaller this value is, the more values will be added, duh. 


newData_X,newData_Y,newData_Z = spline.spline_xy(data_X,data_Y,data_Z,step_down) ##Runs the spline in z direction

#####Plots the point cloud with the all new interpolated values EXCLUDING Z 
#fig1 = plt.figure() 
#ax = plt.axes(projection='3d')
#ax.scatter3D(newData_X, newData_Y, newData_Z,c=newData_Z,cmap = 'Greens')
#plt.show()
#####


nPoints = 10 #n*nPoints = number of new points
newData_X,newData_Y,newData_Z = spline.spline_circle(newData_X,newData_Y,newData_Z,nPoints) #Runs the spline in aximuth direction

#####Plots the point cloud with the all new interpolated values INCLUDING Z 
#fig2 = plt.figure() 
#ax = plt.axes(projection='3d')
#ax.scatter3D(newData_X, newData_Y, newData_Z,c=newData_Z,cmap = 'Greens')
#plt.show()
#####


#################################################################################

points = reshapeArr.fixPoints(newData_X,newData_Y,newData_Z)

delaunay_tri = Delaunay(points); # Gets the Delaunay triangulation of the points 

h = sp.spatial.ConvexHull(points) #Gets convexhull object from Points

faces = h.simplices # Gets the faces of the Delaunay triangulation


Triangular = pv.PolyData(points,force_float=False) #Uses poly data ?

mesh = Triangular.delaunay_3d() # Creates mesh using delaunay 3d triangles
#mesh = delaunay_tri
#Plot the mesh
plotter = pv.Plotter()
plotter.add_mesh(mesh,show_edges=True, color='white')
plotter.add_points(mesh.points,color='red',point_size=2)
plotter.show()