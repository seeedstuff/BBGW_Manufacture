import os
import sys
import  commands
def get_mac_addr():
    mac_addr = {'eth0':'00:11:22:33:44:55','eth1':'00:11:22:33:44:56'}
    for line in os.popen("/sbin/ifconfig"):
        if line[0:4] == 'wlan0':
            x = {'wlan0':line[-20:][0:17]}
            mac_addr.update(x)
        if line[0:4] == 'eth0':
            x = {'eth0':line[-20:][0:17]}
            mac_addr.update(x)
        if line[0:4] == 'eth1':
            x = {'eth1':line[-20:][0:17]}
            mac_addr.update(x)
    return  mac_addr

def do_shell_command(cmd):
    error = 'error'
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        return output
    else:
        error = 'ok'
        return  error

def init_ethernet():
    status = 'error'
    status = do_shell_command("ifconfig eth1 up")
    if status != 'ok':
        status = 'Please insert your usb ethernet card'
        return status

    status = do_shell_command('ifconfig eth0 up')
    if status != 'ok':
        status = 'ethernet test failed'
        return  status

    os.popen("ifconfig eth0 192.168.1.1 netmask 255.255.255.0")
    os.popen("ifconfig eth1 192.168.1.2 netmask 255.255.255.0")

    os.popen("route add 192.168.1.11 dev eth0")
    os.popen("route add 192.168.1.22 dev eth1")

    os.popen("arp -i eth0 -s 192.168.1.11 "+ get_mac_addr()['eth1'])
    os.popen("arp -i eth1 -s 192.168.1.22 "+ get_mac_addr()['eth0'])

    os.popen("iptables -t nat -F")
    os.popen("iptables -t nat -A POSTROUTING  -s 192.168.1.1  -d 192.168.1.11 -j SNAT --to-source        192.168.1.22")
    os.popen("iptables -t nat -A PREROUTING   -s 192.168.1.22 -d 192.168.1.11 -j DNAT --to-destination    192.168.1.2")
    os.popen("iptables -t nat -A POSTROUTING  -s 192.168.1.2  -d 192.168.1.22 -j SNAT --to-source        192.168.1.11")
    os.popen("iptables -t nat -A PREROUTING   -s 192.168.1.11 -d 192.168.1.22 -j DNAT --to-destination    192.168.1.1")

    return  status

def do_ethernet_test():
    a = 0
    result = 'ok'
    for line in os.popen("ping -c 3 -I 192.168.1.2 192.168.1.22"):
        a = line.find('%')
        if a != -1:
            if line[a - 3:a] != ', 0':
                result = 'error'
                return  result

    for line in os.popen("ping -c 3 -I 192.168.1.1 192.168.1.11"):
        a = line.find('%')
        if a != -1:
            if line[a - 3:a] != ', 0':
                result = 'error'
                return result
    return result
def do_ethernet_dhcp():
    os.popen("ifconfig eth0 up")
    os.popen("dhclient eth0")
    result = 'ok'
    for line in os.popen("ping -l 16 -c 3 192.168.31.1"):
        a = line.find('%')
        if a != -1:
            if line[a - 3:a] != ', 0':
                result = 'error'
                print line[a - 3:a]
                return  result
    return result
if __name__ == '__main__':
    if init_ethernet() != 'ok':
        print "init error"
    if do_ethernet_test() == 'ok':
        print "ethernet test ok!"

    else:
        print "ethernet test fail!"

