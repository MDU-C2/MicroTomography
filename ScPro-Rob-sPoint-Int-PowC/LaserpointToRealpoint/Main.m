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


for s = 2:size(surfacePoint,3)
    for r = 1:size(surfacePoint,1)
        scatter3(surfacePoint(r,1,s),surfacePoint(r,2,s),surfacePoint(r,3,s),'filled');
        hold on;
    end
end