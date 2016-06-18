import os
import sys
from collections import OrderedDict
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False
    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
class FM:
	def __init__(self,type,name = ''):
		for case in switch(type):
			if case("version"):
				self.FileName = "/proc/version"
				break
			if case("eeprom"):
				self.FileName = "/sys/devices/ocp.3/44e0b000.i2c/i2c-0/0-0050/eeprom"
				break
			if case("ID"):
				self.FileName = ""	
				break
			if case("MAC"):
				self.FileName = ""
				break
			if case("DDR"):
				self.FileName = "/proc/meminfo"
				break
			if case("customer"):
				print "your file is %s"%name
		try:
			self.__FileHand = open(self.FileName,'rb+')
		except:
			print "sorry,I cannt open %s ,but I created it"%name
			self.__FileHand = open(name,'ab+')
	def readFileText(self,num = -1):
		return self.__FileHand.read(num)

	def writeFileText(self,str):
		self.__FileHand.write(str)

	def readMemory(self):
		meminfo=OrderedDict()
		with open(self.FileName) as f:
			for line in f:
				meminfo[line.split(':')[0]] = line.split(':')[1].strip()
		return  meminfo['MemTotal']

	def getemmcsize(self):
		nr_sectors = open('/sys/block/mmcblk0/size').read().rstrip('\n')
		sect_size = open('/sys/block/mmcblk0/queue/hw_sector_size').read().rstrip('\n')
		return  float(nr_sectors)*float(sect_size)/(1024.0*1024.0*1024.0)

	def check_otg_disk(self):
		status = 'error'
		if os.path.exists('/dev/ttyACM0') == True:
			print "otg test -> /dev/ttyACM0 found"
			status = 'ok'
			return status
		else:
			print "otg test --> /dev/ttyACM0 not found"
			status = 'error'
			return  status

	def __del__(self):
		self.__FileHand.close()

 
