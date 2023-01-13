function [connected, waitingOnPos, TCPplotPos] = getAndPlotTCPposParallel(app, connection, TCPplotPos, wantedTCPplotPos)
%Reads and receives the actual (real-life) robot tcp position from
%connection and plots the acutal position on the plot. Runs in parallel to
%normal operation to always update user on the tcp location.
while true
    connected = checkConnectionStatus(app);
    if connected %when connected, receive and plot actual tcp position in the plot coordinate scale
        [pos, eulerDeg] = ReceiveAndUnpackPose(app, connection);
        plotPos = transRLtoPlot(app, pos);
        if ~isempty(TCPplotPos) %if there is no current plot for tcp pos plot it
            TCPplotPos = plot3(app.UIAxes, plotPos(1), plotPos(2), plotPos(3),'.','MarkerSize',100, 'Color','Blue');
        else %otherwise update its coordinates
            TCPplotPos.XData = plotPos(1);
            TCPplotPos.YData = plotPos(2);
            TCPplotPos.ZData = plotPos(3);
        end

        %signal to other functions if actual tcp pos matches the
        %wanted tcp pos.
        if TCPplotPos.XData == wantedTCPplotPos.XData && TCPplotPos.YData == wantedTCPplotPos.YData && TCPplotPos.ZData == wantedTCPplotPos.ZData
            waitingOnPos = 0;
        else
            waitingOnPos = 1;
        end
    else
        cancel(app.f); %terminate itself if connection is lost
        return
    end
    pause(0.5); %to not flood the computer
end

end