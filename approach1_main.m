clear all 
close all
clc

new_code = load ('SurfacePoint11231426_NecCodeEm.mat');
new_code = new_code.surfacePoint;

new_z =-1.*(0:0.2:100);
spline_resample = zeros(size(new_z,2), 3, size(new_code,3));

for i = 1:size(new_code,3)
    x = new_code(:,1,i);
    y = new_code(:,2,i);
    z = new_code(:,3,i);
    % INTERPOLATION
    % Make the linear part better by changing the fitting function 
    % Make the code find 1, 11, 6, 16 automaticaly. 

    switch i
        % FOr Y i = 1 and i = 11 are linear interpolation change ti linear
    case i == 1 || i ==11
        x_spline = createFit1(new_code(:,3,i),new_code(:,1,i),false);
        title(i);
        y_spline = poly_Fit2(new_code(:,3,i), new_code(:,2,i), false);
        title(i);
         % FOr x i = 6 and 16 are linear 
    case i == 6 || i == 16
        x_spline = poly_Fit3(new_code(:,3,i),new_code(:,1,i),false);
        title(i);
        y_spline = createFit2(new_code(:,3,i), new_code(:,2,i), false);
        title(i);
    otherwise
        x_spline = createFit1(new_code(:,3,i),new_code(:,1,i),true);
        title(i);
        y_spline = createFit2(new_code(:,3,i), new_code(:,2,i), true);
        title(i);
    end
    spline_resample(:,1,i) = x_spline(new_z);
    spline_resample(:,2,i) = y_spline(new_z);
    spline_resample(:,3,i) = new_z;

end
%% Plot results 
figure; hold on ; 
for i = 1:size(spline_resample,3)
    scatter3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i))
end

%% Create new dimension t 

% add dimension with zeros 
for i = 1 : size(spline_resample,3)
    spline_resample(:,4,i) = zeros(size(spline_resample,1),1);
end

for i = 1 : size(spline_resample,3)
    for j = 2: size(spline_resample,1)
        spline_resample(j,4,i) =  spline_resample(j-1,4,i) + sqrt( (spline_resample(j,1,i)-spline_resample(j-1,1,i))^2 + (spline_resample(j,2,i)-spline_resample(j-1,2,i))^2 );
    end
end

%% Circular interpolation 
for j = 1: size(spline_resample,1)
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    zz = squeeze(spline_resample(j,3,:));
    t = squeeze(spline_resample(j,4,:));

    if j == 1 || j == 50 || j == 100|| j == 200|| j == 300|| j == 400|| j == 500


%         scatter(xx,yy);
%         axis([-50 50 -50 50]);
%         axis equal;
%         initialparameter=[0 0 0];
%         mx=@(initialparameter)error_function(initialparameter,xx,yy);
%         [outputparameters, fval]=fminsearch(mx,initialparameter);
    end
end


%%
    x = new_code(:,1,11);
    y = new_code(:,2,11);
    z = new_code(:,3,11);
    figure; 
    scatter(y,z)
