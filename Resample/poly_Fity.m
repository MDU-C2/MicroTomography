function [fitresult, gof] = poly_Fity(z, y, show)



%% Fit: 'fitzy'.
[xData, yData] = prepareCurveData( z, y );

% Set up fittype and options.
ft = fittype( 'poly3' );
opts = fitoptions( 'Method', 'LinearLeastSquares' );
opts.Normalize = 'on';
opts.Robust = 'LAR';

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );

if show == true
    % Plot fit with data.
    figure( 'Name', 'fitzy' );
    h = plot( fitresult, xData, yData );
    legend( h, 'y vs. z', 'fitzy', 'Location', 'NorthEast', 'Interpreter', 'none' );
    % Label axes
    xlabel( 'z', 'Interpreter', 'none' );
    ylabel( 'y', 'Interpreter', 'none' );
    grid on
end


