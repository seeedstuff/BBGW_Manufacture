import time
import pexpect
import subprocess
import sys
import os
import syslog

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

if __name__=="__main__":
    print "wifi test is :" + wifi_scan()
