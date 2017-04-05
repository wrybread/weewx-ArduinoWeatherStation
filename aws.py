#!/usr/bin/env python
#
# Arduino Weather Station, adapted by wrybread@gmail.com.
#
# Connect a Davis anemometer to an Arduino as described here:
# http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer
#
# Installation instructions:
#
# On a CHIP, was simply "apt-get install arduino", Not sure if was necessary.
#
# Original copyright notices:
#
# Copyright 2014 Matthew Wall
# See the file LICENSE.txt for your rights.
# Modified by Yann Chemin for IWMI MWS station
# March 2015 Public Domain if previous copyright allows.
# Building Manual for the Mobile Weather Station is here:
# http://www.iwmi.cgiar.org/resources/mobile-weather-stations/




"""Driver for Arduion Weather Station.

Modified from MWS weather station from here:

https://github.com/YannChemin/MWS

That was modified from weewx/trunk/drivers/ws1.py 

"""

from __future__ import with_statement
import serial
import syslog
import time

import weewx.drivers

DRIVER_NAME = 'AWS'
DRIVER_VERSION = '0.1'


def loader(config_dict, _):
    return AWSDriver(**config_dict[DRIVER_NAME])

def confeditor_loader():
    return AWSConfEditor()


INHG_PER_MBAR = 0.0295333727
METER_PER_FOOT = 0.3048
MILE_PER_KM = 0.621371

DEFAULT_PORT = '/dev/ttyACM0'
DEBUG_READ = 0






