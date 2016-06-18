import os
import sys
import threading
import time
class ledstatus():
	status = 0
	led_clear = 0
	
	def run(self,state):
		if state == self.EEPROM_TEST:
			t = threading.Thread(target=self.eeprom_led)
			t.start()
		if state == self.DDR_TEST:
			t= threading.Thread(target=self.ddr_led)
			t.start()
		if state == self.GPIO_TEST:
			t= threading.Thread(target=self.gpio_led)
			t.start()
		if state == self.VOLTAGE_TEST:
			t= threading.Thread(target=self.voltage_led)
			t.start()
		if state == self.NET_TEST:
			t= threading.Thread(target=self.net_led)
			t.start()
		if state == self.EMMC_TEST:
			t= threading.Thread(target=self.emmc_led)
			t.start()
		if state == self.TEST_OK:
			t= threading.Thread(target=self.ok_led)
			t.start()
		if state == self.TEST_FAIL:
			t= threading.Thread(target=self.error_led)
			t.start()

	def eeprom_led(self):
		self.userLedAllOff()
		while True:
			if self.led_clear == 1:
				break
			self.userLed1On()
			self.userLed2Off()
			self.userLed3Off()
			self.userLed4On()
			time.sleep(0.1)
			self.userLed1Off()
			self.userLed2On()
			self.userLed3On()
			self.userLed4Off()
			time.sleep(0.1)


	def ddr_led(self):
		self.userLedAllOff()
                while True:
                        if self.led_clear == 1:
                                break
                        self.userLed2Off()
                        time.sleep(0.2)
                        self.userLed2On()
                        time.sleep(0.2)

	
	def gpio_led(self):
		self.userLedAllOff()
                while True:
                        if self.led_clear == 1:
                                break
                        self.userLed3Off()
                        time.sleep(0.2)
                        self.userLed3On()
                        time.sleep(0.2)

	
	def voltage_led(self):
		self.userLedAllOff()
                while True:
                        if self.led_clear == 1:
                                break
                        self.userLed4Off()
                        time.sleep(0.2)
                        self.userLed4On()
                        time.sleep(0.2)


	def net_led(self):
		self.userLedAllOff()
                while True:
                        if self.led_clear == 1:
                                break
                        self.userLed1Off()
                        self.userLed2Off()
                        self.userLed3On()
                        self.userLed4On()
                        time.sleep(0.2)
                        self.userLed1On()
                        self.userLed2On()
                        self.userLed3Off()
                        self.userLed4Off()
                        time.sleep(0.2)

	
	def emmc_led(self):
		self.userLedAllOff()
                while True:
                        if self.led_clear == 1:
                                break
                        self.userLed1Off()
                        self.userLed2Off()
                        self.userLed3Off()
                        time.sleep(0.2)
                        self.userLed1On()
                        self.userLed2On()
                        self.userLed3On()
                        time.sleep(0.2)

	
	def error_led(self):
		self.userLedAllOff()
                while True:
                        if self.led_clear == 1:
                                break
                        self.userLed1Off()
                        self.userLed2Off()
                        self.userLed3Off()
                        self.userLed4Off()
                        time.sleep(0.2)
                        self.userLed1On()
                        self.userLed2On()
                        self.userLed3On()
                        self.userLed4On()
                        time.sleep(0.2)

	
	def ok_led(self):
		self.userLedAllOff()
                while True:
                        if self.led_clear == 1:
                                break
                        self.userLed1Off()
                        self.userLed2On()
                        self.userLed3Off()
                        self.userLed4On()
                        time.sleep(0.2)
                        self.userLed1On()
                        self.userLed2Off()
                        self.userLed3On()
                        self.userLed4Off()
                        time.sleep(0.2)
	
		
	def userLed1On(self):
		os.system('echo 255 > /sys/class/leds/beaglebone:green:usr0/brightness')

	def userLed1Off(self):
		os.system('echo 0 > /sys/class/leds/beaglebone:green:usr0/brightness')

	def userLed2On(self):
		os.system('echo 255 > /sys/class/leds/beaglebone:green:usr1/brightness')

	def userLed2Off(self):
		os.system('echo 0 > /sys/class/leds/beaglebone:green:usr1/brightness')

	def userLed3On(self):
		os.system('echo 255 > /sys/class/leds/beaglebone:green:usr2/brightness')

	def userLed3Off(self):
		os.system('echo 0 > /sys/class/leds/beaglebone:green:usr2/brightness')
	
	def userLed4On(self):
		os.system('echo 255 > /sys/class/leds/beaglebone:green:usr3/brightness')
	
	def userLed4Off(self):
		os.system('echo 0 > /sys/class/leds/beaglebone:green:usr3/brightness')
	def userLedAllOn(self):
		self.userLed1On()
		self.userLed2On()
		self.userLed3On()
		self.userLed4On()

	def userLedAllOff(self):
		self.userLed1Off()
		self.userLed2Off()
		self.userLed3Off()
		self.userLed4Off()
		
		
        def __init__(self,value):
                self.status = value

                self.EEPROM_TEST = 0
                self.DDR_TEST = 1
                self.GPIO_TEST = 2
                self.VOLTAGE_TEST = 3
                self.NET_TEST = 4
                self.EMMC_TEST = 5
                self.TEST_OK = 6
                self.TEST_FAIL = 7
                self.run(self.status)


if __name__ == '__main__':
	cnt = 0
	t_eeprom = ledstatus(0)
	while cnt < 30:
		time.sleep(1)
		cnt += 1
		print "eeprom is runing"
	t_eeprom.led_clear = 1

	cnt = 0
	t_ddr = ledstatus(1)
	while cnt < 3:
		time.sleep(1)
		cnt += 1
		print "ddr is runing"
	t_ddr.led_clear = 1

        cnt = 0
        t_gpio = ledstatus(2)
        while cnt < 3:
                time.sleep(1)
                cnt += 1
                print "gpio is runing"
        t_gpio.led_clear = 1

        cnt = 0
        t_voltage = ledstatus(3)
        while cnt < 3:
                time.sleep(1)
                cnt += 1
                print "voltage is runing"
        t_voltage.led_clear = 1

        cnt = 0
        t_net = ledstatus(4)
        while cnt < 30:
                time.sleep(1)
                cnt += 1
                print "net is runing"
        t_net.led_clear = 1

        cnt = 0
        t_emmc = ledstatus(5)
        while cnt < 3:
                time.sleep(1)
                cnt += 1
                print "emmc is runing"
        t_emmc.led_clear = 1

        cnt = 0
        t_ok = ledstatus(6)
        while cnt < 3:
                time.sleep(1)
                cnt += 1
                print "ok is runing"
        t_ok.led_clear = 1

        cnt = 0
        t_error = ledstatus(7)
        while cnt < 5:
                time.sleep(1)
                cnt += 1
                print "error is runing"
        t_error.led_clear = 1
