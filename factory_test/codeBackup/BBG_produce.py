import sys
import os
import binascii
import string
import time
import serial
import platform
import Ethenet_sing
import pins
from  ledstatus  import *
from fileModule import *
from  operate_eeprom import *
import mraa
import barcode_kbd
import multiprocessing
#from wifi_test import *
from bluetooth_test import *
import threading
import multiprocessing


'''
bluetooth_test_status = 'error'
def bluetooth_thread():
    global bluetooth_test_status
    if 'ok' == bluetooth_preInit():
        bl = Bluetoothctl()
        dist_mac_addr = os.popen("cat /media/usb1/mac_addr.txt").read()[:17]
        if 'ok' == bl.run_test(dist_mac_addr):
            bluetooth_test_status = 'ok'
    else:
        print "bluetooth test error"
'''

OK_PIN = 88  # "P9_42"
NG_PIN = 64  # "P9_18"
TEST_PIN = 60  # "P9_14"

ng_pin = mraa.Gpio(NG_PIN)
ok_pin = mraa.Gpio(OK_PIN)
test_pin = mraa.Gpio(TEST_PIN)

ng_pin.dir(mraa.DIR_OUT)
ok_pin.dir(mraa.DIR_OUT)
test_pin.dir(mraa.DIR_OUT)

ng_pin.write(0)
ok_pin.write(0)
test_pin.write(0)

def lock():
        print "lock!"
        while True:
            pass

def report_error():   
    t_error = ledstatus(7)
    t_error.led_clear = 1
    cnt = 0
    os.system("sync")
    os.system("sync")
    os.system("sync")
    while True:    
        ng_pin.write(0)        # GPIO.output(NG_PIN,GPIO.LOW)
        time.sleep(0.5)
        ng_pin.write(1)        # GPIO.output(NG_PIN,GPIO.HIGH)
        time.sleep(0.5)

#bluetooth_led_status = False
bluetooth_led_status = False
bluetooth_test_complete = "no"
def bluetooth_led():    
    global bluetooth_test_complete				#						
    while bluetooth_test_complete=="no":          #
#    while True:
        test_pin.write(0)
        time.sleep(.5)
        test_pin.write(1)
        time.sleep(.5)

def bluetooth_thread():    
    global bluetooth_led_status
    global bluetooth_test_complete
    t = threading.Thread(target=bluetooth_led)
    t.start()
    if os.path.exists('/usr/bin/bb-wl18xx-bluetooth_test')==True:
        print("the bb-wl18xx file exist. delte and copy")
        os.system("rm /usr/bin/bb-wl18xx-bluetooth_test -rf")
        time.sleep(0.1)
        os.system("cp /media/usb1/bb-wl18xx-bluetooth_test /usr/bin/ -rf")
        os.system("sync")
        time.sleep(0.1)
    else:
        print("the bb-wl18xx file not exist. just copy")
        os.system("cp /media/usb1/bb-wl18xx-bluetooth_test /usr/bin/ -rf")
        os.system("sync")

    os.system("chmod +x /usr/bin/bb-wl18xx-bluetooth_test")
    os.system("sync")
    time.sleep(0.1)    
    if 'ok' == bluetooth_preInit():
        bl = Bluetoothctl()
        dist_mac_addr = os.popen("cat /media/usb1/mac_addr.txt").read()[:17]
        if 'ok' == bl.run_test(dist_mac_addr):		
            bluetooth_test_complete = 'ok'
            print "bluetooth test pass and return ok"
        #    t.cancel()
            test_pin.write(1) 
            print "test led blink to on"
    else:
        print "bluetooth test error"

    print "bluetooth_led_status: ", bluetooth_led_status
    print "bluetooth_test_complete: ", bluetooth_test_complete

#bluetooth_test_t = multiprocessing.Process(target=bluetooth_thread)
#bluetooth_test_t.start()

