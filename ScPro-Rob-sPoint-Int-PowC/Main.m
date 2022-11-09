clc 
clear
close all

addpath('connect_rob-mat','Protocall','PowerCrust','LaserPointToRealpoint')

%%%%
RobotCon = ConnectRobot;
calcSurfacePoint = laserPointToRealPoint;
CollectLaserPoints = collectLaserPoint; 
%%%%


t = RobotCon.connect();

Scanpoints = create_scan_points(200,150,50,5); %% Scanpoints = []
tic
LaserPoints = CollectLaserPoints.collect(Scanpoints,t); %%LaserPoints = [laser pos rot]

surfacePoint = calcSurfacePoint.calcSurfacePoint(LaserPoints); %%surfacePoint = [x y z]

%%Interpolation
ppoints = resampling(surfacePoint,5,200);


poToPowerCrust = permute(ppoints,[1 3 2]);
poToPowerCrust = reshape(poToPowerCrust,[],size(ppoints,2),1);

[~,Mesh,~,~] = PowerCrust(poToPowerCrust,0);
toc
figure
shp = alphaShape(Mesh(:,1),Mesh(:,2),Mesh(:,3));
shape.alpha = 200;
figure;
plot(shp)