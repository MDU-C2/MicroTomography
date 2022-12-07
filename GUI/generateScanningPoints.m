function pointList = generateScanningPoints(app, object, distanceThres, surfaceInterpolation)
% Generates *almost* evenly spaced points along the surface of
% the object. Spacing between points depends on variable
% distanceThres, which is the distance the points should have
% between each other and distanceThresTolerance which allows the
% distance to vary within set interval since in some cases
% evenly spaced points are impossible.

% Points are generated along the surface by stepping around the
% object in a cylindrical coordinate system, starting at
% theta = 0 until theta is 0 again. The algorithm works from
% the top of the object to the bottom, decrementing the Z value
% everytime a round around the object is completed. The
% projection onto the object surface (R value) is found through
% a interpolation algorithm. Distance between points are
% controlled by finding the closest point in the same row and
% the row above, and adjusting the point's position accordingly.


%Editable parameters to affect algorithm behavior:
%---------------------------
%distanceThres = 1; %The ideal distance between all points
distanceThresTolerance = 0.5; %How tolerant the distance should be: creates a interval from the distance threshold. Higher number = more accepted points
adjustmentLimit = 1000; %Limit on the maximum amount of adjustemnts done to a single point before the tolerance increased. Higher value = longer execution time, but higher chance of better positioning
stepSizeZ = 1; %Initial step taken in Z direction, should be a relativly low number. The program finds the exact stepsize for Z iterativly
originalStepSizeTheta = 0.01; %The difference in theta for every step
%---------------------------

zMax = max(object.Points(:,3)); %Highest Z of the object
zMin = min(object.Points(:,3)); %Lowest Z of the object
stepSizeTheta = originalStepSizeTheta; %original and stepSizeTheta are seperate because stepsize can vary throught the generation
distanceThresTolerance_c = distanceThresTolerance;
pointsCell = cell(10); %pointsCell holds all the points generated. Each column represents a round around the object in the same Z level
pointCellPol = cell(10);
j = 1; %iterator
pointList = [];
thetaLimit = double(3.1416); %As the algorithm works in cylindrical coordinates, the sign of theta changes at pi
sideSwitched = false; %Keeps track if the algorithm is currently working on the positive side or the negative side
nAdjustments = 0; %Keeps track of the number of adjustments done to a single point's position
zCurrent = zMax-5; %ZCurrent keeps track of the current Z level, algorithm starts at the top of the object

