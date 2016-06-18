import mraa
import subprocess
import sys, time, signal
import math
import serial
import struct
import os
import threading
#from oled96x96 import *

#oled = OLED96x96()

class duait():
    def __init__(self):
        self.istesting = 1
        '''
        ret = os.path.exists('/dev/ttyUSB0')
        if ret != True:
            oled.line = 5
            oled.myPrint('No', 'USB0')
        ret = os.path.exists('/dev/ttyO0')
        if ret != True:
            oled.line = 5
            oled.myPrint('No', 'ttyO0')
        '''
        self.uart = serial.Serial(port = "/dev/ttyUSB0", baudrate=115200, timeout=.7)
        self.uart.flush()
        self.uarto = serial.Serial(port = "/dev/ttyO0", baudrate=115200, timeout=.7)
        self.uarto.flush()
        #self.t = threading.Thread(target=self.write_a)
        #self.t.start()
    def write_a(self):
        while True:
            self.uarto.write('a')
            if self.istesting == 0:
                break
            time.sleep(0.02)

    def read_a(self):
        cnt = 0
        status = 'error'
        while cnt < 250:
            ch = self.uart.read(1)
            if  ch == 'a':
                self.istesting = 0
                status = 'ok'
                break
            print ch
            time.sleep(0.01)
            cnt = cnt + 1
        self.istesting = 0
        return  status
def check_debug_uart():
    uart = duait()
    count = 20
    while count > 0:
        uart.uarto.write("a")
        uart.uarto.write("a")
        uart.uarto.write("a")
        uart.uarto.write("a")
        time.sleep(0.1)
        out = uart.uart.read()
        if out == 'a':
            return 'ok'
        count = count - 1

class GPS:
    #The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
    inp=[]
    # Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
    GGA=[]

    def __init__(self):
        self.ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
        self.ser.flush()
        self.cnt = 0
    #Read data from the GPS
    def read(self):
        while True:
            GPS.inp=self.ser.readline()
            if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
                break
            if self.cnt > 10 :
                break
            self.cnt = self.cnt + 1
            time.sleep(0.3)
        #
        # try:
        #     ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))    #Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
        #     GPS.inp=GPS.inp[ind:]
        #     print  GPS.inp
        # except ValueError:
        #     print "gps error"

        GPS.GGA=GPS.inp.split(",")    #Split the stream into individual parts
        return [GPS.GGA]

    #Split the data into individual elements
    def vals(self):
        time=GPS.GGA[1]
        lat=GPS.GGA[2]
        lat_ns=GPS.GGA[3]
        long=GPS.GGA[4]
        long_ew=GPS.GGA[5]
        fix=GPS.GGA[6]
        sats=GPS.GGA[7]
        alt=GPS.GGA[9]
        return [time,fix,sats,alt,lat,lat_ns,long,long_ew]

class ITG3200():
    #global bus
    def __init__(self):
        self.GYRO_ADDRESS=0x68
        # ITG3200 Register Defines
        self.ITG3200_WHO=0x00
        self.ITG3200_SMPL=0x15
        self.ITG3200_DLPF=0x16
        self.ITG3200_INT_C=0x17
        self.ITG3200_INT_S=0x1A
        self.ITG3200_TMP_H=0x1B
        self.ITG3200_TMP_L=0x1C
        self.ITG3200_GX_H=0x1D
        self.ITG3200_GX_L=0x1E
        self.ITG3200_GY_H=0x1F
        self.ITG3200_GY_L=0x20
        self.ITG3200_GZ_H=0x21
        self.ITG3200_GZ_L=0x22
        self.ITG3200_PWR_M=0x3E

        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        self.bus = mraa.I2c(1)
        self.bus.address(self.GYRO_ADDRESS)
        
    def write_byte_data(self, reg, data):
        return self.bus.writeReg(reg, data)
    
    def read_byte_data(self, reg):
        return self.bus.readReg(reg)

# ********************************************************************
# Function: Initialization for ITG3200.
    def init(self):
        self.write_byte_data(self.ITG3200_PWR_M, 0x80)
        self.write_byte_data(self.ITG3200_SMPL, 0x00)
        self.write_byte_data(self.ITG3200_DLPF, 0x18)

    def read(self, addressh, addressl):
        t_data = self.read_byte_data(addressh)
        data = t_data << 8
        data |= self.read_byte_data(addressl)
        return data

# Function: Get the temperature from ITG3200 that with a on-chip
#            temperature sensor.
    def getTemperature(self):
        temp = self.read(self.ITG3200_TMP_H, self.ITG3200_TMP_L)
        temperature = 35 + (temp + 13200) / 280
        return temperature

# Function: Get the contents of the registers in the ITG3200
#           so as to calculate the angular velocity.
    def getXYZ(self):
        x = self.read(self.ITG3200_GX_H,self.ITG3200_GX_L) + self.x_offset
        y = self.read(self.ITG3200_GY_H,self.ITG3200_GY_L) + self.y_offset
        z = self.read(self.ITG3200_GZ_H,self.ITG3200_GZ_L) + self.z_offset
        return x, y, z
