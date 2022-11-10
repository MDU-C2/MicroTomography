
function positionLaser = collectLaserPoint(Scanpoints,t)

    positionLaser = zeros( size(Scanpoints,1), size(Scanpoints,2)+1, size(Scanpoints,3));

    for s = 1:size(Scanpoints,3)
        for r = 1:size(Scanpoints,1)
            packAndSendPose(Scanpoints(r,1:3,s), Scanpoints(r,4:6,s),1,0,0, t); 
            position = ReceiveAndUnpackPose(t);

            laser=20; %%READ FROM LASER

            positionLaser(r,:,s) = [position laser];
        end
    end
end
        

