function results = testIfStepAllowed(app, newCoord, waitingOnPos, shape)
%tests to see if requested step in manual control is allowed by
%seeing if the robot is currently moving, adding the set minimum
%distance to movement on a vector pointing towards the center of
%the object.
if waitingOnPos
    results = 0;
    writeToLog(app, 'Movement denied: Robot is still moving, please wait...')
    return

end

angleFromX = atan2(sqrt(newCoord(2)^2+newCoord(3)^2),newCoord(1));
angleFromY = atan2(sqrt(newCoord(3)^2+newCoord(1)^2),newCoord(2));
angleFromZ = atan2(sqrt(newCoord(1)^2+newCoord(2)^2),newCoord(3));

%Get length of vector from origo
lenFromOrigo = sqrt(newCoord(1)^2+newCoord(2)^2+newCoord(3)^2);

%Calculate new vector based on angles and new length

newLength = lenFromOrigo - app.MinimumdistancetoobjectSpinner.Value;

%if angleFromX <= ... then sin else cos
newShorterVector(1) = newLength * cos(angleFromX);
newShorterVector(2) = newLength * cos(angleFromY);
newShorterVector(3) = newLength * cos(angleFromZ);

newShorterVectorNoZ(1) = newShorterVector(1);
newShorterVectorNoZ(2) = newShorterVector(2);
newShorterVectorNoZ(3) = newCoord(3);

%app.testingCoord = plot3(app.UIAxes, newShorterVector(1), newShorterVector(2), newShorterVector(3),'.','MarkerSize',10, 'Color','cyan');



in = inShape(shape, newShorterVector) | inShape(shape, newShorterVectorNoZ);
results = ~in;
if in
    writeToLog(app, 'Movement denied: New coordinate would be in object or within minimum distance set to object.');
end

end