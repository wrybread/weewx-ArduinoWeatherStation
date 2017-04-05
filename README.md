# Arduino Weather Station

This is some code to connect a Davis anemometer directly to an Arduino, without the Davis base station (ISS). The anemometer I used is sold as a replacement for the anemomter on the Davis Vantage Pro2. They're on eBay in the $110 range. The one I purchased had the auction name "Davis Instruments 6410 Davis Anemometer For Vantage Pro Pro2 6152".

With this method you get a pro quality internet connected wind gauge for about $130! That's assuming $10 for the Arduino and $10 for the CHIP computer that's running weeWX. Not bad!

Here's a wiring diagram to connect the Davis anemometer to an Arduino:

![alt tag](https://github.com/wrybread/ArduinoWeatherStation/raw/master/arduino-to-davis-anemometer-hookup-circuit.jpg)

Or use the instructions here:

http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer

For the Arduino sketch, see ArduinoWeather.ino, which I adapted from the code at the above link.

To read the data from the Arduino on a Raspberry Pi or CHIP or whatever, see arduino_test.py

To use this with the weeWX weather station program, see the driver aws.py.

For my purposes wind is the biggie, but it would be easy enough to add a thermometer and barometer and other sensors to the Arduino.

## To do:

- add other sensors

## Installation 

- load ArduinoWeather.ino onto your Arduino

- install the weeWX driver file. I'm putting it in /home/weewx/bin/weewx/drivers/aws.py, but I don't think that's the correct location

- add this section to your weeWX config file:

[AWS]

    # This section is for an Arduion Weather Station.

    # Serial port such as /dev/ttyACM0, /dev/ttyS0, /dev/ttyUSB0, or /dev/cuaU0
    port = /dev/ttyACM0

    # The driver to use:
    driver = weewx.drivers.aws

- in the [Station] section of your weeWX config file, set "station_type" to "AWS".

