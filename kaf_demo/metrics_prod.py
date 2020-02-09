#!/usr/bin/env python3

import configparser
import json
import logging
import logging.config
import sys
import time
from kafka import KafkaProducer
from metrics import metrics
from socket import gethostname


class metrics_producer(object):
    '''
    Metrics Producer
    '''

    def __init__(self):
        self.config_file = "../kaf_demo.cfg"
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.config_file)
        except configparser.Error as err:
            print(err)
            logging.error("Error %s "), err
            sys.exit(1)
        self.port = self.config.get('metrics_producer', 'port')
        self.host = self.config.get('metrics_producer', 'host')
        self.topic = self.config.get('metrics_producer', 'topic')
        print(f" topic is {self.topic}")

        self.info_log = self.config.get('Log', 'event_log')
        self.error_log = self.config.get('Log', 'error_log')
        self.debug_log = self.config.get('Log', 'debug_log')
        self.logging_start()
        self.hostname = gethostname()
        self.metrics_producer = self.create_producer(self.host, self.port)



    def logging_start(self):
        '''Start logging'''
        self.create_log_file(self.debug_log, logging.DEBUG)
        self.create_log_file(self.info_log, logging.INFO)
        self.create_log_file(self.error_log, logging.ERROR)
        logging.getLogger('').setLevel(logging.DEBUG)
        return

    def create_log_file(self, filename, level):
        '''

        '''
        '''Create log files , set handler and formating '''
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

    def create_producer(self, host, port):
        '''

        '''
        client = KafkaProducer(
            bootstrap_servers=f"{host}:{port}",
            sasl_mechanism="PLAIN",
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        return client

    def send_message(self, topic, message):
        self.metrics_producer.send(topic, message)
        self.metrics_producer.flush()
        return

    def run(self):
        while True:
            message = {"hostname": gethostname(), "system_metrics": metrics.create_metrics_json()}
            self.send_message(self.topic, message)
            time.sleep(10)

        time.sleep(10)


if __name__ == "__main__":
    # metrics_producer()
    metrics_producer().run()
