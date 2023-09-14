clear all
close all
clc

load data\surfacePoint11221608_RemoveLightAbove.mat;
data = surfacePoints;

%% Run for resampling

show_fit = false;
show_scatter = false;
delta_z = 1;
step_size_t = 1;
points = resample_data(data, delta_z, step_size_t,show_scatter,show_fit);

%% PLOt results
%points = data;
g = importGeometry("data\symmetricalBreastModel.stl");
stlData = stlread('data\symmetricalBreastModel.STL');

stlPoint = stlData.Points; %%% get the points from the stl file
maxPoint = max(stlPoint(:,2)); %%Center the stl data to 0,0,0
stlPoint(:,2) = stlPoint(:,2) - maxPoint;
[min1,idx1] = min(stlPoint(:,2));
stlPoint(:,[1,3]) = stlPoint(:,[1,3]) - stlPoint(idx1,[1,3]);

%maxPoint1 = max(points(:,3)); %%Center the resampled data to 0,0,0 Doesnt
%really work.
%points(:,3) = points(:,3) - maxPoint1;
%[min2,idx2] = min(points(:,3));
%points(:,[1,2]) = points(:,[1,2]) - points(idx2,[1,2]);

figure;hold on;
for i = 1:size(data,3)
    scatter3(data(:,1,i),data(:,2,i),data(:,3,i),'filled', 'black')
end
scatter3(stlPoint(:,1),stlPoint(:,3),stlPoint(:,2),'filled', 'blue')
scatter3(points(:,1),points(:,2),points(:,3),'filled', 'red')
xlabel('X')
ylabel('Y')
zlabel('Z')
legend('Sampled Data','STL data', 'Resampled Data')
%% Weird way to reconstruct the surface
sizeDeg = size(-pi:deg2rad(delta_z):pi,2);
maxI = length(points)/sizeDeg;
j = 1;
for i = 1:maxI
    X(i,:) = points(((i-1)*sizeDeg)+1:i*sizeDeg,1);
    Y(i,:) = points(((i-1)*sizeDeg)+1:i*sizeDeg,2);
    Z(i,:) = points(((i-1)*sizeDeg)+1:i*sizeDeg,3);

end

testSurf = surfc(X,Y,Z);

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

%ColorArray = randi([1 10],size(pp,1),1,'double');

colorMap = zeros(size(pp,1),1);
colorMap(2:end) = colorMap(2:end) -1;

%patch('Faces',con(ix,:),'Vertices',pp,'FaceVertexCData',ColorArray,'FaceColor','interp','EdgeColor','none')
model = createpde();
geometryFromMesh(model,pp',con(ix,:)');

%%Create model from STL data
tic;
DT = delaunayTriangulation(stlPoint(:,1),stlPoint(:,3),stlPoint(:,2));  % create tetrahedrons
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

model1 = createpde();
geometryFromMesh(model1,pp',con(ix,:)');
figure(2)
pdegplot(model1,"FaceLabels","on","FaceAlpha",0.5);
hold on;
pdeplot3D(model,'ColorMapData',colorMap)
