function  show_HT(fig ,axis, HT,scale)
    % Function to show Base vectors to the Homogenous transformation in the
    % axis specified. 

    % Input:
    % Axis: Axis where to show the base vectots
    % HT : Homogenious transformation matrix 
    

    new_x = HT.transform([1,0,0]);
    new_y = HT.transform([0,1,0]);
    new_z = HT.transform([0,0,1]);
    translation_vec = HT.trvec;

    new_z = HT.trvec - new_z;
    new_x = HT.trvec - new_x;
    new_y = HT.trvec - new_y;

    new_z = new_z/ sqrt(norm(new_z));
    new_x = new_x/ sqrt(norm(new_x));
    new_y = new_y/ sqrt(norm(new_y));
    
    figure(fig)
    quiver3(axis, translation_vec(1),translation_vec(2),translation_vec(3),...
        new_z(1),new_z(2),new_z(3),scale, "LineWidth",3, 'Color','blue')
    quiver3(axis, translation_vec(1),translation_vec(2),translation_vec(3),...
        new_x(1),new_x(2),new_x(3),scale, "LineWidth",3, 'Color','red')
    quiver3(axis, translation_vec(1),translation_vec(2),translation_vec(3),...
        new_y(1),new_y(2),new_y(3),scale, "LineWidth",3, 'Color','green')

    quiver3(axis, 0,0,0,...
        0,0,1,scale, "LineWidth",3, 'Color','blue')
    quiver3(axis, 0,0,0,...
        1,0,0,scale, "LineWidth",3, 'Color','red')
    quiver3(axis, 0,0,0,...
        0,1,0,scale, "LineWidth",3, 'Color','green')

end