def wifi_scan():
    status = 'error'
    f = file("./wifi.log", 'w')
    child = pexpect.spawn('connmanctl')
    print "wifi test,connmanctl-1"
    time.sleep(0.1)
    child.logfile = f
    out = child.expect(["Error getting VPN", "connmanctl>", pexpect.EOF, pexpect.TIMEOUT], timeout=2)
    time.sleep(0.1)
    if 3 == out:
        print "wifi test,connmanctl-2"
        child.sendline('connmanctl')
        out = child.expect(["Error getting VPN", "connmanctl>", pexpect.EOF, pexpect.TIMEOUT], timeout=2)

    print "wifi test,scan wifi"
    child.sendline("scan wifi")
    time.sleep(0.1)
    out = child.expect(["Scan completed for wifi", pexpect.EOF,pexpect.TIMEOUT],timeout=10)
    if 0 == out:
        print "wifi test,scan complete"
        child.sendline("services")
        time.sleep(0.1)
        out = child.expect(["wifi_", pexpect.EOF,pexpect.TIMEOUT],timeout=2)
        if 0 == out:
            print "scan wifi, scaned some signal"
            status = 'ok'
    else:
        print "wifi test,scan not complete. but also service"
        child.sendline("services")
        time.sleep(0.1)
        out = child.expect(["wifi_", pexpect.EOF,pexpect.TIMEOUT],timeout=2)
        if 0 == out:
            print "scan wifi, scaned some signal"
            status = 'ok'

    child.sendline("quit")
    return status


if __name__ == '__main__': 
    os.chdir('/root/factory_test')
    test_start = time.time()
    bluetooth_test_status = 'error'
#    bluetooth_test_complete = 'no'
    #bluetooth_test_complete = 'ok'       

    try:
        test_pin.write(1)    #GPIO.output(TEST_PIN,GPIO.HIGH)    
        ng_pin.write(1)        # GPIO.output(NG_PIN,GPIO.HIGH)
        time.sleep(0.5)
        ok_pin.write(0)        # GPIO.output(OK_PIN,GPIO.LOW)

        #id = 'BBGW16050000'
        #mac_addr = '2CF7F1060001'
        
        print  "start readID"
        id, mac_addr = barcode_kbd.readID() 
        report_file = id
        okfile = id
        #report_file = 'BBG115051111'
        ng_pin.write(0)        # GPIO.output(NG_PIN,GPIO.LOW)    
        print  report_file  
        if report_file != 'blank':
            report_file = "/root/factory_test/report/"+report_file+'_fail'+".txt"
            print "report_file: ", report_file
            okfile = "/root/factory_test/report/"+okfile+'_pass'+".txt"
            report = open(report_file,'w+')
        else:        
            report_error()
        report.write("That's BealgeBone Green  Seiral:" + report_file + " production test report!\n")
        report.write("if you have any questions about this test reports,Please conntact:www.seeedstudio.com\n")
        report.write("Software System:" + platform.linux_distribution()[0] + ' ' + platform.linux_distribution()[1] + '\n')
        report.write("Software Version:\n")

        versionfile = FM('version')
        report.write(versionfile.readFileText())

        report.write("Hardware test:\n")
        report.write("************************************************************************\n")
        # Close report file for saving it
        report.close()
 
        '''usb ethent port test'''
        os.system("echo \"-------------------------------USB Ethent test------------------------------\n\" >> " + report_file)
        rcv_str = subprocess.Popen("ifconfig eth0", shell=True, stdout=subprocess.PIPE).stdout.read()       
        if "Device not found" in rcv_str:
            os.system("echo \"USB Ethernet Port Test ------>[fail]\n\n\" >> " + report_file)            
            report_error()
        else:
            os.system("echo \"USB Ethernet Port Teset------>[pass]\n\n\" >> " + report_file)

