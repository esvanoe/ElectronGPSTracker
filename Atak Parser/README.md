# ATAK Listener and Parser

Running parser.py will open up a listener on port 8080 that accepts incoming JSON from a Particle.IO Webhook event from 
the Electron Asset Tracker. 

Upon receiving a POST from Particle, Parser.py will translate the JSON to COT, and save it to cot.xml in the same 
running directory and then initiate sendcot() to push the file to a listening TAK server.

Now you have pretty blue or red or yellow dots on your moving SA map.

Congrats!
