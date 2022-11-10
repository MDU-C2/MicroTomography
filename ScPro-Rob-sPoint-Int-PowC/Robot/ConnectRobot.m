
function t = ConnectRobot()
    t = tcpclient('10.132.158.88',55000);
    flush (t);
end
        
%         function status = checkConnection(obj)
%             status = 1;
%         end
