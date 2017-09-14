#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import logger
import os

log = logger.Log('./my_log.log', 'INFO', 'Androice')
screen_shot_path = os.path.join(os.getcwd(), 'screenshot')


def check_devices():
    cmd = commands.getstatusoutput('adb devices')
    result = cmd[1].split('\n')
    if len(result) <= 2:
        log.warn('There is no device connected currently, please check!')
        return False
    elif len(result) <= 3:
        phone_name = cmd[1].split('\n')[1].split('\t')[0]
        phone_status = cmd[1].split('\n')[1].split('\t')[1]
        log.info('Connected phone: ' + phone_name)
        if phone_status != 'device':
            log.warn('Phone status is {' + phone_status + '}, connection is limited!')
            log.warn('Please replug the cable and confirm the notice of the phone!')
            return False
        else:
            return True
    else:
        for info in result:
            if info: log.info('    ' + info)
        log.info('More than one device/emulator, please check!')
        return False


def get_ctime(*timestamp):
    import time
    if timestamp:
        t = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(timestamp[0]/1000))
    else:
        t = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    return t


def take_screen_shot(file_name, save_path=screen_shot_path):
    if check_devices():
        cmd = commands.getstatusoutput('adb shell /system/bin/screencap -p /sdcard/%s.png' % file_name)
        if cmd[0] == 0:
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            commands.getstatusoutput('adb pull /sdcard/%s.png %s' % (file_name, save_path))
            if os.path.exists(save_path + '/' + file_name + '.png'):
                log.info('Take screen shot done! Saved at %s.png' % (save_path + '/' + file_name))
            else:
                log.warn('Save screen shot failed!')
        else:
            log.warn('Take screen shot failed!')

