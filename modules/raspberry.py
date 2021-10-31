from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from time import sleep

class LcdHandler(CharLCD):
    def __init__(self):
        CharLCD.__init__(self, pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD)

    def writeString(self, string):
        self.write_string(string)
        sleep(2)
        self.clear()

    def stop(self):
        self.clear()
        GPIO.cleanup()
 

