import socket
import sys
import time


def getDistance(ipComputer, ComputerPort, ipArduino, ArduinoPort):
    #For reciving data
    sockk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sockk.bind((ipComputer, ComputerPort))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    
    while True:
        allData = []
        i = 0
        for _ in range(0,8):
            time.sleep(0.01)
            sock.sendto("Get".encode(), (ipArduino, ArduinoPort))
            data, addr = sockk.recvfrom(4096)
            data = data.decode('utf-8')
            #data = data.replace('\r', '')
            #print("'"+data+"'")
            #print(data)
            #print(data.isnumeric())
            #allData.append(int(data))

            #Try to append it as an int, otherwise append as string. This will cause the check later on to fail and redo the 4 measurements.
            try:
                allData.append(int(data))
            except:
                allData.append(data)

         
          


        if len(set(allData)) == 1:
            if allData[0] == 16370:
                return "no object detected"
            elif allData[0] == 16372:
                return "too close to the sensor"
            elif allData[0] == 16374:
                return "too far from the sensor"
            elif allData[0] == 16376:
                return "target can not be evaluated"
            else:
                return ((((allData[0]*(1.02/4096))-0.01)*200)+60)

    


sys.stdout.write(str(getDistance(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))))
sys.stdout.flush()
sys.exit(0)

