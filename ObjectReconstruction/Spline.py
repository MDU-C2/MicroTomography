import numpy as np
import scipy as sp

class spline():
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
   
    
        return xnew,ynew,znew
    
    def spline_circle(data_x,data_y,newTheta,theta):
    
        cx = sp.interpolate.CubicSpline(theta,data_x)
        cy = sp.interpolate.CubicSpline(theta,data_y)

        return cx(newTheta),cy(newTheta)