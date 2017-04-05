/*

Adapted from the excellent work here:

http://cactus.io/hookups/weather/anemometer/davis/hookup-arduino-to-davis-anemometer

Works with a Davis anemometer, which is available on eBay in the $110 range.

Intended to interface with the weeWX program but easily adapted for other uses.

See https://github.com/wrybread/ArduinoWeatherStation

wrybread@gmail.com


*/


#include "TimerOne.h" // Timer Interrupt set to 2 second for read sensors 
#include <math.h> 

#define WindSensorPin (2) // The pin location of the anemometer sensor 
#define WindVanePin (A4) // The pin the wind vane sensor is connected to 
#define VaneOffset 0; // define the anemometer offset from magnetic north 


int vaneValue; // raw analog value from wind vane 
int windDirection; // translated 0 - 360 direction 
int windCalDirection; // converted value with offset applied 
String windCompassDirection; // wind direction as compass points
int lastWindDirectionValue; // last direction value 

// sensors to be added
int temperature;
int barometer; 


volatile bool IsSampleRequired; // this is set true every 2.5s. Get wind speed 
volatile unsigned int TimerCount; // used to determine 2.5sec timer count 
volatile unsigned long Rotations; // cup rotation counter used in interrupt routine 
volatile unsigned long ContactBounceTime; // Timer to avoid contact bounce in isr 

float WindSpeed; // speed miles per hour 




void setup() { 

  lastWindDirectionValue = 0; 
  
  IsSampleRequired = false; 
  
  TimerCount = 0; 
  Rotations = 0; // Set Rotations to 0 ready for calculations 
  
  Serial.begin(9600); 
  
  pinMode(WindSensorPin, INPUT); 

  //@@ Ooops, typo in this line from the original script
  //attachInterrupt(digitalPinToInterrupt(WindSensorPin), rotation, FALLING); 
  attachInterrupt(digitalPinToInterrupt(WindSensorPin), isr_rotation, FALLING); 
  
  Serial.println("Arduino Weather Station"); 
  
  // Setup the timer interupt 
  Timer1.initialize(500000);// Timer interrupt every 2.5 seconds 
  Timer1.attachInterrupt(isr_timer); 

} 

void loop() { 

  getWindDirection(); 


  // placeholders for temperature and barometer.
  temperature = 0;
  barometer = 0;

  
  // Only update the display if change greater than 5 degrees. 
  if(abs(windCalDirection - lastWindDirectionValue) > 5) { 
    lastWindDirectionValue = windCalDirection; 
  } 

  if(IsSampleRequired) { 
    // convert to mp/h using the formula V=P(2.25/T) 
    // V = P(2.25/2.5) = P * 0.9 
    WindSpeed = Rotations * 0.9; 
    Rotations = 0; // Reset count for next sample 
    
    IsSampleRequired = false; 

    /*
    // output the data in a way that's easy to read by a Raspberry Pi or whatever
    // will output for example: wind_speed=5.47,wind_direction=343,wind_compass_direction=N,temperature=0,barometer=0,
    Serial.print("wind_speed="); Serial.print(getKnots(WindSpeed)); Serial.print(",");
    Serial.print("wind_direction="); Serial.print(windCalDirection);  Serial.print(",");
    Serial.print("wind_compass_direction="); Serial.print(windCompassDirection);  Serial.print(",");
    Serial.print("temperature="); Serial.print(temperature);  Serial.print(",");
    Serial.print("barometer="); Serial.print(barometer);  Serial.print(",");
    Serial.println();
    */

    // this section outputs the data in a way that's easy to read by my weeWX driver (comma delimited list)
    //Serial.print(getKnots(WindSpeed)); Serial.print(",");
    Serial.print(WindSpeed); Serial.print(",");
    Serial.print(windCalDirection);  Serial.print(",");
    Serial.print(windCompassDirection);  Serial.print(",");
    Serial.print(temperature);  Serial.print(",");
    Serial.print(barometer);  Serial.print(",");
    Serial.println();
    

    // or output the data in a way that's easy to read by good old fashioned humans:
    //Serial.print("Wind is blowing "); Serial.print(getKnots(WindSpeed)); Serial.print(" knots from the "); Serial.println(windCompassDirection); 
  
  } 
} 


// isr handler for timer interrupt 
void isr_timer() { 

  TimerCount++; 
  
  if(TimerCount == 6) { 
    IsSampleRequired = true; 
    TimerCount = 0; 
  } 
} 




// This is the function that the interrupt calls to increment the rotation count 
void isr_rotation() { 

  if((millis() - ContactBounceTime) > 15 ) { // debounce the switch contact. 
    Rotations++; 
    ContactBounceTime = millis(); 
  } 

} 






// Get Wind Direction 
void getWindDirection() { 

  vaneValue = analogRead(WindVanePin); 
  windDirection = map(vaneValue, 0, 1023, 0, 360); 
  windCalDirection = windDirection + VaneOffset; 
  
  if(windCalDirection > 360) windCalDirection = windCalDirection - 360; 
  if(windCalDirection < 0) windCalDirection = windCalDirection + 360; 


  // get the compass direction for convenience
  if (windCalDirection < 22) windCompassDirection = "N";
  else if (windCalDirection < 67) windCompassDirection = "NE";
  else if (windCalDirection < 112) windCompassDirection = "E";
  else if (windCalDirection < 157) windCompassDirection = "SE";
  else if (windCalDirection < 212) windCompassDirection = "S";
  else if (windCalDirection < 247) windCompassDirection = "SW";
  else if (windCalDirection < 292) windCompassDirection = "W";
  else if (windCalDirection < 337) windCompassDirection = "NW";
  else windCompassDirection = "N";  

} 






// Convert MPH to Knots 
float getKnots(float speed) { 
  return speed * 0.868976; 
} 
