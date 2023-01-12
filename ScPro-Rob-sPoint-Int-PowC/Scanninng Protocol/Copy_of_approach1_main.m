clear all 
close all
clc

new_code = load ('surfacePoints0912_1219.mat');
new_code = new_code.surfacePoint;
data = new_code;
%% ONE FUNCTION TO RUN THEM ALL
% points = resample_data(data,6,0.02,false,false);
figure; hold on;
% scatter3(points(:,1),points(:,2),points(:,3),'blue')
for i = 1:size(data,3)/2 
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'red')
end

% scatter3(points(:,1),points(:,2),points(:,3),'blue')
for i = size(data,3)/2+1:size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'black')
end
%%
tic
[~,Mesh,~,~,~] = PowerCrust(points,0); 
toc
%% Move data down to 0
for i = 1:size(data,3)
    data(:,3,i) = data(:,3,i) - mean(data(1,3,:));
end
%% Prepare data fix nan 

% find longest column 
[A,I] = min(min(sum(isnan(data))));
indx_z = find(isnan(data(:,1,I)),1,'first');
indx_z = indx_z-1;
z_min = data(indx_z,3,I);
z_max = 0;

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
%% PLOT analyse solution
figure; hold on; 
for i = 1:size(data,3)
    scatter(data(:,1,i),data(:,3,i))
    scatter(data(:,2,i),data(:,3,i))
end
xlabel('X')
ylabel('Z')

figure; hold on; 
for i = 1:size(data,3)
    scatter(data(:,2,i),data(:,3,i))
end
xlabel('Y')
ylabel('Z')

figure; hold on; 
for i = 1:size(data,3)
    plot3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i))
end

%% Circular interpolation 
delta_t = 0.05;
points = [];
new_theta = -pi:0.1:pi;
for j = 1: size(spline_resample,1)
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    zz = squeeze(spline_resample(j,3,:));
    for k = 2:size(tt,1)
        tt(k,1) = tt(k-1) + sqrt( ( xx(k) - xx(k-1) )^2  +  (yy(k) - yy(k-1) )^2   );
    end

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
end

%% 
    figure; hold on;
    scatter3(points(:,1),points(:,2),points(:,3))
    for i = 1:size(data,3)
        scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled','red')
    end
%%

tic
[~,Mesh,~,~,~] = PowerCrust(points,0); 
toc
%%
stl_data = stlread("symmetricalBreastModel.STL");
[~,Mesh2,~,~,~] = PowerCrust(stl_data.Points,0); 