function packAndSendPose(pos, eulerDeg,tool,speed,extra, t)
    %put together msg string
    sPos = string(pos);
    sRot = string(eulerDeg);
   
    %add formatting to pos string
    sPos = join(sPos,",");
    sPos = strcat("[",sPos,"]");
    
    %add formatting to rot string
    sRot = join(sRot,",");
    sRot = strcat("[",sRot,"]");

    %%% 1: Laser   0: reciever
    sTool = string(tool);
    sSpeed = string(speed);
    sExtra = string(extra);
    sSpec = strcat("[",sTool,",",sSpeed,",",sExtra,"]");
    
    pos = strcat ("[",sPos,",",sRot,",",sSpec,"]");
    write(t,pos);
    disp ("To Robot: ");
    disp(pos);
end