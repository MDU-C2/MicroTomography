function [angle_H, angle_P, angle_B, k] = calcAngles(app, pos, centerPoints, normals)
%get the current position
%pos = [pos.XData, pos.YData, pos.ZData];
center = centerPoints;
%search for closest triangle center point (gives index of point)
[k,dist] = dsearchn(center,pos);

%get the corresponding normal (use index given from the nearest
%point search)
sNormal = normals(k,:);
U = [0,0,1]; %up vector
angle_H = rad2deg(atan2(sNormal(2), sNormal(1))); %calculate heading angle
angle_P = rad2deg(asin(sNormal(3))); %calculate pitch angle

W0 = [-sNormal(2), sNormal(1), 0 ];
U0 = cross(W0, sNormal);
angle_B = rad2deg(atan2( dot(W0,U) / norm(W0), dot(U0,U) / norm(U0) )); %calculate bank angle
if ismissing(angle_B)
    angle_B = 0;
elseif ismissing(angle_H)
    angle_H = 0;
elseif ismissing(angle_P)
    angle_P = 0;
end

end