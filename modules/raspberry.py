from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
from time import sleep

class LcdHandler(CharLCD):
    def __init__(self):
        CharLCD.__init__(self, pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD, auto_linebreaks=False, cols=16, rows=2)

    def writePrediction(self, product, price, weight):
        totalPrice = round(price*weight/1000,2)
        self.clear()
        self.cursor_pos = (0,0)
        self.write_string(product) 
        self.cursor_pos = (1,0)
        self.write_string(str(price) + "e/kg " + str(weight) + "g")
        sleep(1)
        self.cursor_pos = (1,0)
        totalPriceStr = "Total " + str(totalPrice) +  "e"
        
        for i in range(15-len(totalPriceStr)):
            totalPriceStr += " "

        self.write_string(totalPriceStr)
        sleep(1)
        #self.clear()

    def writeString(self, string):
        self.write_string(string)
        sleep(2)
        self.clear()

    def stop(self):
        self.clear()
        self.close(clear=True)
        GPIO.cleanup()
 

