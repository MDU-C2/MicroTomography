function status = checkConnectionStatus(app, connection)
%checks the status of the connection
if connection.Status == "open"
    status = 1;
else
    status = 0;
    writeToLog(app, "Connection to robot lost.");
end

end
