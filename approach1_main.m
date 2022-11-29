clear all 
close all
clc

new_code = load ('SurfacePoint11231426_NecCodeEm.mat');
new_code = new_code.surfacePoint;

new_z =-1.*(0:3:100);
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
        x_spline = createFitx(new_code(:,3,i),new_code(:,1,i),false);
        title(i);
        y_spline = poly_Fity(new_code(:,3,i), new_code(:,2,i), false);
        title(i);
         % FOr x i = 6 and 16 are linear 
    case i == 6 || i == 16
        x_spline = poly_Fitx(new_code(:,3,i),new_code(:,1,i),false);
        title(i);
        y_spline = createFity(new_code(:,3,i), new_code(:,2,i), false);
        title(i);
    otherwise
        x_spline = createFitx(new_code(:,3,i),new_code(:,1,i),false);
        title(i);
        y_spline = createFity(new_code(:,3,i), new_code(:,2,i), false);
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

% %% add dimension with zeros 
% for i = 1 : size(spline_resample,3)
%     spline_resample(:,4,i) = zeros(size(spline_resample,1),1);
% end
% %% calculate t dimension 
% for j = 1 : size(spline_resample,1)
% 
%     for k = 2: size(spline_resample,3)
%         spline_resample(j,4,k) =  spline_resample(j,4,k-1) + sqrt( (spline_resample(j,1,k)-spline_resample(j,1,k-1))^2 + (spline_resample(j,2,k)-spline_resample(j,2,k-1))^2 );
%     end
% end

%% Circular interpolation WHY IT DOES NOT WORK

% for j = 1: size(spline_resample,1)
%     xx = squeeze(spline_resample(j,1,:));
%     yy = squeeze(spline_resample(j,2,:));
%     zz = squeeze(spline_resample(j,3,:));
%     t = squeeze(spline_resample(j,4,:));
%     new_t = 0:0.2:max(spline_resample(j,4,:));
%     new_t = [new_t 0];
%     x_circ = createFit_tx_circ(t, xx, true); 
%     y_circ = createFit_ty_circ(t, yy, false);
%     if j == 10 || j == 100 || j == 200 || j == 300 || j == 400 || j == 500
%         figure; plot(x_circ(new_t), y_circ(new_t))
%     end
% end

%% Circular interpolation 
step_size_t = 0.05;
t=0:step_size_t:2*pi;
%power_crust_points = zeros (size(t,2),3,size(spline_resample,1));
points = [];
tic
for j = 1: size(spline_resample,1)
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    zz = squeeze(spline_resample(j,3,:));
    initialparameter=[10 10 0 -50 30];
    mx=@(initialparameter)error_function(initialparameter,xx,yy);
    [outputparameters, fval]=fminsearch(mx,initialparameter);
    % plot
%     if j == 10 || j == 100 || j == 200 || j == 300 || j == 400 || j == 500
%         figure;
%         initialparameter=[10 10 0 -50 30];
%         mx=@(initialparameter)error_function(initialparameter,xx,yy);
%         [outputparameters, fval]=fminsearch(mx,initialparameter);
%     end
    % Resample



    if j ==1
        radius1 = linspace(0,outputparameters(1),round(outputparameters(1)/5));
        radius2 = linspace(0,outputparameters(2),round(outputparameters(1)/5));
        for k = 1:size(radius2,2)
            xao=outputparameters(4)+radius1(k)*cos(t);
            yao=outputparameters(5)+radius2(k)*sin(t);
            a=outputparameters(3);
            z=[cos(a) -sin(a);sin(a) cos(a)];
            m=[xao;yao];
            k=z*m;
            xao=k(1,:);
            yao=k(2,:);
            points = [points; xao' yao' repmat(spline_resample(j,3,1),size(xao))'];
        end
    elseif j == size(spline_resample,1)
        radius1 = linspace(0,outputparameters(1),round(outputparameters(1)/5));
        radius2 = linspace(0,outputparameters(2),round(outputparameters(1)/5));
        for k = 1:size(radius2,2)
            xao=outputparameters(4)+radius1(k)*cos(t);
            yao=outputparameters(5)+radius2(k)*sin(t);
            a=outputparameters(3);
            z=[cos(a) -sin(a);sin(a) cos(a)];
            m=[xao;yao];
            k=z*m;
            xao=k(1,:);
            yao=k(2,:);
            points = [points; xao' yao' repmat(spline_resample(j,3,1),size(xao))'];
        end
    else
        xao=outputparameters(4)+outputparameters(1)*cos(t);
        yao=outputparameters(5)+outputparameters(2)*sin(t);
        a=outputparameters(3);
        z=[cos(a) -sin(a);sin(a) cos(a)];
        m=[xao;yao];
        k=z*m;
        xao=k(1,:);
        yao=k(2,:);
        points = [points; xao' yao' repmat(spline_resample(j,3,1),size(xao))'];
    end

    % Create points
%     power_crust_points(:,1,j) = xao;
%     power_crust_points(:,2,j) = yao;
%     power_crust_points(:,3,j) = repmat(spline_resample(j,3,1),size(xao));
end
toc
%% 
points = [];%zeros(size(power_crust_points,1)*size(power_crust_points,3),3);
figure; hold on;
for i = 1:size(power_crust_points,3)
    scatter3(power_crust_points(:,1,i),power_crust_points(:,2,i),power_crust_points(:,3,i))
    points = [points; power_crust_points(:,:,i)];
end

%%
figure;

scatter3(points(:,1),points(:,2),points(:,3))

%%

tic
[~,Mesh,~,~,~] = PowerCrust(points,1); 
toc
