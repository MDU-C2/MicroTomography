##
# Modules
##
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
##
# Class files
##
from Spline import spline
from reshapeArr import reshapeArr
from Surface_Reconstruction import surface_Reconstruction





fileName = "Data\surfacePoint12061105_5.625deg_10stepWITHOUTNAN.mat"
f = sp.io.loadmat(fileName,squeeze_me=False)
data = np.array(f["surfacePoint"]) # Gets the surface points from the .mat file 

data_X = data[:,0,:] #Reorganize the data into rows 
data_Y = data[:,1,:]
data_Z = data[:,2,:]

step_down = 0.0001 #Step size for spline interpolation with x,y in Z direction. The smaller this value is, the more values will be added, duh. 

newData_X,newData_Y,newData_Z = spline.spline_xy(data_X,data_Y,data_Z,step_down) ##Runs the spline in z direction

#####Plots the point cloud with the all new interpolated values EXCLUDING Z 
#fig1 = plt.figure() 
#ax = plt.axes(projection='3d')
#ax.scatter3D(newData_X, newData_Y, newData_Z,c=newData_Z,cmap = 'Greens')
#plt.show()
#####

nPoints = 100 #n*nPoints = number of new points

newData_X,newData_Y,newData_Z = spline.spline_circle(newData_X,newData_Y,newData_Z,nPoints) #Runs the spline in aximuth direction

#####Plots the point cloud with the all new interpolated values INCLUDING Z 
#fig2 = plt.figure() 
#ax = plt.axes(projection='3d')
#ax.scatter3D(newData_X, newData_Y, newData_Z,c=newData_Z,cmap = 'Greens')
#plt.show()
#####


#newData_X,newData_Y,newData_Z = data_X,data_Y,data_Z ##Comment Line  29 and 40 and uncomment this to run the original data without sampling.


points = reshapeArr.fixPoints(newData_X,newData_Y,newData_Z) #Reshapes the array into a points array

#################################################################################



#surface_Reconstruction.delaunay_original(points)
#surface_Reconstruction.alpha_Shape(points)
#surface_Reconstruction.ball_Pivoting(points)
surface_Reconstruction.poisson_surfRecon(points)