%This file creates a 2D point cloud, and feeds it into PowerCrust.m
clc
clear 
close all 

points = [0,1;1,0;0,-1;-1,0; 1/2,-1/2; -1/2,-1/2; 1/2,1/2; -1/2,1/2];

% run Power Crust
PowerCrust(points,1);