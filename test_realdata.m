clc 
clear all 
close all 

load surfacePoint11161212.mat ;


%% Clean files from nan Run once to get files in current folder 
% for i = 1:size(surfacePoint,3)
%     FileName=[num2str(i),'points.csv'];
%     %csvwrite(FileName,surfacePoint(:,:,i))
%     data = readtable(FileName);
%     data = table2array(data);
%     B = isnan(data);
%     data(B(:,1),:)= [];
%     csvwrite(FileName,surfacePoint(:,:,i))  
% end
%%
boundary_height = 100;
z_step_size = 0.5;
num_z_step = (boundary_height)/(z_step_size); % number of steps
zz =  linspace(-z_step_size,-boundary_height, num_z_step);

ppoints = zeros(length(zz),3,21);

figure;hold on;
for i = 1:size(surfacePoint,3)
    FileName=[num2str(i),'points.csv'];
    %csvwrite(FileName,surfacePoint(:,:,i))
    data = readtable(FileName);
    data = table2array(data);
    B = isnan(data);
    data(B(:,1),:)= [];
    scatter3(data(:,1),data(:,2),data(:,3))
    ppx = spline (data(:,3),data(:,1));
    ppy= spline (data(:,3),data(:,2));

    ppoints(:,1,i) = ppval(ppx,zz);
    ppoints(:,2,i) = ppval(ppy,zz);
    ppoints(:,3,i) = zz;

end



%%
    figure;hold on;
for i = 1:size(ppoints,3)
    
    scatter3(ppoints(:,1,i),ppoints(:,2,i),ppoints(:,3,i))
    
end

%%
figure;hold on;
for i = 1:size(surfacePoint,3)
    scatter3(points(:,1,i),points(:,2,i),points(:,3,i))
    view(3)
    drawnow
end


