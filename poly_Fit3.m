function [fitresult, gof] = poly_Fit3(z, x)

%% Fit: 'fitzy'.
[xData, yData] = prepareCurveData( z, x );

% Set up fittype and options.
ft = fittype( 'poly3' );
opts = fitoptions( 'Method', 'LinearLeastSquares' );
opts.Normalize = 'on';
opts.Robust = 'LAR';

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );

% Plot fit with data.
figure( 'Name', 'fitzy' );
h = plot( fitresult, xData, yData );
legend( h, 'x vs. z', 'fitzy', 'Location', 'NorthEast', 'Interpreter', 'none' );
% Label axes
xlabel( 'z', 'Interpreter', 'none' );
ylabel( 'x', 'Interpreter', 'none' );
grid on


