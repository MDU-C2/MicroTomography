function uniform_points = resampling(points,sample_step_size,boundary_height)

num_z_step = (boundary_height)/(sample_step_size); % number of steps 
zz =  linspace(-sample_step_size,-boundary_height, num_z_step);

ppoints = zeros(length(zz),3,size(points,3));
uniform_points = [];
%points= unique(points);
for i = 1:size(points,3)
    ppx(:,i) = spline (points(:,3,i),points(:,1,i));
    ppy(:,i) = spline (points(:,3,i),points(:,2,i));

    
    ppoints(:,1,i) = ppval(ppx(:,i),zz);
    ppoints(:,2,i) = ppval(ppy(:,i),zz);
    ppoints(:,3,i) = zz;
  
end
for i = 1:size(ppoints,1)
    initialparameter=[10 10 0];
    mx=@(initialparameter)error_function(initialparameter,squeeze(ppoints(i,1,:)),squeeze(ppoints(i,2,:)));
    [outputparameters, fval]=fminsearch(mx,initialparameter);

    radius_aprox = (outputparameters(1)+outputparameters(2))/2;
    perimeter = 2*pi* radius_aprox;
    num_angle_steps = round(perimeter/sample_step_size);
    t=linspace(0,2*pi,num_angle_steps);
    
    xao=outputparameters(1)*cos(t);
    yao=outputparameters(2)*sin(t);
    a=outputparameters(3);
    z=[cos(a) -sin(a);sin(a) cos(a)];
    m=[xao;yao];
    k=z*m;
    row = [k(1,:)', k(2,:)', repmat(ppoints(i,3,1), size(k(1,:)))'];
    uniform_points=[uniform_points; row ];

end



end

