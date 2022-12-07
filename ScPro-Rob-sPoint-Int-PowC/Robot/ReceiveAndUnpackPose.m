function position = ReceiveAndUnpackPose(t)
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
    
    disp ("From Robot: ");
    disp(position);
end