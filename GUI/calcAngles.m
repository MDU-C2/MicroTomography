function [angle_H, angle_P, angle_B, dirArrow] = calcAngles(app, wantedTCPplotPos, centerPoints, normals, dirArrow)
%get the current position
pos = [wantedTCPplotPos.XData, wantedTCPplotPos.YData, wantedTCPplotPos.ZData];
center = centerPoints;
%search for closest triangle center point (gives index of point)
[k,dist] = dsearchn(center,pos);
%plot normal, origin from tcp point
if isempty(dirArrow) %if not plotted before, plot, otherwise update coordinates
    dirArrow = quiver3(wantedTCPplotPos.XData, wantedTCPplotPos.YData, wantedTCPplotPos.ZData, normals(k,1), normals(k,2), normals(k,3), 'Parent', app.UIAxes, 'AutoScale','on', 'AutoScaleFactor',15, 'LineWidth',1.5, 'MaxHeadSize',20);
else
    dirArrow.XData = wantedTCPplotPos.XData;
    dirArrow.YData = wantedTCPplotPos.YData;
    dirArrow.ZData = wantedTCPplotPos.ZData;

    dirArrow.UData = normals(k,1);
    dirArrow.VData = normals(k,2);
    dirArrow.WData = normals(k,3);
end
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