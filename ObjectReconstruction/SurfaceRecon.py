##
# Modules
##
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from mayavi import mlab
from statistics import mean
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

step_down = 0.001 #Step size for spline interpolation with x,y in Z direction. The smaller this value is, the more values will be added, duh. 

N = int(len(data_Z[:,0]) / 100 / step_down) #Number of steps

znew = np.linspace(data_Z[-1,0], data_Z[0,0] / 100, N) #Creates new Z array (Only used for getting the shapes of x and y arrays, need to be changed.)


newData_X = np.empty([znew.shape[0],data_X.shape[1]]) #Creates new Arrays for the data.
newData_Y = np.empty([znew.shape[0],data_Y.shape[1]])
newData_Z = np.empty([znew.shape[0],data_Z.shape[1]])

for i in range(data_X.shape[1]):
    newData_X[:,i],newData_Y[:,i],newData_Z[:,i] = spline.spline_xy(data_X[:,i],data_Y[:,i],data_Z[:,i],step_down) #Calls spline function


#####Plots the point cloud with the all new interpolated values EXCLUDING Z 
#fig = plt.figure() 
#ax = plt.axes(projection='3d')
#ax.scatter3D(newData_X, newData_Y, newData_Z,c=newData_Z,cmap = 'Greens')
#lt.show()
#####

data_X = newData_X
data_Y = newData_Y
data_Z = newData_Z


nPoints = 100 #n*nPoints = number of new points
n = newData_X.shape[1] #Number of points around the complete circle,
theta = 360/n #degrees between the points
thetaArray = np.linspace(0,360,n)
newTheta = 360/(n*nPoints)
newThetaArray = np.linspace(0,360,n*nPoints)

newData_X = np.empty([data_X.shape[0],n*nPoints]) #Creates new Arrays for the data.
newData_Y = np.empty([data_Y.shape[0],n*nPoints])
newData_Z = np.empty([data_Z.shape[0],n*nPoints])

for i in range(data_X.shape[0]):
    newData_X[i,:], newData_Y[i,:] = spline.spline_circle(data_X[i,:],data_Y[i,:],newThetaArray,thetaArray)
    newData_Z[i,:] = mean(data_Z[i,:])

points = reshapeArr.fixPoints(newData_X,newData_Y,newData_Z)

delaunay_tri = Delaunay(points); # Gets the Delaunay triangulation of the points 

#####Plots the point cloud with the all new interpolated values INCLUDING Z 
#fig = plt.figure() 
#ax = plt.axes(projection='3d')
#ax.scatter3D(newData_X, newData_Y, newData_Z,c=newData_Z,cmap = 'Greens')
#plt.show()
#####

h = sp.spatial.ConvexHull(points) #Gets convexhull object from Points

faces = h.simplices # Gets the faces of the Delaunay triangulation


Triangular = pv.PolyData(points,force_float=False) #Uses poly data ?

mesh = Triangular.delaunay_3d() # Creates mesh using delaunay 3d triangles

#Plot the mesh
plotter = pv.Plotter()
plotter.add_mesh(mesh, color='white')
plotter.show()