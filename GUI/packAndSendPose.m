function packAndSendPose(app, pos, eulerDeg,tool,speed,extra, t)
    %put together msg string
    eulerDeg(2) = eulerDeg(2) + 00;
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
    writeToLog(app, "GUI sent: " + pos);
end