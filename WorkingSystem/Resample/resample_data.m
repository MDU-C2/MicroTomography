function points = resample_data(data,delta_z,delta_t,show_scatter,show_fit)
%% Move data down to 0
for i = 1:size(data,3)
    data(:,3,i) = data(:,3,i) - mean(data(1,3,:));
end
%% Prepare data fix nan 
% find longest column 
[~,I] = min(min(sum(isnan(data))));
% find min Z
indx_z = find(isnan(data(:,1,I)),1,'first');
indx_z = indx_z-1;
z_min = data(indx_z,3,I);
z_max = 0;

%%
new_z = z_min:delta_z:z_max;
spline_resample = zeros(size(new_z,2), 3, size(data,3));
for i = 1:size(data,3)
    x = data(:,1,i);
    y = data(:,2,i);
    z = data(:,3,i);
    % Add a point in the end so that the splines does not continue in a
    % different direction
    x(end +1,1) = 0;
    y(end +1,1) = 0;
    z(end +1,1) = z_min;
    
    % INTERPOLATION 
    % Make the code find 1, 11, 6, 16 automaticaly. 
    switch i
        % FOr Y i = 1 and i = 11 are linear interpolation change ti linear
    case i == 1 || i ==11
        x_spline = smooth_spline_zx(z,x,show_fit);
        y_spline = poly2_fit(z, y, show_fit);
         % FOr x i = 6 and 16 are linear 
    case i == 6 || i == 16
        x_spline = poly2_fit(z,x,false);
%         title(i);
        y_spline = smooth_spline_zx(z, y, show_fit);
    otherwise
        x_spline = smooth_spline_zx(z,x,show_fit);
%         title(i);
        y_spline = smooth_spline_zx(z, y, show_fit);
    end
    spline_resample(:,1,i) = x_spline(new_z);
    spline_resample(:,2,i) = y_spline(new_z);
    spline_resample(:,3,i) = new_z;
end
%% PLOT analyse solution
if show_scatter == true
figure; hold on; 
    for i = 1:size(data,3)
        scatter3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i),'filled','blue')
        scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled','red')
    end
    legend('Interpolated spline resampled', 'Laser data points')
end
%% Circular interpolation 
points = [];
new_theta = -pi:delta_t:pi;

for j = 1: size(spline_resample,1)
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    zz = squeeze(spline_resample(j,3,:));

    mux = mean(xx);
    muy = mean(yy);
    [Theta,R] = cart2pol(xx- mux,yy-muy);
    [Theta,ind] = sort(Theta);
    R = R(ind);
    r_theta_function = fourie_rtheta(Theta,R,show_fit);
    R_hat = r_theta_function(new_theta');
    [new_xx,new_yy] = pol2cart(new_theta',R_hat);
    
    if show_scatter == true
        figure; hold on; 
        plot(new_xx+mux,new_yy+muy,"blue")
        plot(xx,yy,'red')
        legend('Interpolated spline resampled', 'Laser data points')
    end
    points = [points; new_xx, new_yy, repmat(spline_resample(j,3,1),size(new_xx))];
end

%% 
if show_scatter == true
    figure; hold on;
    scatter3(points(:,1),points(:,2),points(:,3),'filled','blue')
    for i = 1:size(data,3)
        scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled','red')
    end
    legend('Interpolated spline resampled', 'Laser data points')
end
end

