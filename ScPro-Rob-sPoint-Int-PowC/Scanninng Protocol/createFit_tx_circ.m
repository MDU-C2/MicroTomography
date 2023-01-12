function [fitresult, gof] = createFit_tx_circ(t, xx, show)


%% Fit: 'parameter'.
[xData, yData] = prepareCurveData( t, xx );

% Set up fittype and options.
ft = fittype( 'smoothingspline' );
opts = fitoptions( 'Method', 'SmoothingSpline' );
opts.SmoothingParam = 0.00134213622089488;

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );
if show == true
    % Plot fit with data.
    figure( 'Name', 'parameter' );
    h = plot( fitresult, xData, yData );
    legend( h, 'xx vs. t', 'parameter', 'Location', 'NorthEast', 'Interpreter', 'none' );
    % Label axes
    xlabel( 't', 'Interpreter', 'none' );
    ylabel( 'xx', 'Interpreter', 'none' );
    grid on
end


