#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging


def init_logger(filename, level, name):
    # create a logging object
    logger = logging.getLogger()
    logger.setLevel(level)
    # format log file
    formatter = logging.Formatter('%(asctime)s %(levelname)s-%(filename)s: %(message)s')
    # create the logging file handler and format the log file
    fh = logging.FileHandler(filename, mode='a+')
    fh.setFormatter(formatter)
    # create logging print Stream
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    # logger object load the hander
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
