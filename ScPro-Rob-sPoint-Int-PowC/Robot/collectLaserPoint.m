%Sends one-and-one position from the protocoll to the robot, and gets back the position of the robot, and the value of the sensor. Saves it into "positionLaser"
 
function positionLaser = collectLaserPoint(Scanpoints,t)

    positionLaser = zeros( size(Scanpoints,1), size(Scanpoints,2)+1, size(Scanpoints,3));
    pathToLaserCommunicate = horzcat(pwd,'\MicroTomographyHT2022\ScPro-Rob-sPoint-Int-PowC\Robot\communicate.exe');
    [~, result] = system('ipconfig');
    for s =1:size(Scanpoints,3)
        NaNCounter=0;
        for r = 1:size(Scanpoints,1)
            if NaNCounter<3 %counts how many time the Laser dont get a value. To many times in a row = No object = Start new row of scanning 
                packAndSendPose(Scanpoints(r,1:3,s), Scanpoints(r,4:6,s),1,0,0, t); 
                position = ReceiveAndUnpackPose(t);
            
                for i = 1:2
                    [status, laser] = system(horzcat(pathToLaserCommunicate, ' 10.132.158.191 1884 10.132.158.190 1000'));
                    disp(laser);
    
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
        

