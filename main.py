#import electroServer.electrolink as electrolink
import electrolink
# electroDebug is pc based electrolink, just for testing purposes, doing nothing in electronics
#import modules.electroFiles as electroFiles
import electroFiles

import network
# real interface with electronics for ESP8266 processor
#import electroGPIO
from machine import Pin

import time
from ujson import loads
config = loads((open("config.json", "r").read()))

# Give board a name
e = electrolink.Electrolink(config["thing_name"])

# extend Electrolink with additional fnctions
e.addCallbacks(electroFiles.callbacks)

debugLed = Pin(2, Pin.OUT)

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
while not(sta_if.isconnected()):
    debugLed.value(1)
    time.sleep(0.1)
    debugLed.value(0)
    time.sleep(0.1)

# Broker MQTT server, mqtt protocol default port 1883
e.connectToServer(config["broker_server"])

while True:
    # blocking function, waiting for new message
    e.waitForMessage()

    # or use non-blocking message to do something else in this file
    # while checking for new messages
    #e.checkForMessage()
