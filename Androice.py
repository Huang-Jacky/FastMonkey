#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands


def check_devices():
    cmd = commands.getstatusoutput('adb devices')
    result = cmd[1].split('\n')
    if len(result) <= 2:
        print get_ctime() + 'There is no device connected currently, please check!'
        return False
    elif len(result) <= 3:
        phone_name = cmd[1].split('\n')[1].split('\t')[0]
        phone_status = cmd[1].split('\n')[1].split('\t')[1]
        print get_ctime() + 'Connected phone: ' + phone_name
        if phone_status != 'device':
            print get_ctime() + 'Phone status is {' + phone_status + '}, connection is limited!'
            print get_ctime() + 'Please replug the cable and confirm the notice of the phone!'
            return False
        else:
            return True
    else:
        for info in result:
            if info: print get_ctime() + '    ' + info
        print get_ctime() + 'More than one device/emulator, please check!'
        return False


def get_ctime(*timestamp):
    import time
    if timestamp:
        t = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(timestamp[0]/1000))
    else:
        t = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    return t
