clear
N=4000;
r = 6;
center = [2,1,3];
P = zeros(N,3) ;

x1 = 0.01;
x2 = 0.02;
for i=1:N
    x1 = rand;
    x2 = rand;
    Px = sqrt(x1*(2-x1))* cos(2*pi*x2);
    Py = sqrt(x1*(2-x1))* sin(2*pi*x2);
    Pz = 1-x1;
    Px = Px * r + center(1);
    Py = Py * r + center(2);
    Pz = Pz * r + center(3);

    Po(i,:) = [Px, Py, Pz];
end

p = pcread('teapot.ply');
P = double(squeeze(p.Location));
k = boundary(P, 1);


% Create a figure window
fig = uifigure;
fig.WindowState = "maximized";

% Create a UI axes
ax = uiaxes(fig);
ax.XGrid = "on";
ax.YGrid = "on";
ax.ZGrid = "on";
hold(ax, 'on')
view(ax,[-5 2 5])
tes = scatter3(ax, P(:,1),P(:,2),P(:,3), '.');
k = trisurf(k,P(:,1),P(:,2),P(:,3), 'LineStyle', '-', 'FaceAlpha',0.5 ,'Parent', ax);
xlabel('x', 'Parent',ax);
ylabel('y', 'Parent',ax);
zlabel('z', 'Parent',ax);
x = [-1.291 0.6817 2.02534];
y = [-2.531 -1.92441 -3.61522];
z = [6.5632 8.0705 6.83394];
%plot3(ax, x,y,z,'-','MarkerSize',20);
d = datacursormode(fig);
%set(d, 'Marker','o', 'MarkerFaceColor','b');
set(d,'Enable','on', 'UpdateFcn', {@alert, d, ax})
%drawcuboid(tes);

%dT = dataTipInteraction('SnapToDataVertex', 'off');
%ax.Interactions = [dataTipInteraction rotateInteraction];


% Create a push button
btn = uibutton(fig,'push', 'Text','Confirm measurment points', ...
    'Position',[420, 218, 200, 30],...
    'ButtonPushedFcn', @(btn,event) confirmPoints(btn,d, ax));


% Create the function for the ButtonPushedFcn callback
function confirmPoints(btn,d, ax)
selectedPoints = getCursorInfo(d)

end

function resetPoints(btn, ax)
cla(ax);
trisurf(k,P(:,1),P(:,2),P(:,3), 'LineStyle', 'none', 'FaceAlpha',0.5 ,'Parent', ax);
end

function txt = alert(obj, event_obj, d, ax)
%set(event_obj.Target, 'Marker','o', 'MarkerFaceColor','b');
global savedX
tes = savedX;
%delete(tes);
pos = get(event_obj, 'Position');
disp('alerted');
selectedPoints = getCursorInfo(d);
allPointCoord = zeros(1,3);
for i=1:numel(selectedPoints)
    allPointCoord(i, :) = selectedPoints(i).Position;
    %tes(i) = plot3(ax, selectedPoints(i).Position(1) ...
     %   ,selectedPoints(i).Position(2),selectedPoints(i).Position(3), ...
    %    'o','Color','r','MarkerSize',10,...
    %'MarkerFaceColor','r');
    %selectedPoints(i).Position
   % disp(i);
end
tes = plot3(ax, allPointCoord(:,1), allPointCoord(:,2), allPointCoord(:,3), ...
        '-o','Color','r','MarkerSize',10,...
    'MarkerFaceColor','r');
savedX = tes;


%tes = scatter3(ax, selectedPoints.Position() ,P(:,2),P(:,3), '.');
%set(selectedPoints.Target, 'Marker','o', 'MarkerFaceColor','b');
txt = '';
end