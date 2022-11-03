clc 
clear all;

%%%%
RobotCon = ConnectRobot;
calcSurfacePoint = laserPointToRealPoint;
CollectLaserPoints = collectLaserPoint;
%%%%


t = RobotCon.connect();

Scanpoints = create_scan_points(200,150,50,5); %% Scanpoints = []

LaserPoints = CollectLaserPoints.collect(Scanpoints,t); %%LaserPoints = [laser pos rot]

surfacePoint = calcSurfacePoint.calcSurfacePoint(LaserPoints); %%surfacePoint = [x y z]


