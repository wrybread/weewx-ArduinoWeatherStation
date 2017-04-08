# Arduino Weather Station

This is some code to enable connecting a Davis anemometer directly to an Arduino, without the Davis base station (aka the "ISS") or the console. The Arduino then sends the wind data to whatever computer it's attached to as serial data. I also wrote a driver to use it with my favorite weather station proram, weeWX. So connect it to your Raspberry Pi or whatever and you get a pro quality internet connected wind gauge for about $130.

The anemometer I used is sold as a replacement part for the Davis Vantage Pro2. They're on eBay in the $110 range. The one I purchased had the auction name "Davis Instruments 6410 Davis Anemometer For Vantage Pro Pro2 6152". 

Here's a test page I put up that's receiving data from it every few seconds:

http://rproductions.org/wind


## Wiring and Setup

Here's a wiring diagram to connect the Davis anemometer to an Arduino thanks to the good folks at [cactus.io](http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer):

![alt tag](https://github.com/wrybread/ArduinoWeatherStation/raw/master/arduino-to-davis-anemometer-hookup-circuit.jpg)

Or use their instructions directly, since there's a bit more detail on their site:

http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer

A nice way to wire up the anemometer is to use a phone cable extension chord or coupler so you don't need to splice the line coming from the anemometer. Works great but don't forget to flip the wire layout in the diagram above. I unfortunately had to learn that one the hard way. But the good news is that there appears to be some reverse polarity protection in the anemometer...

For the Arduino sketch, see ArduinoWeather.ino above, which I adapted from the code [at cactus.io](http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer):

Then simply connect the Arduino to the USB port of your Pi or whatever. Note the script arduino_test.py, which should start printing the data being sent by your Arduino. If not, you might have to set your port at the top of the file.

To use this with the weeWX weather station program, see the driver aws.py. I need to package it with the weeWX extension manager to make installation a bit easier.


## Installation 

- load ArduinoWeather.ino onto your Arduino

- install the AWS weeWX driver included here (aws.py) in your user directory. It *should* be possible to use the wee_extension tool to install it (see below for instructions), but I haven't confirmed that yet. Anyway, copying the driver (aws.py) to weewx/bin/user/aws.py should do it.

- add this section to your weeWX config file:

[AWS]

    # This section is for an Arduion Weather Station.

    # Serial port such as /dev/ttyACM0, /dev/ttyS0, /dev/ttyUSB0, or /dev/cuaU0
    port = /dev/ttyACM0

    # The driver to use:
    driver = user.aws

- in the [Station] section of your weeWX config file, set "station_type" to "AWS".



## To do:

- set up the Arduino Weather Station next to a Davis Vantage Pro2 and compare the readings

- test installation using the wee_extension utility. These instructions should work:

1) Download the driver:

wget -O weewx-aws.zip https://github.com/wrybread/weewx-ArduinoWeatherStation.git

2) Install the driver:

sudo wee_extension --install weewx-aws.zip

3) Configure the driver:

sudo wee_config --reconfigure