%Algorithm runs until the bottom of the object is reached.
% 1 iteration = 1 row done
while zCurrent >= zMin
    i = 1;
    thetaCurrent = -stepSizeTheta; %the first point should lay on theta = 0, because theta is always incremented by steSizeTheta, give negative so theta becomes 0
    lastPointInRowDone = false; %keeps track of the last point of a row is completed
    lastPointInRow = false; %keeps track if the last point in the row is being worked on
    hoppedSide = false;

    %Loops while placing and adjusting points in a row. Is
    %exited when all points on the row are placed.
    while true
        % the the number of adjustments for a single point
        % exceeds the limit, increase the distance tolerance
        % so that the point has higher chance to be accepted:
        if nAdjustments > adjustmentLimit
            distanceThresTolerance_c = distanceThresTolerance_c + 0.1;
            %                        if distanceThresTolerance_c > distanceThresTolerance * 5
            %                            break;
            %                        end
        end
        thetaCurrent = thetaCurrent + stepSizeTheta;

        %Checks if the row is done by seeing if we have
        %compleeted the last point in the row, theta has passed
        %the first point and we are comming from the negative
        %(theta) side of the object.
        if thetaCurrent >= 0 && sideSwitched || lastPointInRowDone
            sideSwitched = false; %resets the side indicator for the next row
            break %exit the loop to begin a new row
        end

        %if the new theta passes pi, change the theta value so
        %it can continue in the same direction:
        if round(thetaCurrent*1000) >= round(thetaLimit*1000) %if alogorithm goes from positive to negative theta side
            thetaCurrent = -3.1416 + (thetaCurrent-thetaLimit);
            sideSwitched = true;
        elseif round(thetaCurrent*1000) <= -round(thetaLimit*1000) %if algorithm goes from negative to positive theta side
            thetaCurrent = 3.1416 - (thetaCurrent+thetaLimit);
            sideSwitched = false;
        elseif thetaCurrent < 0 %if algorithm works on negative theta side
            sideSwitched = true;
        end
        newPoint = [thetaCurrent, surfaceInterpolation(thetaCurrent, zCurrent), zCurrent]; %create a new point in the current theta and z, r is decided by interpolation

        if newPoint(2) > 500 || any(isnan(newPoint)) || any(isinf(newPoint))
            continue
        end
        in = false;
        o_R = newPoint(2);
        while ~in
            [newPointCart(1), newPointCart(2), newPointCart(3)] = pol2cart(newPoint(1), newPoint(2), newPoint(3)); %Convert from cylindtrical coordinates to carteasian to measure distance
          
            in = inShape(object, newPointCart);
            if ~in
                newPoint(2) = newPoint(2) - 0.1;

            end
            if newPoint(2) < 0
                newPoint(2) = o_R;
                in = true;
            end

        end
        while in
            [newPointCart(1), newPointCart(2), newPointCart(3)] = pol2cart(newPoint(1), newPoint(2), newPoint(3)); %Convert from cylindtrical coordinates to carteasian to measure distance
            in = inShape(object, newPointCart);
            if in
                newPoint(2) = newPoint(2) + 0.1;
            end
        end

        [newPointCart(1), newPointCart(2), newPointCart(3)] = pol2cart(newPoint(1), newPoint(2), newPoint(3)); %Convert from cylindtrical coordinates to carteasian to measure distance

        pointsCell(i, j) = {[]}; %allocate space for current iteration (so that algorithm never works out of bounds)
        sameRowPoints = cell2mat(pointsCell(:, j)); %gets all points exsisting on the current row

        if ~isempty(sameRowPoints) %if there is points on the row (this point is not the first point on the row)
            [k,distance] = dsearchn(sameRowPoints, newPointCart); %search for the closest point in the same row and get the distance between the points
        end

        %if this point is the first point, or the point's
        %position is withing the accepted distance to the
        %closest point on the row:
        if isempty(sameRowPoints) || distance >= distanceThres - distanceThresTolerance_c && distance <= distanceThres + distanceThresTolerance_c
            % if this is not the first row, make an atempt to
            % adjust the Z value to achive an acceptable
            % distance between this point and the closest
            % point in the row above:
            if j > 1 || stepSizeTheta == 0
                aboveRowPoints = cell2mat(pointsCell(:, j-1)); %gets a list of points exsisting in the row above the current working row
                [~,dist] = dsearchn(aboveRowPoints, newPointCart); %searches for closest point to our current working point in the row above, gets the distance between them
                %if the distance between the points are under
                %the accepted minimum distance, and we have not
                %yet reached the bottom of the object: move down
                %on the object to increase the distance:
                if dist < distanceThres - distanceThresTolerance_c && zCurrent - 0.05 > zMin
                    zCurrent = zCurrent - 0.05; %move down a little on the object
                    stepSizeTheta = 0; %do not make any changes to the theta in the next iteration
                    nAdjustments = nAdjustments + 1;
                    continue %start the next iteration of the while loop (skip the rest of the code in the loop)
                elseif dist < distanceThres - distanceThresTolerance_c && zCurrent - 0.05 <= zMin &&  hoppedSide == false
                    %zCurrent = zCurrent - 0.05; %move down a little on the object
                    if thetaCurrent == 0
                        thetaCurrent = thetaLimit; %do not make any changes to the theta in the next iteration
                    else
                        thetaCurrent = -thetaCurrent; %do not make any changes to the theta in the next iteration
                    end
                    hoppedSide = true;
                    stepSizeTheta = 0; %do not make any changes to the theta in the next iteration
                    nAdjustments = nAdjustments + 1;
                    continue %start the next iteration of the while loop (skip the rest of the code in the loop)

                    %if the distance between the points are over the
                    %accepted maximum distance, and we have not
                    %passed the z hight of the row above; move up on
                    %the object to shorten the distance:
                elseif dist > distanceThres + distanceThresTolerance_c && zCurrent + 0.01 < mean(aboveRowPoints(:,3))
                    zCurrent = zCurrent + 0.01; %move up a little on the object (not same amount as when moving done, to catch areas inbetween)
                    stepSizeTheta = 0; %do not make any changes to theta in the next iteration
                    nAdjustments = nAdjustments + 1;
                    continue
                end
                %if these above statesments are false, the
                %point's distance to closest point above is
                %acceptable, and the algorithm can proceed to
                %save the point position.

                %Note: when a adjustment is done in the Z value,
                %this can affect the distance between points on
                %the same row, therefore the algorithm will next
                %adapt the distance between points on the same
                %row to be correct. This may result in the Z
                % value having to be adjusted again. This can
                % become a long iterative process, hence the
                % the adjustment limit is needed to increase
                % tolerance and cut computation time.

            end
            if i > 1 && j == 104
                inCell = any(cellfun(@(x) isequal(x, newPointCart), pointsCell(:, j)));
                %break
            end

            %Save the accepted point position
            pointsCell(i, j) = {newPointCart};
            pointCellPol(i,j) = {newPoint};
            i = i+1;
            %If you want to visually see the points on the
            %object (for debugging etc), uncomment this line:
            %plot3(app.UIAxes, newPointCart(1), newPointCart(2), newPointCart(3),'.','MarkerSize',10, 'Color','cyan');

            %reset the stepsize, nr of adjustments and the
            %distance tolerance for the next point:
            stepSizeTheta = originalStepSizeTheta;
            nAdjustments = 0;
            distanceThresTolerance_c = distanceThresTolerance;

            %If this was the last point on the row, mark it as
            %complete:
            if lastPointInRow
                lastPointInRowDone = true;
            end
        else
            %If the distance on the row was not accepted because
            % it's larger than maximum tolerated distance, decrease
            % theta in the next iteration (go back a bit):
            if distance > distanceThres + distanceThresTolerance_c
                stepSizeTheta = -0.005;

                %If the distance on the row was not accepted because the
                %point is too close to the first point in the row (we
                %have almost completed a round) mark it as the last
                %point and go back a little:
            elseif distance < distanceThres + distanceThresTolerance_c && sideSwitched && k == 1 && height(sameRowPoints) > 1
                lastPointInRow = true;
                stepSizeTheta = -0.005;
                %Else if the distance was to large between the points,
                %increase the theta in the next iteration:
            else
                stepSizeTheta = originalStepSizeTheta;
                if sideSwitched && k == 1
                    lastPointInRow = true;
                end
            end
            prevPoint = cell2mat(pointCellPol(i-1,j));
            prevPointTheta = prevPoint(1);
            prevPointZ = prevPoint(3);

            if thetaCurrent + stepSizeTheta <= prevPointTheta && thetaCurrent > 0 && prevPointTheta > 0 ||  thetaCurrent + stepSizeTheta <= prevPointTheta && thetaCurrent < 0 && prevPointTheta < 0%We do not want to go back over the previous points -> problem must exist in z instead
                stepSizeTheta = 0;
                if prevPointZ > newPoint(3) %If previous point is higher than the new point, minimize distance by moving new point up
                    zCurrent = zCurrent + 0.01;
                else %If previous point is lower than the new point, minimize distance by moving new point down
                    zCurrent = zCurrent - 0.01;
                end

            end
            nAdjustments = nAdjustments + 1;

        end

    end
    zCurrent = zCurrent - stepSizeZ; %row is done, go down a bit to begin the next row
    stepSizeTheta = originalStepSizeTheta; %reset the stepsize
    test = cell2mat(pointsCell(:, j));
    pointList = vertcat(pointList, cell2mat(pointsCell(:, j))); %Add the points in the completed row to the total list of points
    j = j+1;
end
%point generation is done




end