# Function: Get the angular velocity and its unit is degree per second.
    def getAngularVelocity(self):
        x,y,z = self.getXYZ()
        ax = x/14.375
        ay = y/14.375
        az = z/14.375

        return ax, ay, az

    def zeroCalibrate(self, samples, sampleDelayMS):
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        x_offset_temp = 0
        y_offset_temp = 0
        z_offset_temp = 0
        x,y,z = self.getXYZ()
        for i in range(samples):
            time.sleep(sampleDelayMS/1000.0)
            x,y,z = self.getXYZ()
            x_offset_temp += x
            y_offset_temp += y
            z_offset_temp += z
        #print "offet_temp ", x_offset_temp, x_offset_temp, x_offset_temp
        self.x_offset = abs(x_offset_temp)/samples
        self.y_offset = abs(y_offset_temp)/samples
        self.z_offset = abs(z_offset_temp)/samples
        if x_offset_temp > 0:
            self.x_offset = -self.x_offset
        if y_offset_temp > 0:
            self.y_offset = -self.y_offset
        if z_offset_temp > 0:
            self.z_offset = -self.z_offset


def check_uart():
    status = 'error'
    os.system("echo BB-UART2 > /sys/devices/platform/bone_capemgr/slots")
    os.system("sync")
    os.system("sync")
    os.system("sync")    
    status = 'error'
    ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
    ser.timeout = 2
    ser.write("AT")
    ret = ser.read(2)    
    if "OK" == ret:
        status = "ok"

    return status

def check_i2c():
    status = 'error'
    gyro = ITG3200()
    try:
        gyro.init()
    except:
        status = 'error'
        return status
    gyro.zeroCalibrate(5, 5)
    time.sleep(2)
    cnt = 0
    while cnt < 5:
        if gyro.getTemperature() > 0:
            status = 'ok'
            break
        cnt = cnt + 1
        time.sleep(0.5)
    return  status

def check_voltage():
    ain0 = mraa.Aio(0)
    ain1 = mraa.Aio(1)
    ain2 = mraa.Aio(2)
    ain3 = mraa.Aio(3)
    ain4 = mraa.Aio(4)
    ain5 = mraa.Aio(5) 
    ain6 = mraa.Aio(6)
    
    times = 100
    sum = 0
    values = []
    
    os.system("echo 59 > /sys/class/gpio/export")
    os.system("echo out > /sys/class/gpio/gpio59/direction")
    os.system("echo 1 > /sys/class/gpio/gpio59/value")
    os.system("echo 117 > /sys/class/gpio/export")
    os.system("echo in > /sys/class/gpio/gpio117/direction")           
    
    # Read GPIO3_21 for 100 times, values HIGH should not less than 30 
    while times:
        times = times - 1
        values.append(os.popen("cat  /sys/class/gpio/gpio117/value").read())

    for i in values:
        sum += int(i)
    print "sum: ", sum
    if sum < 30:
        print "GPIO3_21 check fail!"
    else:
        print "GPIO3_21 check ok!"
        
    
    VOLTAGES = [["AIN0", 1.50, 1.80, ain0],
                ["AIN2", 0.85, 0.95, ain2],
                ["AIN4", 0.90, 1.30, ain4],
                ["AIN6", 1.42, 1.58, ain6],
                ["AIN1", 1.04, 1.16, ain1], # VDD_3V3B / 3
                ["AIN3", 1.40, 1.75, ain3], # VDD_5V   / 3
                ["AIN5", 1.40, 1.80, ain5]] # SYS_5V   / 3
                
    # ADC.setup()
    result = []
    status = 'ok'
    for v in VOLTAGES:
        ain = v[3].read()/1024.0*1.8    #ain = ADC.read(v[0])*1.8        
        #print ain
        if ain < v[1] or ain > v[2]:
            result.append('%f (%s) is out of range: %f ~ %f.' % (ain, v[0], v[1], v[2]))
            status = 'error'
        else:
            result.append('%f (%s) is in of range: %f ~ %f.' % (ain, v[0], v[1], v[2]))    
    return  status,result

