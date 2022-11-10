function packAndSendPose(pos, eulerDeg, t)
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