#        P = multiprocessing.Process(target=wifi_scan)
#        P.start()
        
        '''DDR test'''        
        os.system("echo \"--------------------------------DDR test------------------------------\n\" >> " + report_file)
        ddr_file = FM('DDR')
        ddrsize = float(ddr_file.readMemory()[0:6])
        print  'ddrsize: ', ddrsize
        # if ddrsize > 507904:
        if ddrsize > 503904:            
            os.system("echo \"DDR size: ' + ddr_file.readMemory() + '------>[pass]\n\n\" >> " + report_file)
        else:            
            os.system("echo \"DDR size: ' + ddr_file.readMemory() + '------>[fail]\n\n\" >> " + report_file)            
            report_error()
        
        '''eMMC test'''        
        os.system("echo \"-------------------------------eMMC test------------------------------\n\" >> " + report_file)
        emmcsize = ddr_file.getemmcsize()
        if emmcsize > 3.6:            
            os.system("echo \"eMMc size: ' + '%f'%emmcsize + ' GB ------>[pass]\n\n\" >> " + report_file)
        else:            
            os.system("echo \"eMMc size: ' + '%f'%emmcsize + ' GB ------>[fail]\n\n\" >> " + report_file)
            report_error()    
        
        '''Debug Uart test'''
        print "Debug Uart test"        
        os.system("echo \"----------------------------Debug Uart test---------------------------\n\" >> " + report_file)

        if pins.check_debug_uart() == 'ok':            
            os.system("echo \"Debug Uart test   ------>[pass]\n\n\" >> " + report_file)
        else:            
            os.system("echo \"Debug Uart test   ------>[fail]\n\n\" >> " + report_file)
            report_error()    
            
        # Grove Uart test
        print "Grove Uart test"        
        os.system("echo \"----------------------------Grove Uart test---------------------------\n\" >> " + report_file)
        os.system("echo BB-UART2 > /sys/devices/platform/bone_capemgr/slots")
        os.system("sync")
        os.system("sync")
        os.system("sync")
        if pins.check_uart() == 'ok':            
            os.system("echo \"Grove Uart test   ------>[pass]\n\n\" >> " + report_file)
        else:            
            os.system("echo \"Grove Uart test   ------>[fail]\n\n\" >> " + report_file)
            report_error()
        
        # Grove I2C test
        print "Grove I2C test"        
        os.system("echo \"----------------------------Grove I2C test----------------------------\n\" >> " + report_file)
        if pins.check_i2c() == 'ok':                    
            os.system("echo \"Grove I2C test   ------>[pass]\n\n\" >> " + report_file)
        else:                      
            os.system("echo \"Grove I2C test   ------>[fail]\n\n\" >> " + report_file)
            report_error()
            
        
        # analog pins test
        print "analog pins test"        
        os.system("echo \"----------------------------analog pins test---------------------------\n\" >> " + report_file)
        status,result = pins.check_voltage()
        for v in result:            
            os.system("echo \""+ v + "\n\" >> " + report_file)
        if status == 'ok':            
            os.system("echo \"analog pins test   ------>[pass]\n\n\" >> " + report_file)
        else:            
            os.system("echo \"analog pins test   ------>[fail]\n\n\" >> " + report_file)
            report_error()
        
        
        # PMU test
        print "PMU test"        
        os.system("echo \"----------------------------PMU test---------------------------\n\" >> " + report_file)
        status,result = pins.check_power()
        for v in result:
            #report.write(v+'\n')
            os.system("echo \"" + v + "\n\" >> " + report_file)
        if status == 'ok':            
            os.system("echo \"PMU test   ------>[pass]\n\n\" >> " + report_file)
        else:            
            os.system("echo \"PMU test   ------>[fail]\n\n\" >> " + report_file)
            report_error()
        
        
        # GPIO test
        print "GPIO test"        
        os.system("echo \"------------------------------ GPIO test------------------------------\n\" >> " + report_file)
        badio = []        
        os.system("echo \"config-test-gpio overlay gpio-test\" >> " + report_file)
        badio = pins.check_io()
        if len(badio) != 0:            
            os.system("echo \"" + "gpio test ------>[fail]\n\n" + "\" >> " + report_file)
            for pin in badio:
                #report.write(str(pin) +'\n')            
                os.system("echo \"" + str(pin) + "\n" + "\" >> " + report_file)
            report_error()
        else:            
            os.system("echo \"" + "gpio test ------>[pass]\n\n" + "\" >> " + report_file)

        ''' 
        # OTG test
        print "OTG test"
        #report.write("-------------------------------OTG test-------------------------------\n")
        os.system("echo \"  \" >> " + report_file)
        if ddr_file.check_otg_disk() == 'ok':            
            os.system("echo \"OTG test   ------>[pass]\n\n\" >> " + report_file)
        else:            
            os.system("echo \"OTG test   ------>[fail]\n\n\" >> " + report_file)
            report.error()            
        ''' 
          
        # Start bluttoth test thread
        #bluetooth_test_t.start()

        # Net test
