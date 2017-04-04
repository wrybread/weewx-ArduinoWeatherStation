# Arduino Weather Station

This is some code to connect a Davis anemometer directly to an Arduino, without the Davis base station (ISS). The anemometer I used is sold as a replacement for the anemomter on the Davis Vantage Pro2. They're on eBay in the $110 range. The one I purchased had the auction name "Davis Instruments 6410 Davis Anemometer For Vantage Pro Pro2 6152".

With this method you get a pro quality internet connected wind gauge for about $130! That's assuming $10 for the Arduino and $10 for the CHIP computer that's running weeWX. Not bad!

To connect the anemometer to the Arduino, use the excellent instructions here:

http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer

For the Arduino sketch, see ArduinoWeather.ino, which I adapted from the code at the above link.

To read the data from the Arduino on a Raspberry Pi or CHIP or whatever, see arduino_test.py

To use this with the weeWX weather station program, see the driver aws.py.

