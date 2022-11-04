classdef collectLaserPoint
    methods
        function positionLaser = collect(obj, Scanpoints,t)

            positionLaser = zeros( size(Scanpoints,1), size(Scanpoints,2)+1, size(Scanpoints,3));

            for s = 1:size(Scanpoints,3)
                for r = 1:size(Scanpoints,1)
                    packAndSendPose(obj, 0, Scanpoints(r,1:3,s), Scanpoints(r,4:6,s), t); 
                    position = ReceiveAndUnpackPose(obj, 0, t);

                    laser=20; %%READ FROM LASER

                    positionLaser(r,:,s) = [position laser];
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

        function position = ReceiveAndUnpackPose(obj, ~, t)
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

            position=[trans rot];
        end
   end
end


