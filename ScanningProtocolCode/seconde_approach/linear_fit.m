function [fitresult, gof] = linear_fit(z, y, show)

%% Fit: 'untitled fit 1'.
[xData, yData] = prepareCurveData( z, y );

% Set up fittype and options.
ft = fittype( 'poly1' );

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft );
if show == true
    % Plot fit with data.
    figure( 'Name', 'untitled fit 1' );
    h = plot( fitresult, xData, yData );
    legend( h, 'y vs. z', 'untitled fit 1', 'Location', 'NorthEast', 'Interpreter', 'none' );
    % Label axes
    xlabel( 'z', 'Interpreter', 'none' );
    ylabel( 'y', 'Interpreter', 'none' );
    grid on
end

