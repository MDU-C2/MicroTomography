clc 
clear
close all

%rmpath('')
%addpath('connect_rob-mat','Protocall','PowerCrust','Robot')

t = ConnectRobot();

Scanpoints = create_scan_points(200,150,50,5); %% Scanpoints = []

%Test different points randomly from scanpoints
%TestRandPoints(Scanpoints,t);

tic
LaserPoints = collectLaserPoint(Scanpoints,t); %%LaserPoints = [laser pos rot]

surfacePoint = calcSurfacePoint(LaserPoints); %%surfacePoint = [x y z]

%%Interpolation
ppoints = resampling(surfacePoint,20,200);


poToPowerCrust = permute(ppoints,[1 3 2]);
poToPowerCrust = reshape(poToPowerCrust,[],size(ppoints,2),1);

[~,Mesh,~,~] = PowerCrust(poToPowerCrust,0);
toc
figure
shp = alphaShape(Mesh(:,1),Mesh(:,2),Mesh(:,3));
shape.alpha = 200;
figure;
plot(shp)