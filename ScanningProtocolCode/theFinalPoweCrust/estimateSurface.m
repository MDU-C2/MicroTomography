function [x,y,z,MeshVerts,MeshEdges,MedialAxis,MAT,vert] = estimateSurface(amountOfSamples,noiseRange,sizeOfPhantom)
% 
%%%% In general, you can estimate the radius as; r = a + (b-a).*rand(N,1) 
%%%% to get values between the a and b. 
num_theta=36;

RadiusRandom        = (sizeOfPhantom-noiseRange) + noiseRange*2*rand(1,amountOfSamples); %%% getting r ranging from the 95-100 as state in the fomula above
 
azimuth             =  0:((360/(amountOfSamples))*pi)/180:(2*pi); %  = linspace(0, 360,amountOfSamples); %%% the angles in x,y-plane 
elivation           =  linspace(pi/2,0,amountOfSamples);  %linspace(0,90,amountOfSamples); %%% only half of the sphere
r                   = (sizeOfPhantom-noiseRange) + noiseRange*2*rand(1,amountOfSamples); %%% getting r ranging from the 95-100 as state in the fomula above 
[azimuth,elivation] = meshgrid(azimuth,elivation); 
% [x,y,z]             = sph2cart(azimuth,elivation,r); %%% just convertion to car-coordinates
points              = zeros(amountOfSamples*amountOfSamples,3);

x = r .* cos(elivation) .* cos(azimuth);
y = r .* cos(elivation) .* sin(azimuth);
z = r .* sin(elivation) ;

for i=1:amountOfSamples
    points(1+amountOfSamples*(i-1):amountOfSamples+amountOfSamples*(i-1),1) = x(:,i);
    points(1+amountOfSamples*(i-1):amountOfSamples+amountOfSamples*(i-1),2) = y(:,i);
    points(1+amountOfSamples*(i-1):amountOfSamples+amountOfSamples*(i-1),3) = z(:,i);
end
tic 
 [MeshVerts,MeshEdges,MedialAxis,MAT,vert] = PowerCrust(points);
toc 
 % 

% x = RadiusRandom .*cos(elivation).*cos(azimuth);
% y = RadiusRandom .*cos(elivation).*sin(azimuth);
% z = RadiusRandom .*sin(elivation);
% figure;
% scatter3(x,y,z);
% points(1,:) =  
% points(2,:) =

% [x,y,z] = sph2cart(azimuth,elivation,RadiusRandom);




% % Define the radius of the shell of points, the surface of the sphere.
% % Define the number of points to place on the surface of the sphere.
% numPoints = amountOfSamples;	% Use a large value.
% 
% % Get a 3-by-numPoints list of (x, y, z) coordinates randomly.
% r = randn(3,numPoints); 
% 
% % At this point the points can be anywhere in 3D space,
% % not just on the surface of a sphere, a shell of constant radius.
% % Divide by the distance of each point from the origin.
% % This will place each point out at a definite radius of 1, not scattered throughout the volume.
% 
%  r = bsxfun(@rdivide, r, sqrt(sum(r.^2,1))); %%% function where the specified operationa that would be perfomed on the two matrices. 
% 
% % Now multiply by radius to make the shell out 
% % at a specified radius instead of a radius of exactly 1
% r =  RadiusRandom .* r; %%% Introduce noisy mesurment from the laser 
% r(3,1:numPoints) = abs(r(3,1:numPoints)); 
% 
% % Extract the x, y, and z coordinates from the array.
% x = r(1,:); % Extract x from row #1.
% y = r(2,:); % Extract y from row #2.
% z = r(3,:); % Extract z from row #3.
% 
% % Display the shell of point cloud
% scatter3(x, y, z);
% axis square; % Make sure the aspect ratio is maintained as it's displayed and rotated.
% xlabel('X-axis', 'FontSize', 20);
% ylabel('Y-axis', 'FontSize', 20);
% zlabel('Z-axis', 'FontSize', 20);
% title('The scatter plot of the randomized points','FontSize', 20);
% 
% set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]); % Enlarge figure to full screen.
% 
% points=zeros(amountOfSamples,3); %%% The matrix cotaining all points 
% 
% x=x';
% y=y';
% z=z';
% 
% points(1:amountOfSamples,1) = x(:,1);
% points(1:amountOfSamples,2) = y(:,1);
% points(1:amountOfSamples,3) = z(:,1);
% 
% tic 
% [MeshVerts,MeshEdges,MedialAxis,MAT,vert]=PowerCrust(points);
% % [MeshVerts,MeshEdges,MedialAxis,MAT,vert]=PowerCrust(pointsafter);
% disp('PowerCrust took: ')
% toc
end