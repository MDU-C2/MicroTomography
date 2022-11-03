clc 
clear all;

%%%%
RobotCon = ConnectRobot;
calcSurfacePoint = laserPointToRealPoint;
CollectLaserPoints = collectLaserPoint;
%%%%


t = RobotCon.connect();

Scanpoints = create_scan_points(200,200,100,5); %% Scanpoints = []

LaserPoints = CollectLaserPoints.collect(Scanpoints); %%LaserPoints = [laser pos rot]

surfacePoint = calcSurfacePoint.calcSurfacePoint(LaserPoints); %%surfacePoint = [x y z]


