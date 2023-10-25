function [] = MoveSmallRobotUp()
%CONNECTTOSMALLROBOT Summary of this function goes here
%   Detailed explanation goes here
uR = udpport("LocalHost", "10.132.158.191", "LocalPort", 1885);
uS = udpport("IPV4");
%195 highest, moveDown:3200 = steg ner, moveUp:3200 = steg up
write(uS,"moveUp:3200","string","10.132.158.192",1001);
data = read(uR,12, "string");
end

