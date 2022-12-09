clear all 
close all
clc

new_code = load ('surfacePoint11221617_RemoveLightAboveExtra.mat');
new_code = new_code.surfacePoints;
data = new_code;
%% FUnction for all above 
delta_z = 1;
step_size_t = 0.2;
points = resample_points(data, delta_z, step_size_t);

%% PLOt results
figure;hold on;
for i = 1:size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled', 'black')
    drawnow
end
scatter3(points(:,1),points(:,2),points(:,3),'filled', 'red')
xlabel('X')
ylabel('Y')
zlabel('Z')


%
for i = size(data,3)/2 +2 :size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled','red')
    drawnow
end
%scatter3(points(:,1),points(:,2),points(:,3),'filled', 'red')

%% POWERCRUST
[~,Mesh,~,~,~] = PowerCrust(points,0); 

%% Prepare data fix nan 

% find longest column 
[A,I] = min(min(sum(isnan(data))));

for i = 1:size(data,3)
    % create nan index
    nan_indexes = zeros(size(data,1),1,'logical');
    % find nan values
    nan_indexes(5:end)  = isnan(data(5:end,1,i));
    % replace nan values with longest column 
    data(nan_indexes,:,i) = data(nan_indexes,:,I);
end
%%
data = prepare_data(data);
%%
delta_z = 1;
new_z =-1.*(0:delta_z:abs(min(min(data(:,3,:)))));

spline_resample = zeros(size(new_z,2), 3, size(data,3));

for i = 1:size(data,3)
    x = data(:,1,i);
    y = data(:,2,i);
    z = data(:,3,i);
    % INTERPOLATION
    % Make the linear part better by changing the fitting function 
    % Make the code find 1, 11, 6, 16 automaticaly. 

    switch i
        % FOr Y i = 1 and i = 11 are linear interpolation change ti linear
    case i == 1 || i ==11
        x_spline = createFitx(data(:,3,i),data(:,1,i),false);
        y_spline = poly_Fity(data(:,3,i), data(:,2,i), false);
         % FOr x i = 6 and 16 are linear 
    case i == 6 || i == 16
        x_spline = poly_Fitx(data(:,3,i),data(:,1,i),false);
%         title(i);
        y_spline = createFity(data(:,3,i), data(:,2,i), false);
    otherwise
        x_spline = createFitx(data(:,3,i),data(:,1,i),false);
%         title(i);
        y_spline = createFity(data(:,3,i), data(:,2,i), false);
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
%% Finding normal vector
clear all 
close all
clc

new_code = load ('SurfacePoint11231426_NecCodeEm.mat');
new_code = new_code.surfacePoint;
data = new_code;

i = 18;

x = data(:,1,i);
y = data(:,2,i);
z = data(:,3,i);

% fig = figure; 
% scatter3(x,y,z);
% xlabel('X')
% ylabel('Y')
% zlabel('Z')


ppx = spline(x,z);


dppx = fnder(ppx,1);

x_point = 30 ; 
y_point = ppval(ppx,x_point);

fig = figure; hold on;
scatter(x_point, y_point, 'filled')
fnplt(ppx)

slope = ppval(dppx,x_point);
b = y_point - slope.*x_point;

x_line = linspace(10,50,50);

y_line = slope.*(x_line) + b;

figure(fig);hold on; 
plot(x_line, y_line)

normal_slope = -slope;
normal_b = y_point - normal_slope.*x_point;

x_normal = linspace(10,50,50);

y_normal = normal_slope.*(x_normal) + normal_b;

figure(fig);hold on; 
plot(x_normal, y_normal)

angle = rad2deg(atan(normal_slope));

ppy = spline(y,z);
dppy = fnder(ppy,1);
x_point2 = -21 ; 
y_point2 = ppval(ppy,x_point2);

figure(fig); hold on;
scatter(x_point2, y_point2, 'filled')
fnplt(ppy)

slope2 = ppval(dppy,x_point2);
b2 = y_point2 - slope2.*x_point2;

x_line2 = linspace(-10,-50,50);

y_line2 = slope2.*(x_line2) + b2;

figure(fig);hold on; 
plot(x_line2, y_line2)

normal_slope2 = -slope2;
normal_b2 = y_point2 - normal_slope2.*x_point2;

x_normal2 = linspace(-10,-50,50);

y_normal2 = normal_slope2.*(x_normal2) + normal_b2;

figure(fig);hold on; 
plot(x_normal2, y_normal2)

angle2 = rad2deg(atan(normal_slope2));


%% klad