def check_io(): 
    #Group1
    P8_7 = mraa.Gpio(7)
    P8_9 = mraa.Gpio(9)
    P8_13 = mraa.Gpio(13)
    P8_27 = mraa.Gpio(27)
    P8_29 = mraa.Gpio(29)
    P8_35 = mraa.Gpio(35)
    P8_36 = mraa.Gpio(36)
    P8_37 = mraa.Gpio(37)
    P8_40 = mraa.Gpio(40)
    P9_13 = mraa.Gpio(46+13)
    P9_23 = mraa.Gpio(46+23)
    P9_26 = mraa.Gpio(46+26)
    P9_27 = mraa.Gpio(46+27)
    
    #Group2
    P8_8 = mraa.Gpio(8)
    P8_10 = mraa.Gpio(10)
    P8_19 = mraa.Gpio(19)
    P8_28 = mraa.Gpio(28)
    P8_30 = mraa.Gpio(30)
    P8_32 = mraa.Gpio(32)
    P8_33 = mraa.Gpio(33)
    P8_34 = mraa.Gpio(34)
    P8_38 = mraa.Gpio(38)
    P8_39 = mraa.Gpio(39)
    P9_11 = mraa.Gpio(46+11)
    P9_15 = mraa.Gpio(46+15)
    P9_17 = mraa.Gpio(46+17)
    P9_24 = mraa.Gpio(46+24)
    P9_42 = mraa.Gpio(46+42)
    
    #Group3
    P8_31 = mraa.Gpio(31)
    P8_42 = mraa.Gpio(42)
    
    IO_GROUP1 = [P8_7,P8_9,P8_13,P8_27,P8_29,
                 P8_35,P8_36,P8_37,P8_40,P9_13,
                 P9_23,P9_26,P9_27]
                 
    IO_GROUP2 = [P8_8,P8_10,P8_19,P8_28,P8_30,
                 P8_32, P8_33,P8_34,P8_38,P8_39,P9_11,
                 P9_15,P9_17,P9_42]
                 
    IO_GROUP3 = [P8_31, P8_42]
    
    io_group1 = ['P8_7','P8_9','P8_13','P8_27','P8_29',
                 'P8_35','P8_36','P8_37','P8_40', 'P9_13',
                 'P9_23','P9_26','P9_27']

    io_group2 = ['P8_8','P8_10','P8_19','P8_28','P8_30',
                 'P8_32','P8_33','P8_34','P8_38','P8_39',
                 'P9_11','P9_15','P9_17','P9_42']

    io_group3 = ['P8_31','P8_42']    
    
    
    badio = []
    IO_GROUP1[0].dir(mraa.DIR_OUT)     #GPIO.setup(IO_GROUP1[0], GPIO.OUT)
    for pin in IO_GROUP1[1:]:
        pin.dir(mraa.DIR_IN)     #GPIO.setup(pin, GPIO.IN)
    IO_GROUP1[0].write(1)     #GPIO.output(IO_GROUP1[0], GPIO.HIGH)

    IO_GROUP2[0].dir(mraa.DIR_OUT)       #GPIO.setup(IO_GROUP2[0], GPIO.OUT)
    for pin in IO_GROUP2[1:]:
        pin.dir(mraa.DIR_IN)        #GPIO.setup(pin, GPIO.IN)
    IO_GROUP2[0].write(0)        #GPIO.output(IO_GROUP2[0], GPIO.LOW)

    IO_GROUP3[0].dir(mraa.DIR_OUT)       #GPIO.setup(IO_GROUP3[0], GPIO.OUT)
    for pin in IO_GROUP3[1:]:
        pin.dir(mraa.DIR_IN)        #GPIO.setup(pin, GPIO.IN)
    IO_GROUP3[0].write(1)        #GPIO.output(IO_GROUP3[0], GPIO.HIGH)

    for pin in IO_GROUP1[1:]:
        if pin.read() != 1:      #if GPIO.input(pin) != GPIO.HIGH:
            badio.append(io_group1[IO_GROUP1.index(pin)])


    for pin in IO_GROUP2[1:]:
        if pin.read() != 0:      #if GPIO.input(pin) != GPIO.LOW:
            badio.append(io_group2[IO_GROUP2.index(pin)])


    for pin in IO_GROUP3[1:]:
        if pin.read() != 1:      #if GPIO.input(pin) != GPIO.HIGH:
            badio.append(io_group3[IO_GROUP3.index(pin)])

    return badio
    
'''
def check_power_ex():
    import powerstatus
    
    powerstatus.show_reg(powerstatus.PGOOD, "PGOOD", powerstatus.PGOOD_LABELS)
    status = powerstatus.query(powerstatus.PGOOD)
'''

# display value of each bit in the register, along with its label
def describe_bits(val,labels):
    result = []
    for x in range(0,len(labels)):
        if(not labels[x]): # skip None labels
            continue
        msk = 1<<x
        result.append("%s = %d"%(labels[x],(val&msk)!=0))
    return result
 
def check_power():
    result = []
    isok = 'ok'
    STATUS_LABELS = ["Push Button", None, "USB Power", "AC Power"] # skip the rest
    PGOOD_LABELS = ["LDO2 power-good","LDO1 power-good","DCDC3 power-good","DCDC2 power-good","DCDC1 power-good", "LDO4 power-good","LDO3 power-good"]
    
    pgood = int(subprocess.check_output(['i2cget', '-y' ,'-f', '0', '0x24', '0xC']).strip(), 16)
    status = int(subprocess.check_output(['i2cget', '-y' ,'-f', '0', '0x24', '0xA']).strip(), 16)
    
    result = describe_bits(pgood, PGOOD_LABELS)
    #describe_bits(status, STATUS_LABELS)
    if pgood != 0x7F:
        isok = 'error'
    
    return isok,result
    
if __name__ == '__main__':
    #print "check_power: ", check_power()
    #print "check_voltage: ", check_voltage()    
    #print "check_i2c: ", check_i2c()
    #print "check_io: ", check_io()    
    #print "check_uart: ", check_uart()
    print "check_debug", check_debug_uart()
