function spline_resample = spline_resampling(data,delta_z)
    %% This function fits the relation between Z and X , Z and Y 
    % and resample the splines with an interval of deltaz
    % Create new Z for resampling
    new_z =-1.*(0:delta_z:abs(min(min(data(:,3,:)))));
    % Prepare the new data array 
    spline_resample = zeros(size(new_z,2), 3, size(data,3));
    % for every spline 
    for i = 1:size(data,3)

        % INTERPOLATION
        % To make it better : Choose another linear interpolation when
        % spline is 0, 90, 180 , 270 degrees because the relation between
        % Z and X , Z and Y is linear and not spline. 
        % A spline in those angles make the spline go through all points 

        % To make it better derive the spline number i = 1, 11, 6, 16 from
        % the azimuth angle chosen in the protocol. The angle used in this
        % code is 18 degrees and that leads to that those i represents the
        % certain normal splines to the dimension of X or Y. 
        switch i
            % FOr Y i = 1 and i = 11 are linear interpolation change ti linear
        case i == 1 || i ==11
            x_spline = createFitx(data(:,3,i),data(:,1,i),false);
            y_spline = poly_Fity(data(:,3,i), data(:,2,i), false);
             % FOr x i = 6 and 16 are linear 
        case i == 6 || i == 16
            x_spline = poly_Fitx(data(:,3,i),data(:,1,i),false);
            y_spline = createFity(data(:,3,i), data(:,2,i), false);
        otherwise
            x_spline = createFitx(data(:,3,i),data(:,1,i),false);
            y_spline = createFity(data(:,3,i), data(:,2,i), false);
        end
        % Resampling
        spline_resample(:,1,i) = x_spline(new_z);
        spline_resample(:,2,i) = y_spline(new_z);
        spline_resample(:,3,i) = new_z;
    end
end

