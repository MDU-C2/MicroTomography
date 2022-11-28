function [fitresult, gof] = createFit(y, z)
%% Fit: '2'.
[xData, yData] = prepareCurveData( y, z );

% Set up fittype and options.
ft = fittype( 'smoothingspline' );
opts = fitoptions( 'Method', 'SmoothingSpline' );
opts.Normalize = 'on';
opts.SmoothingParam = 0.994806586464716;

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );

% Plot fit with data.
figure( 'Name', '2' );
h = plot( fitresult, xData, yData );
legend( h, 'z vs. y', '2', 'Location', 'NorthEast', 'Interpreter', 'none' );
% Label axes
xlabel( 'y', 'Interpreter', 'none' );
ylabel( 'z', 'Interpreter', 'none' );
grid on


