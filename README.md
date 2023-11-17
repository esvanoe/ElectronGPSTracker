# Electron GPS Tracker for ATAK

Use a cellular Electron from Particle.IO as a GPS Tracker (just how it was designed) 

Type1 GPS Tracker relies on a Particle.IO Console webhook to receive the variables and resend them in JSON to a lsitening server (server.py) hosted somewhere.

Type2 GPS Tracker is being re-written to take Particle out as the middle man and utilize httpclient.h to manage all the web traffic direct from the device to the listening translation server.

Relies on both httpclient.h and AssetTracker.h libraries to run.

TODO: Finish uploading python server code, example webhook.
