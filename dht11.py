import Adafruit_DHT
import platform

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.

# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
#pin = 'P8_11'



# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
def getTemperatureAndHumudityInterior():
    if platform.processor() == 'x86_64':
        return("DHT module not supported")
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 18)
# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
    if humidity is not None and temperature is not None:
        return('T={0:0.1f}*C  Hum={1:0.1f}%'.format(temperature, humidity))
    else:
        return('Failed to get reading. Try again!')

