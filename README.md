Code for using the Electron from Particle.IO as a GPS Tracker as well as receiveing the output of that device and working with the data.

Last Updated:

11 September 2019

GPSTracker.ino is the code for an Electron device with a v2 GPS Tracker board. One must import both httpclient.h and the AssetTracker.h libraries for it to work.

Need to add the python server that catches requests from the board and modifies them into COT format for use with something like ATAK or anything else that catches COT packets for situational awareness.

