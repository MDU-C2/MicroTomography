clc 
clear
close all

%rmpath('')
addpath('Protocall','PowerCrust','Robot')

t = ConnectRobot();
Mesh = scanBreast(t);

%%TEST

function Mesh = scanBreast(t)
    Scanpoints = create_scan_points(150,150,50,10,18,10,false);
    %Scanpoints = [125,0,-16,0,90,180;0,125,-16,0,90,90;-125,0,-16,0,90,0;0,-125,-16,0,90,-90;125,0,-16,0,90,-180];
    %Scanpoints(:,:,2) = Scanpoints;
    
    %Test different points randomly from scanpoints    
    %TestRandPoints(Scanpoints(:,:,:),t);
    
    tic
    
    %%Collect surface points: 
    LaserPoints = collectLaserPoint(Scanpoints,t); %%LaserPoints = [laser robPos robRot]
    surfacePoint = calcSurfacePoint(LaserPoints); %%surfacePoint = [x y z]
    toc
    %%Interpolation:
    ppoints = resampling(surfacePoint,2,200);
    
    %%PowerCrust:
    poToPowerCrust = permute(ppoints,[1 3 2]);
    poToPowerCrust = reshape(poToPowerCrust,[],size(ppoints,2),1);
    [~,Mesh,~,~] = PowerCrust(poToPowerCrust,0);
    
    toc
    
    figure
    shp = alphaShape(Mesh(:,1),Mesh(:,2),Mesh(:,3));
    shape.alpha = 200;
    figure;
    plot(shp)
end
