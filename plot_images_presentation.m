clear all
close all
clc
% Load STL file
[geo,stl_points] = load_stl("symmetricalBreastModel.STL");
figure; 
scatter3(stl_points(:,1),stl_points(:,2),stl_points(:,3),'.','black');
set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');

% tic
% [~,Mesh,~,~,~] = PowerCrust(stl_points,0); 
% toc
shp = alphaShape(stl_points(:,1),stl_points(:,2),stl_points(:,3),50)
figure;
plot(shp,'FaceColor',[.7 .7 .7])
set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');

%%
clear all
close all 
clc 

new_code = load ('surfacePoint12060940_90deg_20step (1).mat');
new_code = new_code.surfacePoint;
data = new_code;

azimuth = linspace(0,360-(360/20),20);

new_data = zeros(size(data,1),3,size(azimuth,2));

for i = 1:size(azimuth,2)
    rotate = rotz(azimuth(i));
    rot_data = rotate*data(:,:,1)';
    new_data(:,:,i) = rot_data';
end

figure; hold on; 
for i = 1:size(new_data,3)
    scatter3(new_data(:,1,i),new_data(:,2,i),new_data(:,3,i),'filled')
end
set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');
%% calculate surface normal 
points = [];%zeros(size(power_crust_points,1)*size(power_crust_points,3),3);
for i = 1:size(new_data,3)
    points = [points; new_data(:,:,i)];
end
[normals,curvature] = findPointNormals(points,[],[0,0,10],true);
 normals = -normals;

 figure; hold on; 
 scatter3(points(:,1),points(:,2),points(:,3),'filled')
 quiver3(points(:,1),points(:,2),points(:,3), ...
     normals(:,1),normals(:,2),normals(:,3),'LineWidth',2, 'Color','black')

set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');
%% Splines
%%
delta_z = 5;
z_min = -84.6797;
new_z = z_min:delta_z:20;
spline_resample = zeros(size(new_z,2), 3, size(new_data,3));

figure; hold on;

for i = 1:size(new_data,3)
    x = new_data(:,1,i);
    y = new_data(:,2,i);
    z = new_data(:,3,i);


    % INTERPOLATION
    % Make the linear part better by changing the fitting function 
    % Make the code find 1, 11, 6, 16 automaticaly. 
    
    switch i
        % FOr Y i = 1 and i = 11 are linear interpolation change ti linear
    case i == 1 || i ==11
        x_spline = smooth_spline_zx(z,x,false);
        y_spline = poly2_fit(z, y, false);
         % FOr x i = 6 and 16 are linear 
    case i == 6 || i == 16
        x_spline = poly2_fit(z,x,false);
%         title(i);
        y_spline = smooth_spline_zx(z, y, false);
    otherwise
        x_spline = smooth_spline_zx(z,x,false);
%         title(i);
        y_spline = smooth_spline_zx(z, y, false);
    end
    spline_resample(:,1,i) = x_spline(new_z);
    spline_resample(:,2,i) = y_spline(new_z);
    spline_resample(:,3,i) = new_z;
    plot3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i), 'LineWidth',3)
    scatter3(new_data(:,1,i),new_data(:,2,i),new_data(:,3,i),'filled')
end
set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');


%% Circular interpolation 
delta_t = 0.07;
points = [];
new_theta = -pi:delta_t:pi+0.1;
figure; hold on; 
% for i = 1:size(spline_resample,3)
% scatter3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i),'filled','red')
% end
for j = 1: size(spline_resample,1)
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    zz = squeeze(spline_resample(j,3,:));


    mux = mean(xx);
    muy = mean(yy);
    [Theta,R] = cart2pol(xx- mux,yy-muy);
    [Theta,ind] = sort(Theta);
    R = R(ind);
    r_theta_function = fourie_rtheta(Theta,R,false);
    R_hat = r_theta_function(new_theta');
    [new_xx,new_yy] = pol2cart(new_theta',R_hat);

%     figure; hold on; 
%     plot(xx,yy,'red')
%     plot(new_xx+mux,new_yy+muy,"blue")
%     legend('Scanned Points', 'Resampled interpolated')
    
    points = [points; new_xx, new_yy, repmat(spline_resample(j,3,1),size(new_xx))];
    %plot3(new_xx,new_yy,repmat(zz(1),size(new_xx,1),1),'LineWidth',3)
    scatter3(new_xx,new_yy,repmat(zz(1),size(new_xx,1),1),'filled','black')
end
set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');
%%
shp = alphaShape(points(:,1),points(:,2),points(:,3),50)
figure;
plot(shp,'FaceColor',[.7 .7 .7])
set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');

%% Results

clear all
close all
clc

new_code = load ('surfacePoints0912_1219.mat');
new_code = new_code.surfacePoint;
data = new_code;
for i = 1:size(data,3)
    data(:,3,i) = data(:,3,i) - mean(data(1,3,:));
end
% points = resample_data(data,6,0.02,false,false);
figure; hold on;
% scatter3(points(:,1),points(:,2),points(:,3),'blue')
for i = 1:size(data,3)/2 
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'red','filled')
end
% scatter3(points(:,1),points(:,2),points(:,3),'blue')
for i = size(data,3)/2+1:size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'green','filled')
end
set(gca, 'Visible', 'off');
colorbar('off');set(gca, 'Visible', 'off');
colorbar('off');

