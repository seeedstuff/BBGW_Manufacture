
#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
import time
import os
import pins
if __name__ == "__main__":
   status,rt = pins.check_voltage()
   if status == 'ok':
      for v in rt:
         print v

   print pins.check_io()

   status,rt = pins.check_power()
   print  status
   if status == 'ok':
      for v1 in rt:
         print v1