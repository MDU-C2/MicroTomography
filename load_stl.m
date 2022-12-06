function [geo,stl_points]  = load_stl(file_name)

    geo = stlread (file_name);
    new_points = rotx(90)*geo.Points';
    stl_points = new_points';
    % center
    stl_points(:,3) = stl_points(:,3) -120;
    stl_points(:,2) = stl_points(:,2) +60;
    stl_points(:,1) = stl_points(:,1) -60;

end

