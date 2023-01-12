clear all
close all
clc
% Load STL file
[geo,stl_points] = load_stl("symmetricalBreastModel.STL");
figure; 
scatter3(stl_points(:,1),stl_points(:,2),stl_points(:,3),'filled');
set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');
% xlabel('X Axis','fontweight','bold')
% ylabel('Y Axis','fontweight','bold')
% zlabel('Z Axis','fontweight','bold')
% Convert to cylindrical coordinates
[theta,rho,z] = cart2pol(stl_points(:,1),stl_points(:,2),stl_points(:,3)); 
% Sort THeta
[theta,I] = sort(theta);
rho = rho(I);
z = z(I);
% Find occurence of each Theta
rounded_theta = round(theta*10)/10;
[GC,GR] = groupcounts(rounded_theta);
% Devide data into splines for theta that occures 27 times
spline_count27 = 1;
spline_count10 = 1;
for i=1:size(GR)
    if GC(i) == 27
        K = find(rounded_theta == GR(i));
        cylind_coord_27(:,1,spline_count27) = theta(K);
        cylind_coord_27(:,2,spline_count27) = rho(K);
        cylind_coord_27(:,3,spline_count27) = z(K);
        spline_count27 = spline_count27+1;
    end
    if GC(i) == 10
        K = find(rounded_theta == GR(i));
        cylind_coord_10(:,1,spline_count10) = theta(K);
        cylind_coord_10(:,2,spline_count10) = rho(K);
        cylind_coord_10(:,3,spline_count10) = z(K);
        spline_count10 = spline_count10+1;
    end
end
% Convert to cartesian coordiantes
for i = 1:size(cylind_coord_27,3)
    [data_27(:,1,i),data_27(:,2,i),data_27(:,3,i)] = pol2cart(cylind_coord_27(:,1,i),cylind_coord_27(:,2,i),cylind_coord_27(:,3,i));
end

for i = 1:size(cylind_coord_10,3)
    
    [data_10(:,1,i),data_10(:,2,i),data_10(:,3,i)] = pol2cart(cylind_coord_10(:,1,i),cylind_coord_10(:,2,i),cylind_coord_10(:,3,i));
end

figure; hold on; 
for i= 1:size(data_27,3)
    scatter3(data_27(:,1,i),data_27(:,2,i),data_27(:,3,i),'black')
    drawnow
    view(3)
end
hold on;
for i= 1:size(data_10,3)
    scatter3(data_10(:,1,i),data_10(:,2,i),data_10(:,3,i),'red')
    drawnow
    view(3)
end
%%




i = 1; ind_interval = 1:27;
[asym_points(:,1,i),asym_points(:,2,i),asym_points(:,3,i)]= pol2cart(theta(ind_interval),rho(ind_interval),z(ind_interval)); 
i = i +1; ind_interval = 28:54;
[asym_points(:,1,i),asym_points(:,2,i),asym_points(:,3,i)]= pol2cart(theta(ind_interval),rho(ind_interval),z(ind_interval)); 
i = i +1; ind_interval = 55:64;
[asym_points(:,1,i),asym_points(:,2,i),asym_points(:,3,i)]= pol2cart(theta(ind_interval),rho(ind_interval),z(ind_interval)); 
i = i +1; ind_interval = 65:91;
[asym_points(:,1,i),asym_points(:,2,i),asym_points(:,3,i)]= pol2cart(theta(ind_interval),rho(ind_interval),z(ind_interval)); 
i = i +1; ind_interval = 92:118;
[asym_points(:,1,i),asym_points(:,2,i),asym_points(:,3,i)]= pol2cart(theta(ind_interval),rho(ind_interval),z(ind_interval)); 
i = i +1; ind_interval = 119:128;
[asym_points(:,1,i),asym_points(:,2,i),asym_points(:,3,i)]= pol2cart(theta(ind_interval),rho(ind_interval),z(ind_interval)); 
i = i +1; ind_interval = 129:155;
[asym_points(:,1,i),asym_points(:,2,i),asym_points(:,3,i)]= pol2cart(theta(ind_interval),rho(ind_interval),z(ind_interval)); 






figure; 
scatter3(stl_points(:,1),stl_points(:,2),stl_points(:,3))