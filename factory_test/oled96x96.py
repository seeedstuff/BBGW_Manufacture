import time, signal, sys
import pyupm_i2clcd as upmLCD

class OLED96x96:
    def __init__(self):
        self.oled = upmLCD.SSD1327(1, 0x3C);
        self.oled.setGrayLevel(12)
        self.oled.setCursor(0,0)
        self.line = 0

    def printEnter(self):
        self.line = self.line + 1
        
    def printBackLine(self):
        self.line = self.line - 1
        
    def myPrint(self,tittle,status):
        self.oled.setCursor(self.line, 0)
        self.oled.write(tittle)
        self.oled.write(': ')
        self.oled.write(status)
        self.printEnter()
        
    def printBottom(self, tittle, status):
        self.oled.setCursor(11,0)
        self.oled.write(tittle)
        self.oled.write(": ")
        self.oled.write(status)
        
if __name__=="__main__":
    oled = OLED96x96()
    oled.myPrint("UART", "  OK")
    oled.myPrint("UART", "  OK")
    oled.myPrint("UART", "  OK")
    oled.printBottom('BT', "    OK")
    print "Existing"