def logmsg(level, msg):
    syslog.syslog(level, 'aws: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

class AWSDriver(weewx.drivers.AbstractDevice):
    """weewx driver that communicates with an Arduino weather station
    
    port - serial port
    [Required. Default is /dev/ttyACM0]

    polling_interval - how often to query the serial interface, seconds
    [Optional. Default is 1]

    max_tries - how often to retry serial communication before giving up
    [Optional. Default is 5]

    retry_wait - how long to wait, in seconds, before retrying after a failure
    [Optional. Default is 10]
    """
    def __init__(self, **stn_dict):
        self.port = stn_dict.get('port', DEFAULT_PORT)
        self.polling_interval = float(stn_dict.get('polling_interval', 1))
        self.max_tries = int(stn_dict.get('max_tries', 5))
        self.retry_wait = int(stn_dict.get('retry_wait', 10))
        self.last_rain = None
        loginf('driver version is %s' % DRIVER_VERSION)
        loginf('using serial port %s' % self.port)
        loginf('polling interval is %s' % self.polling_interval)
        global DEBUG_READ
        DEBUG_READ = int(stn_dict.get('debug_read', DEBUG_READ))

        self.last_read_time = time.time()

    @property
    def hardware_name(self):
        return "AWS"

    def genLoopPackets(self):

        ntries = 0

        
        while ntries < self.max_tries:
            
            ntries += 1
            
            try:

                packet = {'dateTime': int(time.time() + 0.5),
                          'usUnits': weewx.US}
                # open a new connection to the station for each reading
                with Station(self.port) as station:
                    readings = station.get_readings()
                    
                data = Station.parse_readings(readings)

                packet.update(data)

                self._augment_packet(packet)

                ntries = 0


                # %%
                time_since_last_read = time.time() - self.last_read_time
                print "%s seconds since last read" % time_since_last_read
                self.last_read_time = time.time()
                
                yield packet

                if self.polling_interval:
                    time.sleep(self.polling_interval)

                    
            except (serial.serialutil.SerialException, weewx.WeeWxIOError), e:
                logerr("Failed attempt %d of %d to get LOOP data: %s" %
                       (ntries, self.max_tries, e))

                time.sleep(self.retry_wait)
        else:
            msg = "Max retries (%d) exceeded for LOOP data" % self.max_tries
            logerr(msg)
            raise weewx.RetriesExceeded(msg)

    def _augment_packet(self, packet):
        # calculate the rain delta from rain total
        #if self.last_rain is not None:
        #    packet['rain'] = packet['long_term_rain'] - self.last_rain
        #else:
        #    packet['rain'] = None
        #self.last_rain = packet['long_term_rain']

        # no wind direction when wind speed is zero
        if 'windSpeed' in packet and not packet['windSpeed']:
            packet['windDir'] = None
















class Station(object):

    
    def __init__(self, port):
        self.port = port
        self.baudrate = 9600
        self.timeout = 60
        self.serial_port = None

        #self.serial_port = self.open()




        

    def __enter__(self):

        self.open()
        return self

    def __exit__(self, _, value, traceback):
        self.close()

    def open(self):
        
        logdbg("open serial port %s" % self.port)

        try:
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logdbg("successfully opened the Arduino on port %s" % self.port)
        except Exception, e:
            logerr("Failed to open the Arduino: %s" % e)
            self.serial_port = None

        #self.serial_port = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

    def close(self):

        if self.serial_port is not None:
            logdbg("close Arduino on port %s" % self.port)

            try: self.serial_port.close()
            except: pass
            
            self.serial_port = None



    def read(self):

        # read the buffer
        data = ""

        try:
            while True:
                data = self.serial_port.readline()
                data = data.replace("\n", "")
                break

        except: pass
        
        return data


    def get_readings(self):
        
        b = self.read()
        if DEBUG_READ:
            logdbg(b)
        return b

    @staticmethod
    def parse_readings(b):
        """
	  AWS station emits csv data in the format:

          #Serial.print("lon,lat,altitude,sats,date,GMTtime,winddir");
          #Serial.print(",windspeedms,windgustms,windspdms_avg2m,winddir_avg2m,windgustms_10m,windgustdir_10m");
          #Serial.print(",humidity,tempc,rainhourmm,raindailymm,rainindicate,rain5minmm,pressure,batt_lvl,light_lvl");

          [0]wind speed
          [1]wind direction
          [2]wind direction compass
          [3]temperature
          [4]barometer
        """

        parts = b.split(",")
        
        #print "parsing: ", b, "parts =", parts
        
        data = dict()
        
        try: data['windSpeed'] = float(parts[0])  # mph
        except Exception, e:
            logerr("Error getting windSpeed: %s" % e)
            data['windSpeed'] = 0 # prob not a good idea to report 0 mph when the device isn't attached...
        
	try: data['windDir'] = float(parts[1])
	except Exception, e:
            logerr("Error getting windDir: %s" % e)
            data['windDir'] = 0 # prob not a good idea to report 0 mph when the device isn't attached...

	#data['windDirCompass'] = parts[2]  # wind speed compass. Unused, or probably wrong variable name.

        #%%
        print "aws: ", data


        if DEBUG_READ:
            logdbg(data)
        return data










class AWSConfEditor(weewx.drivers.AbstractConfEditor):
    @property
    def default_stanza(self):
        return """
[AWS]
    # This section is for an Arduion Weather Station.

    # Serial port such as /dev/ttyACM0, /dev/ttyS0, /dev/ttyUSB0, or /dev/cuaU0
    port = /dev/ttyACM0

    # The driver to use:
    driver = weewx.drivers.aws
"""

    def prompt_for_settings(self):
        print "Specify the serial port on which the station is connected, for"
        print "example /dev/ttyUSB0 or /dev/ttyACM0."
        port = self._prompt('port', '/dev/ttyACM0')
        return {'port': port}


# define a main entry point for basic testing of the station without weewx
# engine and service overhead.  invoke this as follows from the weewx root dir:
#
# Ubuntu standard set up with user driver:
# PYTHONPATH=bin python /usr/share/weewx/user/aws.py

if __name__ == '__main__':
    import optparse

    usage = """%prog [options] [--help]"""

    syslog.openlog('aws', syslog.LOG_PID | syslog.LOG_CONS)
    syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_DEBUG))
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--version', dest='version', action='store_true',
                      help='display driver version')
    parser.add_option('--port', dest='port', metavar='PORT',
                      help='serial port to which the station is connected',
                      default=DEFAULT_PORT)
    (options, args) = parser.parse_args()

    if options.version:
        print "AWS driver version %s" % DRIVER_VERSION
        exit(0)

    with Station(options.port) as s:
        while True:

            print time.time(), s.get_readings() 

