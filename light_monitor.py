#!/usr/local/bin/python
# ref: https://pimylifeup.com/raspberry-pi-light-sensor/

import RPi.GPIO as GPIO # communicate with GPIO pins
import time # tell the script when to sleep
import subprocess # opens the audio file(s)
import numpy # math fxns, used to calc average brightness
import os # fs access
import random # randomize the audio file to play

GPIO.setmode(GPIO.BOARD) # set the numbering we use in this script to refer to the physical numbering of the rpi pins


# GLOBAL CONFIGS
__pin_to_circuit__ = 7 # pin that goes to the circuit (the I/O pin on the RPI)
__brightness_threshhold__ = 400 # lights at 100% have ~300-350 light_level
__delay_between_plays__ = 15 * 60 # delay (s) for next light level check after brightness_threshhold is exceeded


# measures and returns the brightness level
def get_brightness (__pin_to_circuit__):
    count = 0

    # output on the pin for 
    GPIO.setup(__pin_to_circuit__, GPIO.OUT)
    GPIO.output(__pin_to_circuit__, GPIO.LOW)
    time.sleep(0.75) # delay between reedings

    # change the pin back to input
    GPIO.setup(__pin_to_circuit__, GPIO.IN)

    # count until the pin goes high
    while (GPIO.input(__pin_to_circuit__) == GPIO.LOW):
        count += 1

    return count # this reading reflects the brightness level

# plays a random audio file from our list
def play_music ():
  # play a random file
    audio_files = os.listdir('./assets')
    pid = subprocess.Popen(["/usr/bin/mpg321", "assets/" + random.choice(audio_files)])
    
    time.sleep(15) # "Blinded By The Light" lyric ends 15s into the .mp3
    pid.kill()


# Main
try:
    current_light_levels = [0,0,0,0,0] # track the last 5 light levels

    while True:
        
        # get current brightness
        light_level = get_brightness(__pin_to_circuit__)
        print light_level
        
        # track last 5 brightness measurements...
        current_light_levels.insert(0, light_level)
        current_light_levels.pop()
        
        # ...and play our song if the lights blind the shit out of us
        average_brightness = numpy.average(current_light_levels)
        if (
               all(readings > 0 for readings in current_light_levels) and\
               average_brightness < __brightness_threshhold__
           ):
            play_music()
            current_light_levels = [0,0,0,0,0] # reset our readings
            time.sleep(__delay_between_plays__)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()