%%
figure; hold on; 
plot(data(:,2,6),data(:,3,6), 'LineWidth',3,'Color','red');
plot(data(:,2,16),data(:,3,16), 'LineWidth',3,'color','green');
xlabel('Y axis','fontweight','bold','fontsize',16)
ylabel('Z axis','fontweight','bold','fontsize',16)
set(gca,'fontweight','bold','fontsize',16);


%% Prepare data fix nan 

% find longest column 
[A,I] = min(min(sum(isnan(data))));
indx_z = find(isnan(data(:,1,I)),1,'first');
indx_z = indx_z-1;
z_min = data(indx_z,3,I);
z_max = 9;

%%
delta_z = 5;
new_z = z_min:delta_z:z_max;
spline_resample = zeros(size(new_z,2), 3, size(data,3));

for i = 1:size(data,3)
    x = data(:,1,i);
    y = data(:,2,i);
    z = data(:,3,i);

    x(end +1,1) = 0;
    y(end +1,1) = 0;
    z(end +1,1) = z_min;
    % INTERPOLATION
    % Make the linear part better by changing the fitting function 
    % Make the code find 1, 11, 6, 16 automaticaly. 
    
    switch i
        % FOr Y i = 1 and i = 11 are linear interpolation change ti linear
    case i == 1 || i ==11
        x_spline = smooth_spline_zx(z,x,false);
        y_spline = poly2_fit(z, y, false);
         % FOr x i = 6 and 16 are linear 
    case i == 6 || i == 16
        x_spline = poly2_fit(z,x,false);
%         title(i);
        y_spline = smooth_spline_zx(z, y, false);
    otherwise
        x_spline = smooth_spline_zx(z,x,false);
%         title(i);
        y_spline = smooth_spline_zx(z, y, false);
    end
    spline_resample(:,1,i) = x_spline(new_z);
    spline_resample(:,2,i) = y_spline(new_z);
    spline_resample(:,3,i) = new_z;
end

figure; hold on; 
for i = 1:size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled');
    plot3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i), 'linewidth', 3)
end
xlabel('X axis','fontweight','bold','fontsize',16)
ylabel('Y axis','fontweight','bold','fontsize',16)
zlabel('Z axis','fontweight','bold','fontsize',16)
set(gca,'fontweight','bold','fontsize',16);
%% 
figure; hold on; 
for i = 1:size(data,3)
    scatter3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i),'filled', 'red');
    plot3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i), 'linewidth', 3)
end
xlabel('X axis','fontweight','bold','fontsize',16)
ylabel('Y axis','fontweight','bold','fontsize',16)
zlabel('Z axis','fontweight','bold','fontsize',16)
set(gca,'fontweight','bold','fontsize',16);

%% Circular interpolation 
delta_t = 0.05;
points = [];
new_theta = -(pi+delta_t):delta_t:pi+delta_t;
% figure; hold on; 
% for i = 1:size(spline_resample,3)
%     scatter3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i),'filled', 'red');
% end
for j = 1: size(spline_resample,1)
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    zz = squeeze(spline_resample(j,3,:));

    mux = mean(xx);
    muy = mean(yy); 
    [Theta,R] = cart2pol(xx- mux,yy-muy);
    [Theta,ind] = sort(Theta);
    R = R(ind);
    r_theta_function = fourie_rtheta(Theta,R,false);
    R_hat = r_theta_function(new_theta');
    [new_xx,new_yy] = pol2cart(new_theta',R_hat);

%     figure; hold on; 
%     plot(xx,yy,'red')
%     plot(new_xx+mux,new_yy+muy,"blue")
%     legend('Scanned Points', 'Resampled interpolated')

%     plot3(new_xx,new_yy,repmat(zz(1),size(new_xx)),'LineWidth',3)
    points = [points; new_xx, new_yy, repmat(spline_resample(j,3,1),size(new_xx))];
end
xlabel('X axis','fontweight','bold','fontsize',16)
ylabel('Y axis','fontweight','bold','fontsize',16)
zlabel('Z axis','fontweight','bold','fontsize',16)
set(gca,'fontweight','bold','fontsize',16);
%%
figure; hold on; 
scatter3(points(:,1),points(:,2),points(:,3), 'filled', 'black')
xlabel('X axis','fontweight','bold','fontsize',16)
ylabel('Y axis','fontweight','bold','fontsize',16)
zlabel('Z axis','fontweight','bold','fontsize',16)
set(gca,'fontweight','bold','fontsize',16);

%% 
[~,Mesh,~,~,~] = PowerCrust(points,0); 

