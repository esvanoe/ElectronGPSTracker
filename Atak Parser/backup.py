#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

# Set the Listening Server Options (host, port)
hostName = ""
hostPort = 8080

# Set the TAK Server IP and Port
global takServer
takServer = "123.123.123.123"
global takPort
takPort = 8088

# writeCot is the function to create the XML packet from the parsed data (XML.COT)
def writeCot():
    f = open("COT.xml", 'w')
    uid = "Erik's IOT"
    type = "a-f-G-M-F-U-M"
    f.write("""<?xml version='1.0' standalone='yes'?>
<event version="2.0"
    uid="{0}"
    type="{1}"
    time="{2}-{3}-{4}T{5}:{6}:{7}.00Z"
    start="{2}-{3}-{4}T{5}:{6}:{7}.00Z"
    stale="{2}-{3}-{4}T{5}:{8}:{7}.00Z" >
    <detail>
    </detail>
    <point lat="{9}" lon="{10}" ce="20"
        hae="0" le="20"  />
</event>""".format(uid, type, year, month, day, hours, minutes, seconds, staleMin, lat, lon ))
    f.close()
    cotSend()

#  cotSend pushes the newly created COT file to the TAK Server defined inside of it.
def cotSend():
    import socket
    sock = socket.socket()  # Create a socket object
    #   host = '54.213.93.44'  # tak server IP
    #   port = 8088  # TCP Stream Port
    sock.connect((takServer, takPort))

    f = open('COT.xml', 'rb')  # read the COT Data into memory
    print("Sending...")  # unnecessary in production
    l = f.read(4096)
    while (l):
        print("Sending...")  # unnecessary in production
        sock.send(l)
        l = f.read(4096)
    f.close()
    print("Done Sending")  # unnecessary in production
    sock.shutdown(socket.SHUT_WR)
    sock.close()

class MyServer(BaseHTTPRequestHandler):

    #   Function that listens for POST request and parses / stores data for writeCot().
    def do_POST(self):

        #       Handle the connection, receive POST Headers with GPS Data.
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        #       print(content_length)
        post_data = (self.rfile.read(content_length)) # <--- Gets the data itself
        self.send_response(200)
        self.end_headers()
        #       Put received data into variables
        strData = str(post_data)
        global year
        global month
        global day
        global hours
        global minutes
        global seconds
        global lat
        global lon
        global staleMin
        year = int((strData[24:28]))
        month = int((strData[29:31]))
        day = int((strData[32:34]))
        hours = int((strData[35:37]))
        minutes = int((strData[38:40]))
        seconds = int((strData[41:43]))
        lat = float((strData[62:71]))
        lon = float((strData[72:82]))
        if month < 10:
            month = str("0{}".format(month))
        if day < 10:
            day = str("0{}".format(day))
        if hours < 10:
            hours = str("0{}".format(hours))
        if minutes < 10:
            minutes = str("0{}".format(minutes))
        if minutes < 58:
            staleMin = minutes + 2
        if minutes == 58:
            staleMin = "00"
        if minutes == 59:
            staleMin = "01"
        if seconds < 10:
            seconds = str("0{}".format(seconds))
        print("The Date is {} Month(s), {} Day(s) into Year {} \n".format(month, day, year))
        print("time is {} Hours, {} Minutes and {} Seconds \n".format(hours, minutes, seconds))
        print("Your Latitude is {} and your Longitude is {} \n".format(lat, lon))
        print('Making COT Packet for you now \n')
        writeCot()

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
