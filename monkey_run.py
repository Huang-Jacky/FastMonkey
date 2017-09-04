#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os
import time
import commands
from Androice import check_devices
import thread
import logger

logger = logger.init_logger('./my_log.log', 'DEBUG', 'test')


class MyFrame(wx.Frame):
    delayDefault = "2"
    seedDefault = "5000000"
    executeNumDefault = "60000000"
    log_dir = "./"
    root_dir = os.getcwd()
    default_package = ['com.mobvista.sdk.demo']
    monkey_p = ""
    logcat_p = ""

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "FastMonkey", pos=(480, 25), size=(420, 700),
                          style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1)

        x_pos = 10
        x_pos1 = 180
        y_pos = 12
        y_delta = 40
        execute_mode = ["默认",
                        "忽略程序崩溃",
                        "忽略程序无响应",
                        "忽略安全异常",
                        "出错中断程序",
                        "本地代码导致的崩溃"
                        ]

        log_mode = ["简单", "普通", "详细"]
        execution_mode_default = execute_mode[0]

        menu_bar = wx.MenuBar()
        menu1 = wx.Menu()
        item1_save_log = wx.MenuItem(menu1, 1, '&SaveLog')
        item1_quit = wx.MenuItem(menu1, 2, '&Quit')
        item1_stop_and_analysis = wx.MenuItem(menu1, 3, '&StopLog')
        menu1.Append(item1_save_log)
        menu1.Append(item1_stop_and_analysis)
        menu1.Append(item1_quit)
        menu2 = wx.Menu()
        menu_bar.Append(menu1, "&File")
        menu_bar.Append(menu2, '&Help')
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.save_logcat, id=1)
        self.Bind(wx.EVT_MENU, self.on_quit, id=2)
        self.Bind(wx.EVT_MENU, self.build_fatal_log, id=3)

        wx.StaticText(panel, -1, "种子数:", pos=(x_pos, y_pos))
        self.seedCtrl = wx.TextCtrl(panel, -1, "", pos=(x_pos1, y_pos))
        self.seedCtrl.Bind(wx.EVT_KILL_FOCUS, self.valid_seed)
        # self.seedCtrl.SetFocus()

        wx.StaticText(panel, -1, "执行次数:", pos=(x_pos, y_pos + y_delta))
        self.executeNumCtrl = wx.TextCtrl(panel, -1, "", pos=(x_pos1, y_pos + y_delta))
        self.executeNumCtrl.Bind(wx.EVT_KILL_FOCUS, self.valid_num)

        wx.StaticText(panel, -1, "延时:", pos=(x_pos, y_pos + 2 * y_delta))
        self.delayNumCtrl = wx.TextCtrl(panel, -1, "", pos=(x_pos1, y_pos + 2 * y_delta))
        self.delayNumCtrl.Bind(wx.EVT_KILL_FOCUS, self.valid_delay)

        wx.StaticText(panel, -1, "执行方式:", pos=(x_pos, y_pos + 3 * y_delta))
        self.executeModeCtrl = wx.ComboBox(panel, -1, "", (x_pos1, y_pos + 3 * y_delta), choices=execute_mode,
                                           style=wx.CB_READONLY)

        self.checkListBox = wx.CheckListBox(panel, -1, (x_pos, y_pos + 4 * y_delta), (400, 350), [])

        y_pos_layout = y_pos + 14 * y_delta
        wx.StaticText(panel, -1, "日志输出等级:", pos=(x_pos, y_pos_layout - y_delta))
        self.logModeCtrl = wx.ComboBox(panel, -1, "", (x_pos1, y_pos_layout - y_delta), choices=log_mode,
                                       style=wx.CB_READONLY)

        self.readButton = wx.Button(panel, -1, "读取程序包", pos=(x_pos, y_pos_layout))
        self.Bind(wx.EVT_BUTTON, self.get_package_list, self.readButton)
        self.readButton.SetDefault()

        self.selectButton = wx.Button(panel, -1, "全部选择", pos=(x_pos + 120, y_pos_layout))
        self.Bind(wx.EVT_BUTTON, self.on_select_all, self.selectButton)
        self.selectButton.SetDefault()

        self.unSelectButton = wx.Button(panel, -1, "全部取消", pos=(x_pos + 120 * 2, y_pos_layout))
        self.Bind(wx.EVT_BUTTON, self.on_unselect, self.unSelectButton)

        self.defaultButton = wx.Button(panel, -1, "默认参数", pos=(x_pos, y_pos_layout + y_delta))
        self.Bind(wx.EVT_BUTTON, self.on_reset, self.defaultButton)
        self.defaultButton.SetDefault()

        self.quickButton = wx.Button(panel, -1, "一键Monkey", pos=(x_pos + 120, y_pos_layout + y_delta))
        self.Bind(wx.EVT_BUTTON, self.start_monkey, self.quickButton)
        self.quickButton.SetDefault()

        self.doButton = wx.Button(panel, -1, "开始Monkey", pos=(x_pos + 120 * 2, y_pos_layout + y_delta))
        self.Bind(wx.EVT_BUTTON, self.begin_monkey, self.doButton)
        self.doButton.SetDefault()

        self.stopButton = wx.Button(panel, -1, "停止Monkey", pos=(x_pos, y_pos_layout + 2 * y_delta))
        self.Bind(wx.EVT_BUTTON, self.stop_monkey, self.stopButton)
        self.stopButton.SetDefault()

    def on_quit(self, e):
        self.stop_monkey(e)
        self.Close()

    @staticmethod
    def input_check(value):
        if value == '':
            return True
        elif all(x in '0123456789' for x in value):
            if '.' in value:
                if value.count('.') == 1 and value[0] != '.' and value[-1] != '.':
                    return True
                else:
                    return False
            elif len(value) >= 1 and value[0] != '0':
                return True
            else:
                return False
        else:
            return False

    def valid_seed(self, event):
        value = self.seedCtrl.GetValue().strip()
        if self.input_check(value):
            if value != '':
                self.seedCtrl.SetValue(value)
        else:
            self.seedCtrl.SetValue(self.seedDefault)

    def valid_num(self, event):
        value = self.executeNumCtrl.GetValue().strip()
        if self.input_check(value):
            if value != '':
                self.executeNumCtrl.SetValue(value)
        else:
            self.executeNumCtrl.SetValue(self.executeNumDefault)

    def valid_delay(self, event):
        value = self.delayNumCtrl.GetValue().strip()
        if self.input_check(value):
            if value != '':
                logger.info('Delay_num = ' + value)
                self.delayNumCtrl.SetValue(value)
        else:
            self.delayNumCtrl.SetValue(self.delayDefault)

    def quick_monkey(self):
        self.quickButton.Disable()
        self.doButton.Disable()
        self.reset()
        self.start_cmd()

    def normal_monkey(self):
        self.quickButton.Disable()
        self.doButton.Disable()
        self.start_cmd()

    @staticmethod
    def start_new_thread(task):
        thread.start_new_thread(task, ())

    def start_monkey(self, event):
        self.start_new_thread(self.quick_monkey)

    def begin_monkey(self, event):
        self.start_new_thread(self.normal_monkey)

    def on_select_all(self, event):
        list_string = self.checkListBox
        count = list_string.GetCount()
        array = []
        for i in range(0, count):
            array.append(i)
        list_string.SetCheckedItems(array)

    def on_unselect(self, event):
        self.checkListBox.SetCheckedItems([])

    def on_reset(self, event):
        self.reset()

    def get_package_list(self, event):
        self.checkListBox.Clear()
        cmd = "adb shell ls data/data"
        result = commands.getoutput(cmd).split('\r')
        while '' in result:
            result.remove('')
        if len(result) > 1:
            for item in result:
                if item != "":
                    self.checkListBox.Append(item.strip())
                else:
                    self.checkListBox.Append(self.default_package)
        elif len(result) == 1:
            if 'Permission' in result[0]:
                logger.warn('Need ROOT Permission to access!')
                self.checkListBox.Append(self.default_package)
            else:
                logger.info(result[0])
                self.checkListBox.Append(result[0].strip())

    def reset(self):
        self.seedCtrl.SetValue(self.seedDefault)
        self.executeNumCtrl.SetValue(self.executeNumDefault)
        self.delayNumCtrl.SetValue(self.delayDefault)
        self.executeModeCtrl.SetSelection(0)
        self.logModeCtrl.SetSelection(2)

    def start_cmd(self):
        seed = self.seedCtrl.GetValue()
        execute_num = self.executeNumCtrl.GetValue()
        delay_num = self.delayNumCtrl.GetValue()
        # execute_mode = self.executeModeCtrl.GetValue()
        date = time.strftime('%Y%m%d%H%m%s', time.localtime(time.time()))
        list_string = self.checkListBox

        package_section = ""
        if list_string.CheckedStrings == 0:
            package_list = list_string.GetCheckedStrings()
        else:
            package_list = self.default_package
        logger.info("select package count:" + str(len(package_list)))
        for i in range(0, len(package_list)):
            logger.info(package_list)
            package = package_list[i]
            pack = package.strip('\r\n')
            package_section += (" -p " + pack)

        seed_section = " -s " + seed
        delay_section = " --throttle " + delay_num
        log_section = ""

        hard_key_section = ' --pct-anyevent 0'
        system_key_section = ' --pct-syskeys 0'
        activity_p_section = ' --pct-appswitch 0'

        log_level = self.logModeCtrl.GetSelection()
        if log_level == 0:
            log_section += " -v"
        elif log_level == 1:
            log_section += " -v -v"
        elif log_level == 2:
            log_section += " -v -v -v"

        mode_id = self.executeModeCtrl.GetSelection()
        mode = ["",
                " --ignore-crashes",
                " --ignore-timeouts",
                " --ignore-security-exceptions",
                " --ignore-native-crashes",
                " --monitor-native-crashes"]
        if mode_id == 1:
            execute_mode_section = mode[1]
        elif mode_id == 2:
            execute_mode_section = mode[2]
        elif mode_id == 3:
            execute_mode_section = mode[3]
        elif mode_id == 4:
            execute_mode_section = mode[4]
        elif mode_id == 5:
            execute_mode_section = mode[5]
        else:
            execute_mode_section = mode[1] + mode[2] + mode[3] + mode[4] + mode[5]

        # create monkey log dir ###############
        if not os.path.isdir('./MonkeyLog/'):
            os.mkdir('./MonkeyLog/')
        os.chdir('./MonkeyLog/')
        log_home = os.getcwd()
        log_name = "MonkeyLog_" + date
        os.mkdir(log_name)
        self.log_dir = os.path.join(log_home, log_name)
        logger.info(self.log_dir)
        os.chdir(self.log_dir)

        # run monkey and record monkey log ################
        monkey_cmd = "adb shell monkey"
        monkey_cmd = monkey_cmd + delay_section + seed_section + package_section + hard_key_section\
                     + system_key_section + activity_p_section + log_section + execute_mode_section
        monkey_cmd = monkey_cmd + " " + execute_num + " > monkey.log"
        logger.info(monkey_cmd)
        commands.getstatusoutput(monkey_cmd)
        logger.info('#' * 15 + ' Monkey finish '+'#' * 15)
        os.chdir(self.root_dir)
        self.quickButton.Enable()
        self.doButton.Enable()

    @staticmethod
    def build_log(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.find("logcat.txt") == 0:
                    log_f = f.strip()
                    os.chdir(root)
                    if log_f != "":
                        grep_cmd = "grep -Eni -B30 -A30 'FATAL|error|exception|system.err|androidruntime' " + log_f + \
                                   " > " + log_f.split('.')[0] + str(time.time()) + "_fatal.log"
                        os.system(grep_cmd)
        logger.info('#' * 15 + ' Log build finish ' + '#' * 15)

    def save_logcat(self, event):
        os.chdir(self.log_dir)
        self.start_new_thread(self.save_log)

    def stop_logcat(self, event):
        if check_devices():
            self.logcat_p = commands.getoutput('adb shell ps | grep logcat')
            if self.logcat_p != "":
                for i in self.logcat_p.strip().split('\r'):
                    pid = i.split(' ')[5]
                    logger.info('Logcat pid = ' + pid)
                    commands.getoutput('adb shell kill %s' % pid)
            else:
                logger.info('No logcat process running!')

    @staticmethod
    def clear_logcat():
        cmd = 'adb logcat -c'
        commands.getstatusoutput(cmd)

    def save_log(self):
        self.clear_logcat()
        cmd = 'adb logcat -v time > logcat.txt'
        commands.getstatusoutput(cmd)

    def build_fatal_log(self, event):
        self.stop_logcat(event)
        self.build_log(self.log_dir)

    def check_monkey(self, event):
        if check_devices():
            self.monkey_p = commands.getoutput('adb shell ps | grep monkey')
            if self.monkey_p != "":
                pid = self.monkey_p.split(' ')[5]
                logger.info('Monkey pid = ' + pid)
                return True, pid
            else:
                logger.info('No monkey process running!')
                return False

    def stop_monkey(self, event):
        monkey_event = self.check_monkey(event)
        if monkey_event:
            pid = monkey_event[1]
            commands.getoutput('adb shell kill %s' % pid)
            self.stop_logcat(event)
        self.quickButton.Enable()
        self.doButton.Enable()
        os.chdir(self.root_dir)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
