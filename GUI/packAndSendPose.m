function packAndSendPose(app, pos, eulerDeg, t)
%eulerRad = deg2rad(eulerDeg);
%eulerDeg = [0,0,0];

%rot = eul2quat(eulerRad)';

%put together msg string
sPos = string(pos);
sRot = string(eulerDeg);


%add formatting to pos string
sPos = join(sPos,",");
sPos = strcat("[",sPos,"]");

%add formatting to rot string
sRot = join(sRot,",");
sRot = strcat("[",sRot,"]");
write(t,sPos);
write(t, sRot);

%put pos and rot together
%sendMsg = strcat(sPos,",",sRot);
%sendMsg = strcat("[",sendMsg,"]");

%send msg string
%write(t,sendMsg)
end
