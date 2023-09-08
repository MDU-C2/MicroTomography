clear all 
close all
clc

load surfacePoint11221608_RemoveLightAbove.mat;
new_code = surfacePoints;
data = new_code; 
%% FUnction for all above 

show_fit = false;
show_scatter = false;
delta_z = 1;
step_size_t = 1;
points = resample_data(data, delta_z, step_size_t,show_scatter,show_fit);

%% PLOt results
%points = data;
figure;hold on;
for i = 1:size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled', 'black')
end
scatter3(points(:,1),points(:,2),points(:,3),'filled', 'red')
xlabel('X')
ylabel('Y')
zlabel('Z')
legend('Sampled Data', 'Resampled Data')
%% Tight Cocone
tic;
DT = delaunayTriangulation(points(:,1),points(:,2),points(:,3));  % create tetrahedrons
con = DT.ConnectivityList;
pp = DT.Points;
xx = pp(:,1);
yy = pp(:,2);
zz = pp(:,3);
x = xx(con);
y = yy(con);
z = zz(con);
ix = true(size(con,1),1);

mlength = 200;                       % minimum side length
for i = 1:3
    for j = i+1:4
        A = [x(:,i)-x(:,j) y(:,i)-y(:,j) z(:,i)-z(:,j)]; % length of side
        D = sqrt(sum(A.^2,2)) < mlength;                 % is length small?
        ix = ix & D;                                     % if big write '0'
    end
end
toc;


patch('Faces',con(ix,:),'Vertices',pp,'FaceColor','Blue','EdgeColor','Blue')