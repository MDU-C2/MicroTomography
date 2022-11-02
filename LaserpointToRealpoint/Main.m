RobotCon = ConnectRobot;
calcSurfacePoint = laserPointToRealPoint;

%%% TEST
o=[-100,0,0];
h1=[0,-100,0];
h2=[100,0,0];
v1=[0,100,0];
v2=[100,0,0];


ro=[0,0,0];
rh1=[0,90,0];
rh2=[0,180,0];
rv1=[0,-90,0];
rv2=[0,-180,0];

s=[o;h1;h2;h1;o;v1;v2;v1;o];
r=[ro;rh1;rh2;rh1;ro;rv1;rv2;rv1;ro];
i=1;
%%% END

t = RobotCon.connect();

while true %While length of scanning points
    %%% TEST
    if i>length(s)
        i=1;
    end
    trans=s(i,:);
    rot=r(i,:);
    %%% END

    surfacePoint = calcSurfacePoint.GetSurfacepoint(t, trans, rot);

    %%% TEST
    i=i+1;
    %%% END
end

