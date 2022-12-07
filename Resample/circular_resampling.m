function points = circular_resampling(spline_resample,step_size_t)
%% Circular interpolation 
% New t array to sample the circles 
t=0:step_size_t:2*pi;
% Create points array
points = [];
% For every height
for j = 1: size(spline_resample,1)
    xx = squeeze(spline_resample(j,1,:));
    yy = squeeze(spline_resample(j,2,:));
    % Search for solution 
    initialparameter=[10 10 0 0 0];
    mx=@(initialparameter)error_function(initialparameter,xx,yy);
    [outputparameters, ~]=fminsearch(mx,initialparameter);

    xao=outputparameters(4)+outputparameters(1)*cos(t);
    yao=outputparameters(5)+outputparameters(2)*sin(t);
    a=outputparameters(3);
    z=[cos(a) -sin(a);sin(a) cos(a)];
    m=[xao;yao];
    k=z*m;
    xao=k(1,:);
    yao=k(2,:);
    points = [points; xao' yao' repmat(spline_resample(j,3,1),size(xao))'];
end
end

