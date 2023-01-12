function [fitresult, gof] = createFity(z, y, show)

%% Fit: 'fitzy'.
[xData, yData] = prepareCurveData( z, y );

% Set up fittype and options.
ft = fittype( 'smoothingspline' );
opts = fitoptions( 'Method', 'SmoothingSpline' );
opts.SmoothingParam = 0.012576973161283;

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );

if show== true
    % Plot fit with data.
    figure( 'Name', 'fitzy' );
    h = plot( fitresult, xData, yData );
    legend( h, 'y vs. z', 'fitzy', 'Location', 'NorthEast', 'Interpreter', 'none' );
    % Label axes
    xlabel( 'z', 'Interpreter', 'none' );
    ylabel( 'y', 'Interpreter', 'none' );
    grid on
end


