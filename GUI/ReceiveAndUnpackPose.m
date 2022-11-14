function [pos, rot] = ReceiveAndUnpackPose(app, t)
%wait until message is received
noMsgReceived = 1;
while noMsgReceived
    receivedMsg = char(read(t));
    noMsgReceived = isempty(receivedMsg);
    %pause(0.5);
end
%Handle message string so that it becoms seperate rot och pos arrays
match = ["[","]"];
pose = split(receivedMsg, match);
pos = pose(2);
pos = split(pos,",");
pos = str2double(pos);

while noMsgReceived
    receivedMsg = char(read(t));
    noMsgReceived = isempty(receivedMsg);
    %pause(0.5);
end
match = ["[","]"];
pose = split(receivedMsg, match);
rot = pose(2);
rot = split(rot, ",");
rot = str2double(rot);

%eulerRad = quat2eul(rot');
%eulerDeg = rad2deg(eulerRad);
end