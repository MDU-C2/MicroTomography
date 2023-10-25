function points = resample_data(data,delta_z,delta_t,show_scatter,show_fit)

% The function resample the data with a delta z in height and delta t in
% circular samples , show_scatter and show fit is to plot the functions
% IF YOU SET THE PLOT TO TRUE THE FUNCTION WILL TAKE SOME TIME TO PLOT AND
% YOU WILL GET A LOT OF FIGURE 

% data: should be 3 dimensional [ Samples points, 3(x,y,z) , SPLINES ] 


%% Move data down to 0
% This is because of the gape in yumis callibration . You can comment this
% out and compare the results with the STL file. 
for i = 1:size(data,3)
    data(:,3,i) = data(:,3,i) - mean(data(1,3,:));
end
%% Prepare data fix nan 
% This is because the Yumi is not callibrated , we need to limit the
% splines to a point on the nipple otherwise the splines will continue to
% the other side while resampling. 
% This can be changed when yumi is callibrated. 
% find longest column 
[~,I] = min(min(sum(isnan(data))));
% find min Z
indx_z = find(isnan(data(:,1,I)),1,'first');
indx_z = indx_z-1;
z_min = data(indx_z,3,I);
z_max = 0;

%% Fit and resample splines 
new_z = z_min:delta_z:z_max; % new resampling vector
% Declare new resampled points. 
spline_resample = zeros(size(new_z,2), 3, size(data,3));
% for each spline
for i = 1:size(data,3)
    x = data(:,1,i);
    y = data(:,2,i);
    z = data(:,3,i);
    % Add a point in the end so that the splines does not continue in a
    % different direction the point is computed in the previous step
    x(end +1,1) = 0;
    y(end +1,1) = 0;
    z(end +1,1) = z_min;
    
    % INTERPOLATION 

    x_spline = smooth_spline_zx(z,x,show_fit);
    y_spline = smooth_spline_zx(z, y, show_fit);

    % Resample the splines at the new Z vector created in the begining. 
    spline_resample(:,1,i) = x_spline(new_z);
    spline_resample(:,2,i) = y_spline(new_z);
    spline_resample(:,3,i) = new_z;
end
%% PLOT Results if needed
if show_scatter == true
figure; hold on; 
    for i = 1:size(data,3)
        scatter3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i),'filled','blue')
        scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled','red')
    end
    legend('Interpolated spline resampled', 'Laser data points')
end
%% Circular interpolation 
% declare the new sampled points 
points = [];
% New sampling for the circles. 
new_theta = -pi:deg2rad(delta_t):pi;
% For every height 
for j = 1: size(spline_resample,1)
    % Extract the data of every circle ZZ should be the same for all points
    % because the data is resample in the spline to match in heigh with
    % new_z
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    zz = squeeze(spline_resample(j,3,:));
    % mean for normalization the data
    mux = mean(xx);
    muy = mean(yy);
    % change to polar coordinate
    [Theta,R] = cart2pol(xx- mux,yy-muy);
    % sort Theta and match it with R 
    [Theta,ind] = sort(Theta);
    R = R(ind);
    % fit theta and R with fourier series 
    r_theta_function = fourie_rtheta(Theta,R,show_fit);
    % resample R using the new theta
    R_hat = r_theta_function(new_theta');
    % convert back to cartezian space 
    [new_xx,new_yy] = pol2cart(new_theta',R_hat);
    % If plot is needed
    if show_scatter == true
        figure; hold on; 
        plot(new_xx+mux,new_yy+muy,"blue")
        plot(xx,yy,'red')
        legend('Interpolated spline resampled', 'Laser data points')
    end
    % Save the new resampled points
    points = [points; new_xx, new_yy, repmat(spline_resample(j,3,1),size(new_xx))];
end

%% If plots is needed
if show_scatter == true
    figure; hold on;
    scatter3(points(:,1),points(:,2),points(:,3),'filled','blue')
    for i = 1:size(data,3)
        scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled','red')
    end
    legend('Interpolated spline resampled', 'Laser data points')
end
end

