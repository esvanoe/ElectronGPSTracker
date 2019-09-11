// This #include statement was automatically added by the Particle IDE.
#include <AssetTracker.h>

/* -----------------------------------------------------------
This example shows a lot of different features. As configured here
it will check for a good GPS fix every 10 minutes and publish that data
if there is one. If not, it will save you data by staying quiet. It also
registers 3 Particle.functions for changing whether it publishes,
reading the battery level, and manually requesting a GPS reading.
---------------------------------------------------------------*/

// Getting the library
#include "AssetTracker.h"

// Set whether you want the device to publish data to the internet by default here.
// 1 will Particle.publish AND Serial.print, 0 will just Serial.print
// Extremely useful for saving data while developing close enough to have a cable plugged in.
// You can also change this remotely usng the Particle.function "tmode" defined in setup()
int transmittingData = 1;

// Used to keep track of the last time we published data
long lastPublish = 0;

// How many minutes between publishes? 10+ recommended for long-time continuous publishing!
int delayMinutes = 1;

// Creating an AssetTracker named 't' for us to reference
AssetTracker t = AssetTracker();

// A FuelGauge named 'fuel' for checking on the battery state
FuelGauge fuel;

// setup() and loop() are both required. setup() runs once when the device starts
// and is used for registering functions and variables and initializing things
void setup() {
    // Sets up all the necessary AssetTracker bits
    t.begin();

    // Enable the GPS module. Defaults to off to save power.
    // Takes 1.5s or so because of delays.
    t.gpsOn();

    // Opens up a Serial port so you can listen over USB
    Serial.begin(9600);

}

// loop() runs continuously
void loop() {
    // You'll need to run this every loop to capture the GPS output
    t.updateGPS();
    float value;
    value = fuel.getVCell();
    String output = "{\"VOLTS\": \"" + String(value) + "\"}";

    // if the current time - the last time we published is greater than your set delay...
    if (millis()-lastPublish > delayMinutes*60*1000) {
        // Remember when we published
        lastPublish = millis();

        //String pubAccel = String::format("%d,%d,%d", t.readX(), t.readY(), t.readZ());
        //Serial.println(pubAccel);
        //Particle.publish("A", pubAccel, 60, PRIVATE);

        // Dumps the full NMEA sentence to serial in case you're curious
        Serial.println(t.preNMEA());

        // GPS requires a "fix" on the satellites to give good data,
        // so we should only publish data if there's a fix
        if (t.gpsFix()) {
            // Only publish if we're in transmittingData mode 1;
            if (transmittingData) {
                // Short publish names save data!
                Particle.publish("GPS", t.readLatLon(), 60, PRIVATE);
                Particle.publish("Vdc", output, 60, PRIVATE);
            }
            // but always report the data over serial for local development
            Serial.println(t.readLatLon());
            }
        else {
            if (transmittingData) {
                Particle.publish("Fail", "1", 60, PRIVATE);
                Particle.publish("Vdc", output, 60, PRIVATE);
            }
            Serial.println(t.readLatLon());
        }
        
    }
}
