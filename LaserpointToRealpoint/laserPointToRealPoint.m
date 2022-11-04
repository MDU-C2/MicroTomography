% clc
% clear
% close all;
% 
% 

classdef laserPointToRealPoint
   methods
       function surfacePoints = calcSurfacePoint(obj, LaserPoints)
           surfacePoints=zeros( size(LaserPoints,1), 3, size(LaserPoints,3));
           for s = 2:size(LaserPoints,3)
                for r = 1:size(LaserPoints,1)
                    %Take next elements in array TRANS ROT
                    surfacePoint = findSurfacePosition(obj, LaserPoints(r,1:3,s), LaserPoints(r,4:6,s), LaserPoints(r,7,s));
                    surfacePoints(r,:,s) = surfacePoint;
                end
           end
       end

%        function position = GetSurfacepoint(obj,p)
%             scatter3(pos(1),pos(2),pos(3),'filled');
%             hold on;
%             laserlength=20;
%             position = findSurfacePosition(obj, rot,pos,laserlength);
%             scatter3(position(1),position(2),position(3));
%             pause(.1);
%             hold on;
%         end
        
        
        function position = findSurfacePosition(obj,posRobot,rot,laserlength)
            d=[0,0,0];
            laserlength=[0;0;laserlength;1];
        
            T1=createTransformationMatrix(obj, rotx(rot(3)),posRobot);
            T2=createTransformationMatrix(obj, roty(rot(2)),d);
            T3=createTransformationMatrix(obj, rotx(rot(1)),d);
            T = T1*T2*T3;
        
            position = T*laserlength;
            position=position(1:3)';
        
        end
        
        function T=createTransformationMatrix(~,R,D)
            D=D';
        
            T = [R D];
            T = [T ; [0,0,0,1]];
        end
        
        


   end
end