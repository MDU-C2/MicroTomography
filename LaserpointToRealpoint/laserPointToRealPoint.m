% clc
% clear
% close all;
% 
% 

classdef laserPointToRealPoint
   methods
       function position = GetSurfacepoint(obj, t,transIn,rotIn)
            packAndSendPose(obj, 0, transIn, rotIn, t);
        
            [pos, rot] = ReceiveAndUnpackPose(obj, 0, t);
        
            scatter3(pos(1),pos(2),pos(3),'filled');
            hold on;
            laserlength=20;
            position = findSurfacePosition(obj, rot,pos,laserlength);
            scatter3(position(1),position(2),position(3));
            pause(.1);
            hold on;
        end
        
        
        function position = findSurfacePosition(obj, rot,posRobot,laserlength)
            d=[0,0,0];
            laserlength=[0;0;laserlength;1];
        
            T1=createTransformationMatrix(obj, rotx(rot(3)),posRobot);
            T2=createTransformationMatrix(obj, roty(rot(2)),d);
            T3=createTransformationMatrix(obj, rotx(rot(1)),d);
            T = T1*T2*T3;
        
            position = T*laserlength;
            position=position(1:3);
        
        end
        
        function T=createTransformationMatrix(obj,R,D)
            D=D';
        
            T = [R D];
            T = [T ; [0,0,0,1]];
        end
        
        function [trans, rot] = ReceiveAndUnpackPose(obj, ~, t)
        
            noMsgReceived = 1;
            while noMsgReceived
                receivedMsg = char(read(t));
                noMsgReceived = isempty(receivedMsg);
            end
            
            msg=strrep(receivedMsg,',',' ');
            msg=strrep(msg,'][',' ');
            msg=msg(2:end-1);
        
            pos = str2num(msg);
        
            trans = pos(1:3);
            rot = pos(4:end);
        end
        
        function packAndSendPose(obj, ~, pos, eulerDeg, t)
            %put together msg string
            sPos = string(pos);
            sRot = string(eulerDeg);
            
            
            %add formatting to pos string
            sPos = join(sPos,",");
            sPos = strcat("[",sPos,"]");
            
            %add formatting to rot string
            sRot = join(sRot,",");
            sRot = strcat("[",sRot,"]");
        
            pos = strcat ("[",sPos,",",sRot,"]");
            write(t,pos);
        end

   end
end