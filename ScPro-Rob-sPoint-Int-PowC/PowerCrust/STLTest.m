%%%% A function just to try the poweCrust algorithm with points from
%%%% the symetrical or asymetric brest model.   
clc
clear
close all hidden
figure
g = importGeometry("asymmetricalBreastModel.stl");
stlData = stlread('asymmetricalBreastModel.STL');

points = stlData.Points; %%% get the points from the stl file 
rotate(g,90,[0 0 0],[1 0 0])
pdegplot(g) %%% Just to plot the stl file 
figure (2)
%%%% The stl file containes alot of point so this removes every second.
% points(2:2:end,:) = []; 
% points(4:4:end,:) = [];
tic 
[~,Mesh,~,~,~] = PowerCrust(points,1); 
toc