import time
import pexpect
import subprocess
import sys
import os
import syslog

def bluetooth_preInit():
    status = 'error'
    print "bluetooth_preInit!"
    # Initialize bluetooth device

    child = pexpect.spawn("bb-wl18xx-bluetooth_test")
    time.sleep(5)
    out = child.expect(["Device setup complete", "Can't initialize device: Success", "Initialization timed out",  pexpect.EOF])
    print "bb-wl18xx-bluetooth result: ", out 
    if 2 == out:
        child = pexpect.spawn("bb-wl18xx-bluetooth_test")
        time.sleep(5)
        out = child.expect(["Device setup complete", "Can't initialize device: Success", "Initialization timed out", pexpect.EOF])
        print "bb-wl18xx-bluetooth_test result: ", out
        if 1 < out:
            return status

    os.system("rm /var/lib/bluetooth/1?:2* -rf")
    os.system("rm /var/lib/bluetooth/1?:3* -rf")
    os.system("rm /var/lib/bluetooth/1?:4* -rf")
    os.system("rm /var/lib/bluetooth/1?:5* -rf")
    os.system("rm /var/lib/bluetooth/1?:6* -rf")
    os.system("rm /var/lib/bluetooth/1?:7* -rf")
    os.system("rm /var/lib/bluetooth/1?:8* -rf")
    os.system("rm /var/lib/bluetooth/1?:9* -rf")
    os.system("rm /var/lib/bluetooth/1?:A* -rf")
    os.system("rm /var/lib/bluetooth/1?:B* -rf")
    os.system("rm /var/lib/bluetooth/1?:C* -rf")
    os.system("rm /var/lib/bluetooth/1?:D* -rf")
    os.system("rm /var/lib/bluetooth/1?:E* -rf")
    os.system("rm /var/lib/bluetooth/1?:F* -rf")
    os.system("rm /var/lib/bluetooth/1?:0* -rf")

    os.system("rm /var/lib/bluetooth/1A* -rf")
    os.system("rm /var/lib/bluetooth/1B* -rf")
    os.system("rm /var/lib/bluetooth/1C* -rf")
    os.system("rm /var/lib/bluetooth/1D* -rf")
    os.system("rm /var/lib/bluetooth/1E* -rf")
    os.system("rm /var/lib/bluetooth/1F* -rf")
    os.system("rm /var/lib/bluetooth/2* -rf")
    os.system("rm /var/lib/bluetooth/3* -rf")
    os.system("rm /var/lib/bluetooth/4* -rf")
    os.system("rm /var/lib/bluetooth/5* -rf")
    os.system("rm /var/lib/bluetooth/6* -rf")
    os.system("rm /var/lib/bluetooth/7* -rf")
    os.system("rm /var/lib/bluetooth/8* -rf")
    os.system("rm /var/lib/bluetooth/9* -rf")
    os.system("rm /var/lib/bluetooth/A* -rf")
    os.system("rm /var/lib/bluetooth/B* -rf")
    os.system("rm /var/lib/bluetooth/C* -rf")
    os.system("rm /var/lib/bluetooth/D* -rf")
    os.system("rm /var/lib/bluetooth/E* -rf")
    os.system("rm /var/lib/bluetooth/F* -rf")
    time.sleep(0.2)
    results = os.popen("ls /var/lib/bluetooth/").read()
    print "len(results): ", len(results)
    if 18 == len(results):
        status = 'ok'        
    return status

class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass


class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):                        
        f = file("./plog.out", 'w')
        # Start to open bluetoothctl
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl")
        
        # TO-DO
        # If run bluetoothctl and can't get beaglebone MAC address, then reinitialize again
        
        self.child.logfile = f                                                   
            
    def __del__(self):
        self.child.sendline("quit")
        # print self.child.before
        self.child
        print "del function"
        
    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n")



    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address, 2)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success



#    def run_test(self,dist_mac_addr = "78:09:73:C8:90:C7"):
    def run_test(self,dist_mac_addr = "52:4E:79:28:67:3C"):
        count =4
        status = 'error'   
        while count > 0 :
            print "connect to[1] : " + dist_mac_addr    
            self.child.sendline("connect " + dist_mac_addr)
            time.sleep(1)
            results = self.child.expect(["Connection successful", "Fail", "org.bluez.Error.Failed", pexpect.EOF,pexpect.TIMEOUT], timeout=10)
            print "connect speaker result: ",results
            if 0 < results:
                print "test whether connect ok?"
                time.sleep(4)
                self.child.sendline("info " + dist_mac_addr)
                time.sleep(1)
                results = self.child.expect(["Connected: yes", "Connected: no", pexpect.EOF,pexpect.TIMEOUT], timeout=5)
                if results > 0:
                    count = count -1
                else:
                    count = 0
            else:
                count = 0
        time.sleep(0.5)
        if dist_mac_addr=="51:91:E2:BF:AE:47" :     
            os.system("mpg123 /root/factory_test/music/unit1.mp3")
        elif dist_mac_addr=="49:7A:10:6F:2D:D4":
            os.system("mpg123 /root/factory_test/music/unit2.mp3")
        elif dist_mac_addr=="EF:50:7B:BD:C8:16":    
            os.system("mpg123 /root/factory_test/music/unit3.mp3")
        elif dist_mac_addr=="3A:6B:13:A0:32:B6":
            os.system("mpg123 /root/factory_test/music/unit4.mp3")
        elif dist_mac_addr=="78:09:73:C8:77:50":     
            os.system("mpg123 /root/factory_test/music/unit5.mp3")
        elif dist_mac_addr=="FC:CD:B3:39:96:66":
            os.system("mpg123 /root/factory_test/music/unit6.mp3")
        elif dist_mac_addr=="9F:9E:E3:E5:44:86":    
            os.system("mpg123 /root/factory_test/music/unit7.mp3")
        elif dist_mac_addr=="78:09:73:C8:90:C7":
            os.system("mpg123 /root/factory_test/music/unit8.mp3")
        elif dist_mac_addr=="59:38:43:7C:64:92":     
            os.system("mpg123 /root/factory_test/music/unit9.mp3")
        elif dist_mac_addr=="52:4E:79:28:67:3C":
            os.system("mpg123 /root/factory_test/music/unit10.mp3")
        time.sleep(1)
        self.child.sendline("disconnect " + dist_mac_addr)
        status = 'ok'
        time.sleep(1.5)                    
        return status


   

if __name__ == "__main__":
    if 'ok' == bluetooth_preInit():
        bl = Bluetoothctl()
        result = bl.run_test()
        print "bluetooth test result: ", result
    else:
        print "error"  

        

 

