#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.config
import configparser
import sys

class util(object):
    def __init__(self):
        self.config_file = "../kaf_demo.cfg"
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.config_file)
        except configparser.Error as err:
            print(err)
            logging.error("Error %s "), err
            sys.exit(1)
        self.info_log = self.config.get('Log', 'event_log')
        self.error_log = self.config.get('Log', 'error_log')
        self.debug_log = self.config.get('Log', 'debug_log')
        print('config')
        self.logging_start()

    def logging_start(self):
        '''Start logging'''
        self.create_log_file(self.debug_log, logging.DEBUG)
        self.create_log_file(self.info_log, logging.INFO)
        self.create_log_file(self.error_log, logging.ERROR)
        logging.getLogger('').setLevel(logging.DEBUG)
        return

    def create_log_file(self, filename, level):
        """Create log files , set handler and formating """
        handler = logging.handlers.RotatingFileHandler(filename)
        handler = logging.FileHandler(filename)
        handler.setLevel(level)
        handler.maxBytes = 256000000
        handler.backupCount = 10
        formatter = logging.Formatter(
            '%(asctime)s-15s [%(levelname)s] %(filename)s %(processName)s %(funcName)s %(lineno)d: %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)
        return