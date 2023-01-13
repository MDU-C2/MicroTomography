function [fitresult, gof] = createFit_ty_circ(t, yy, show)

% Fit: 'parameter'.
[xData, yData] = prepareCurveData( t, yy );

% Set up fittype and options.
ft = fittype( 'smoothingspline' );
opts = fitoptions( 'Method', 'SmoothingSpline' );
opts.SmoothingParam = 0.000814476884136154;

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );

if show == true
    % Plot fit with data.
    figure( 'Name', 'parameter' );
    h = plot( fitresult, xData, yData );
    legend( h, 'yy vs. t', 'parameter', 'Location', 'NorthEast', 'Interpreter', 'none' );
    % Label axes
    xlabel( 't', 'Interpreter', 'none' );
    ylabel( 'yy', 'Interpreter', 'none' );
    grid on
end

