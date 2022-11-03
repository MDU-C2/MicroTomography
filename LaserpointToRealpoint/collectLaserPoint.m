classdef collectLaserPoint
    methods
        function [laser,pos,rot] = collect(obj, Scanpoints)
            laser=[];
            pos=[];
            rot=[];
            spline = size(Scanpoints,3);
            Rows = size(Scanpoints,1);

            for s = 1:spline
                for r = 1:Rows
                    packAndSendPose(obj, 0, A(r,1:3,spline), A(r,4:6,spline), t); 
                    [pos(end+1), rot(end+1)] = ReceiveAndUnpackPose(obj, 0, t);

                    laser(end+1)=20; %%READ FROM LASER:
                end
            end
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
   end
end


