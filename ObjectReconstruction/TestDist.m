clear all 
close all
clc

load data\surfacePoint11221608_RemoveLightAbove.mat;
data = surfacePoints;

for i = 1:size(data,3)
    dataNew{:,:,i} = rmmissing(data(:,:,i));
end
C = size(data,1);

for i = 1:size(dataNew,3)
    B = size(dataNew{i});
    if B(1) < C
        C = B(1);
    end
end

for i = 1:size(dataNew,3)

    dataNew2(:,:,i) = dataNew{:,:,i}(1:C,:,:);

end

data = dataNew2;


dataSet = data(:,1,1);
dist = 0;
for i = 1:length(data)-1
    
    dist = dist + sqrt(data(i)^2 + data(i+1)^2);

end
dist = dist/length(data);

p = 1/(1+dist^3/6);