eval_dppx = ppval(dppx,new_x);
angles = (pi/2) -atan2(eval_dppx,1);
angles = rad2deg(angles);

xx = new_x + 2*cos(angles);
yy = new_z + 2*sin(angles);

nxx = new_x + 2*cos(0);
nyy = new_z + 2*sin(0);

figure; hold on;
fnplt(ppx)
quiver(new_x, ppval(ppx,new_x), xx, yy)
quiver(new_x, ppval(ppx,new_x), nxx, nyy)
scatter(new_x, new_z)






%%
delta_z = 1;
spline_resample = spline_resampling(data, delta_z);
%% Plot results 
figure; hold on ; 
for i = 1:size(spline_resample,3)
    scatter3(spline_resample(:,1,i),spline_resample(:,2,i),spline_resample(:,3,i))
end

figure; hold on ; 
for i = 1:size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i))
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
step_size_t = 0.2;
t=0:step_size_t:2*pi;
%power_crust_points = zeros (size(t,2),3,size(spline_resample,1));
points = [];
tic
for j = 1: size(spline_resample,1)
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    zz = squeeze(spline_resample(j,3,:));
    % Search for solution 
    initialparameter=[10 10 0 0 0];
    mx=@(initialparameter)error_function(initialparameter,xx,yy);
    [outputparameters, fval]=fminsearch(mx,initialparameter);
    % plot
%     if j == 1 || j == 10 || j == 50 || j == 80 || j == 90 || j == 100
%         figure;
%         initialparameter=[10 10 0 -50 30];
%         mx=@(initialparameter)error_function(initialparameter,xx,yy);
%         [outputparameters, fval]=fminsearch(mx,initialparameter);
%     end
    % Resample

        xao=outputparameters(4)+outputparameters(1)*cos(t);
        yao=outputparameters(5)+outputparameters(2)*sin(t);
        a=outputparameters(3);
        z=[cos(a) -sin(a);sin(a) cos(a)];
        m=[xao;yao];
        k=z*m;
        xao=k(1,:);
        yao=k(2,:);
        points = [points; xao' yao' repmat(spline_resample(j,3,1),size(xao))'];

%     if j ==0%1
%         radius1 = linspace(0,outputparameters(1),round(outputparameters(1)/5));
%         radius2 = linspace(0,outputparameters(2),round(outputparameters(1)/5));
%         for k = 1:size(radius2,2)
%             xao=outputparameters(4)+radius1(k)*cos(t);
%             yao=outputparameters(5)+radius2(k)*sin(t);
%             a=outputparameters(3);
%             z=[cos(a) -sin(a);sin(a) cos(a)];
%             m=[xao;yao];
%             k=z*m;
%             xao=k(1,:);
%             yao=k(2,:);
%             points = [points; xao' yao' repmat(spline_resample(j,3,1),size(xao))'];
%         end
%     elseif j ==0% size(spline_resample,1)
%         radius1 = linspace(0,outputparameters(1),round(outputparameters(1)/5));
%         radius2 = linspace(0,outputparameters(2),round(outputparameters(1)/5));
%         for k = 1:size(radius2,2)
%             xao=outputparameters(4)+radius1(k)*cos(t);
%             yao=outputparameters(5)+radius2(k)*sin(t);
%             a=outputparameters(3);
%             z=[cos(a) -sin(a);sin(a) cos(a)];
%             m=[xao;yao];
%             k=z*m;
%             xao=k(1,:);
%             yao=k(2,:);
%             points = [points; xao' yao' repmat(spline_resample(j,3,1),size(xao))'];
%         end
%     else
%         xao=outputparameters(4)+outputparameters(1)*cos(t);
%         yao=outputparameters(5)+outputparameters(2)*sin(t);
%         a=outputparameters(3);
%         z=[cos(a) -sin(a);sin(a) cos(a)];
%         m=[xao;yao];
%         k=z*m;
%         xao=k(1,:);
%         yao=k(2,:);
%         points = [points; xao' yao' repmat(spline_resample(j,3,1),size(xao))'];
%     end

    % Create points
%     power_crust_points(:,1,j) = xao;
%     power_crust_points(:,2,j) = yao;
%     power_crust_points(:,3,j) = repmat(spline_resample(j,3,1),size(xao));
end
toc
%% 
step_size_t = 0.2;
points = circular_resampling(spline_resample,step_size_t);
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
[~,Mesh,~,~,~] = PowerCrust(points,0); 
toc
%%
stl_data = stlread("symmetricalBreastModel.STL");
[~,Mesh2,~,~,~] = PowerCrust(stl_data.Points,0); 