function [fitresult, gof] = fourie_rtheta(Theta, R, show)

%% Fit: 'untitled fit 1'.
[xData, yData] = prepareCurveData( Theta, R );

% Set up fittype and options.
ft = fittype( 'fourier2' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.Normalize = 'on';
opts.Robust = 'Bisquare';
opts.StartPoint = [0 0 0 0 0 1.92427646224661];

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );

if show == true
    % Plot fit with data.
    figure( 'Name', 'untitled fit 1' );
    h = plot( fitresult, xData, yData );
    legend( h, 'R vs. Theta', 'untitled fit 1', 'Location', 'NorthEast', 'Interpreter', 'none' );
    % Label axes
    xlabel( 'Theta', 'Interpreter', 'none' );
    ylabel( 'R', 'Interpreter', 'none' );
    grid on
end

