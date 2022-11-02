classdef ConnectRobot
    methods
        function t = connect(obj)
            t = tcpclient('192.168.125.1',55000);
            flush (t);
        end
        
        function status = checkConnection(obj)
            status = 1;
        end
    end
end