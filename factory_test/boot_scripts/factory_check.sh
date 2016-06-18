#!/bin/bash
interval=1
count=40
i=0

while [ $i -lt $count ]; do
    echo "start........"
    if [ -b /dev/sda ]; then
        echo "find sda....."
        if [ -b /dev/sda1 ]; then
            mkdir  /media/usb1
            sync
            mount /dev/sda1 /media/usb1
            sync
            if [ -d /media/usb1  ];then
                echo "hello"
            fi
            if [ -f /media/usb1/mac_addr.txt  ];then
                python /root/factory_test/BBG_produce.py
                umount -f /media/usb1
                rm -r /media/usb1
                break
            else
                umount -f /media/usb1
            fi
        else
            echo "find usb storage......"
            mkdir -p /media/usb
            mount /dev/sda  /media/usb
            if [ -f /media/usb1/mac_addr.txt  ];then
                python /root/factory_test/BBG_produce.py
                umount /media/usb
                rm -r /media/usb
                break
            else
                umount /media/usb
            fi
        fi
    fi
    if [ -b /dev/sdb ]; then
        if [ -b /dev/sdb1 ]; then
            mkdir -p /media/usb1
            mount /dev/sdb1 /media/usb1
            if [ -f /media/usb1/mac_addr.txt  ];then
                python /root/factory_test/BBG_produce.py
                umount -f /media/usb1
                rm -r /media/usb1
                break
            else
                umount -f /media/usb1
            fi
        else
            mkdir -p /media/usb1
            mount /dev/sdb /media/usb1
            if [ -f /media/usb1/mac_addr.txt  ];then
                python /root/factory_test/BBG_produce.py
                umount -f /media/usb1
                rm -r /media/usb1
                break
            else
                umount -f /media/usb1
            fi
        fi
    fi
    
    echo 255 > /sys/class/leds/beaglebone:green:usr0/brightness
    echo 255 > /sys/class/leds/beaglebone:green:usr1/brightness
    echo 255 > /sys/class/leds/beaglebone:green:usr2/brightness
    echo 255 > /sys/class/leds/beaglebone:green:usr3/brightness
    sleep $interval
    
    echo 0 > /sys/class/leds/beaglebone:green:usr0/brightness
    echo 0 > /sys/class/leds/beaglebone:green:usr1/brightness
    echo 0 > /sys/class/leds/beaglebone:green:usr2/brightness
    echo 0 > /sys/class/leds/beaglebone:green:usr3/brightness
    sleep $interval
    
    if [ $i -gt $count ]; then
        break;
    fi
done

