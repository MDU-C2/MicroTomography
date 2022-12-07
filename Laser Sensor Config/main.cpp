#include <iostream>
#include <vector>
#include <string>
#include "MEDAQLib.h"
#include <windows.h>
#include <assert.h>

using namespace std;



int main()
{
    /*vector<string> msg {"Hello", "C++", "World", "from", "VS Code", "and the C++ extension!"};

    for (const string& word : msg)
    {
        cout << word << " ";
    }
    cout << endl;*/

    // HINSTANCE hInstance= LoadLibrary((LPCSTR)"MEDAQLib-4.12.0.31896\\Release-x64\\MEDAQLib.dll");

    // FARPROC pCreateSensorInstance =  GetProcAddress(hInstance, "CreateSensorInstance");

    // FARPROC pReleaseSensorInstance = GetProcAddress(hInstance, "ReleaseSensorInstance");

    // uint32_t hSensor = pCreateSensorInstance();

    // cout << hSensor;

    // Tell MEDAQLib about sensor type to be used.
    uint32_t hSensor = CreateSensorInstByName("optoNCDT 1302"); //must not return zero
    assert(hSensor != 0);

    //Setup MEDAQLib for RS422 (emulated RS232) sensor communication
    ERR_CODE err = SetParameterString(hSensor, "IP_Interface", "RS232"); //f the IF2001_USB (RS422) is used "RS232" must be set, because a RS232 interface is emulated.
    assert(err == 0); //returns ERR_NOERROR (0) on success

    //Set com port
    err = SetParameterString(hSensor, "IP_Port", "COM5");
    assert(err == 0);

    //Set baudrate
    err = SetParameterInt(hSensor, "IP_Baudrate", 115200);
    assert(err == 0);

    // Enable Logfile writing
    err = SetParameterInt (hSensor, "IP_EnableLogging", 1);
    assert(err == 0);

    //"Open" connection to sensor
    err = OpenSensor(hSensor);
    assert(err == 0);



    

    // In the following we try to always get 200 values from sensor.
/*
    while (1 == 1)
    {
        // Check whether there’s enough data to read in.
        int32_t currentlyAvailable = 0;
        err = DataAvail(hSensor, &currentlyAvailable);

        if (currentlyAvailable > 200){
            // Allocate memory to get raw and scaled data into.
            int32_t rawData[200];
            double scaledData[200];
            // Set additional parameters for TransferData;
            int32_t expectedBlockSize = 200;
            int32_t gotBlockSize = 0;
            // Fetch data from MEDAQLib’s internal buffer.
            err = TransferData(hSensor, rawData, scaledData, expectedBlockSize, &gotBlockSize);
            // Now expectedBlockSize should be equal to gotBlockSize.
            // rawData contains original values from sensor, scaledData contains scaled data.
            // Do your computation on data ....
            cout << scaledData;
        }
        Sleep(10); // Sleep 10ms, allow other things to happen, ....
    }

*/
}

