function TestRandPoints(ListofPoints,t)
    while true
        p1=round(rand()*(size(ListofPoints,1)-1))+1
        p2=round(rand()*(size(ListofPoints,3)-1))+1
        randPoint = ListofPoints(p1,:,p2)

        packAndSendPose(randPoint(1:3), randPoint(4:6), t); 
        position = ReceiveAndUnpackPose( t);

        pause(1)
    end
end