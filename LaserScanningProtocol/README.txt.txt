The scanning contains 3 Folders: 

1- Scanning Protocol - [Create and plot a cylindrical scanning positions]

create_scan_points(): Function create the scanning positions including orientation. 
show_HT(): Is used to display the scanning points and plot the orientation of the base coordinate system after applying the HT matrix. 
main.m : A script file to test and run the functions


2- Interpolation Resample - [Curve fitting of the scanned data and resampling of the curves]

resample_data(): Is the main function of this folder , it fits and resample the data into the desired density. 
fourie_rtheta(): Created by the curve fitting APP, fits fourie serie of 2nd degree to the polar coordinates. Used in resample_data()
smooth_spline_zx(): Created by the curve fitting APP, fitrs smooth splines to the data. Used in resample_data()
main.m : A script to test the main function resample_data()

3- Normal to the Surface step

This step is added to use the intial scan and create a new scanning position that is normal to the surface. Due to the time constrains and the Uncalibrated yumi
this step is not complete. 
find. 

The folder contains another folder that is the method to extract the surface normals. The reference to the author of this method is included in the license 
file in the findPointNormals folder. 

normal_scanning_protocol(): Takes the intial scan as input and use the first spline to create multiple duplicates rotated around the center. This is due to the 
uncalibrated yumi. The data is not smooth around the nipple region and will create different directions because unformality in the surface of the uncalibrated data. 
The function uses the findPointNormals files to find the normnal and calculate the orientation by finding the translation from the base coordinate to the new point 
coordinates. 