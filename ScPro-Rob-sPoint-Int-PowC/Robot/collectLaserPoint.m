 
function positionLaser = collectLaserPoint(Scanpoints,t)

    positionLaser = zeros( size(Scanpoints,1), size(Scanpoints,2)+1, size(Scanpoints,3));

    for s = 1:size(Scanpoints,3)
        NaNCounter=0;
        for r = 1:size(Scanpoints,1)
            if NaNCounter<3
                packAndSendPose(Scanpoints(r,1:3,s), Scanpoints(r,4:6,s),1,0,0, t); 
                position = ReceiveAndUnpackPose(t);
% 
%             laser=20; %%READ FROM LASER
%             read = 0;

            
                for i = 1:3
                    [status, laser] = system('communicate.exe 10.132.158.95 1884 10.132.158.190 1000');
                    %Check laser. if laser inte är nummer: status=1;
                    %laser=20;
    
                    read = any(isletter(laser));
                    if ~ read
                        break;
                    end
                end
                
                if ~ read
                    positionLaser(r,:,s) = [position str2double(laser)];
                    NaNCounter=0;
                else 
                    positionLaser(r,:,s) = [NaN,NaN,NaN,NaN,NaN,NaN,NaN];
                    NaNCounter=NaNCounter+1;
                end
            else
                positionLaser(r,:,s) = [NaN,NaN,NaN,NaN,NaN,NaN,NaN];
            end

        end
    end
end
        

