from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from mayavi import mlab
from statistics import mean

#X = Z, Y = (X or Y)

def spline_xy(data_x,data_y,data_z,step):
   
   
    N = int(len(data_z) / 100 / step)

    znew = np.linspace(data_z[-1], data_z[0] / 100, N)
    
     
    f_x = sp.interpolate.interp1d(data_z,data_x)
    f_y = sp.interpolate.interp1d(data_z,data_y)

    
    xnew = f_x(znew)
    ynew = f_y(znew)

    xnew = xnew[::-1]
    znew = znew[::-1]
    ynew = ynew[::-1]
    #plt.plot(znew,xnew)
    #plt.plot(data_x,data_z,'o')
    #plt.show()

    
    
    
    return xnew,ynew,znew
    
def spline_circle(data_x,data_y,newTheta,theta):
    
    cx = sp.interpolate.CubicSpline(theta,data_x)
    cy = sp.interpolate.CubicSpline(theta,data_y)

    return cx(newTheta),cy(newTheta)



f = sp.io.loadmat("Data\surfacePoint12061105_5.625deg_10stepWITHOUTNAN.mat",squeeze_me=False)
data = np.array(f["surfacePoint"]) # Gets the surface points from the .mat file 

data_X = data[:,0,:] #Reorganize the data into rows 
data_Y = data[:,1,:]
data_Z = data[:,2,:]

step_down = 0.001 #Step size for spline interpolation with x,y in Z direction

N = int(len(data_Z[:,0]) / 100 / step_down) #Number of steps

znew = np.linspace(data_Z[-1,0], data_Z[0,0] / 100, N) #Creates new Z array (Only used for getting the shapes of x and y arrays, need to be changed.)


newData_X = np.empty([znew.shape[0],data_X.shape[1]]) #Creates new Arrays for the data.
newData_Y = np.empty([znew.shape[0],data_Y.shape[1]])
newData_Z = np.empty([znew.shape[0],data_Z.shape[1]])

for i in range(data_X.shape[1]):
    newData_X[:,i],newData_Y[:,i],newData_Z[:,i] = spline_xy(data_X[:,i],data_Y[:,i],data_Z[:,i],step_down) #Calls spline function



fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(newData_X, newData_Y, newData_Z,c=newData_Z,cmap = 'Greens')
plt.show()

data_X = newData_X
data_Y = newData_Y
data_Z = newData_Z

#Next step is to interpolate the circles
# Might be able to use scipy.interpolate.cubic
# Have to i
nPoints = 10 #n*nPoints = number of new points
n = newData_X.shape[1] #Number of points around the complete circle,
theta = 360/n #degrees between the points
thetaArray = np.linspace(0,360,n)
newTheta = 360/(n*nPoints)
newThetaArray = np.linspace(0,360,n*nPoints)

newData_X = np.empty([data_X.shape[0],n*nPoints]) #Creates new Arrays for the data.
newData_Y = np.empty([data_Y.shape[0],n*nPoints])
newData_Z = np.empty([data_Z.shape[0],n*nPoints])

for i in range(data_X.shape[0]):
    newData_X[i,:], newData_Y[i,:] = spline_circle(data_X[i,:],data_Y[i,:],newThetaArray,thetaArray)
    newData_Z[i,:] = mean(data_Z[i,:])

#delaunay_tri = Delaunay(points); # Gets the Delaunay triangulation of the points 



fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(newData_X, newData_Y, newData_Z,c=newData_Z,cmap = 'Greens')
plt.show()

#h = scipy.spatial.ConvexHull(points)

#faces = h.simplices # Gets the faces of the Delaunay triangulation

#mlab.triangular_mesh(points[:,0], points[:,1], points[:,2], faces) #Creates mesh from the Delaunay triangulation
#mlab.show() #Shows the mesh









