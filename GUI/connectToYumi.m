function [status, connection] = connectToYumi(app)
%connect to server through ip (TCP)
writeToLog(app, "Connect to robot: Starting connection through TCP.");
connection = tcpclient('10.132.158.88',55000);
if connection.Status == "open"
    status = 1;
    writeToLog(app, "Connect to robot: TCP connection to robot successful.");
else
    status = 0;
    writeToLog(app, "Connect to robot: TCP connection to robot failed.");
end
end