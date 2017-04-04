# Arduino Weather Station

This is some code to connect a Davis anemometer directly to an Arduino, without the Davis base station (ISS). The anemometer I used is sold as a replacement for the anemomter on the Davis Vantage Pro2. They're on eBay in the $110 range. I think the part name is "Davis Instruments 6410 Davis Anemometer For Vantage Pro Pro2 6152"

To connect the anemometer to the Arduino, use the excellent instructions here:

http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer

For the Arduino sketch, use ArduinoWeather.ino

To read the data from the Arduino on a Raspberry Pi or whatever, see arduino_test.py

To use this with the weeWX weather station program, see the driver aws.py.