#        print "WiFi test"
        os.system("echo \"" + "-------------------------------WiFi test-------------------------------\n" + "\" >> " + report_file)
        wifiStatus = 'error'
        wifiStatus = wifi_scan()
                  
        if 'ok' == wifiStatus:
            os.system("echo \"WiFi test ------->[passed]\n\n\" >> " + report_file)    
        else:                    
            os.system("echo \"WiFi test ------->[fail]\n\n\" >> " + report_file)
            report_error()


        bluetooth_thread()

        os.system("echo \"************************************************************************\n\n\" >> " + report_file)
        time_use = str(time.time()-test_start) 
        os.system("echo \"" + "Test use time: " + time_use + "\n\n"  + "\" >> " + report_file)

        P8_43 = mraa.Gpio(43)    #GPIO.setup('P8_43', GPIO.IN)
        P8_43.dir(mraa.DIR_IN)
        ok_pin.dir(mraa.DIR_OUT)   #GPIO.setup(OK_PIN,GPIO.OUT)
        test_pin.dir(mraa.DIR_OUT)   #GPIO.setup(TEST_PIN,GPIO.OUT)
        
        
        test_pin.write(0)   #GPIO.output(TEST_PIN,GPIO.LOW)
        ok_pin.write(1)
        while True:
            if P8_43.read() == 0:
                os.system("echo \"" + "sd button test ok!" + "\" >> " + report_file)
                break

        '''eeprom test'''
        os.system("echo \"-------------------------------eeprom test------------------------------\n\" >> " + report_file)
        Myeeprom = eeprom()
        Myeeprom.dd_name_2_eeprom()
 
        name, version, serial, _mac_addr = Myeeprom.readBoardinfo()
        print name,version,serial,mac_addr        
        
        version = 'GW1A'
        serial = id        
                
        Myeeprom.writeBoardinfo(name,version,serial,mac_addr)
        name,version,serial,_mac_addr = Myeeprom.readBoardinfo()
        
        # Actually because of the struct style, mac_addr has 18 bytes
        _mac_addr = _mac_addr[:12]
       
        if serial == id and mac_addr == str(_mac_addr):            
            os.system("echo \"write board serial: ' + serial + '------>[pass]\n\n\" >> " + report_file)
            os.system("echo \"write board mac_addr: ' + '%s'%_mac_addr + '------>[pass]\n\n\" >> " + report_file)
            os.system("echo \"write board version: ' + '%s'%version + '------>[pass]\n\n\" >> " + report_file)
        else:            
            os.system("echo \"write board serial: ' + serial + '------>[fail]\n\n\" >> " + report_file)            
            os.system("echo \"write board mac_addr: ' + '%s'%_mac_addr + '------>[fail]\n\n\" >> " + report_file)            
            os.system("echo \"write board version: ' + '%s'%version + '------>[fail]\n\n\" >> " + report_file)            
            report_error()
           
        os.system("sync")
        os.system("mv "+report_file+" "+okfile)
        os.system("sync")
        os.system("sync")
        os.system("sync")

        ok_pin.write(0)    #GPIO.output(OK_PIN,GPIO.LOW)
    except Exception as e:        
        print e
        report_error()    

 


