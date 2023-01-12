function [fitresult, gof] = createFitx(z, x, show)

%% Fit: 'fitzx'.
[xData, yData] = prepareCurveData( z, x );

% Set up fittype and options.
ft = fittype( 'smoothingspline' );
opts = fitoptions( 'Method', 'SmoothingSpline' );
opts.SmoothingParam = 0.0334645621620676;

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );

if show == true
    % Plot fit with data.
    figure( 'Name', 'fitzx' );
    h = plot( fitresult, xData, yData );
    legend( h, 'x vs. z', 'fitzx', 'Location', 'NorthEast', 'Interpreter', 'none' );
    % Label axes
    xlabel( 'z', 'Interpreter', 'none' );
    ylabel( 'x', 'Interpreter', 'none' );
    grid on
end


