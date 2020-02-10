#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    Metrics Producer class
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
        """
        Create log files , set handler and formating

        :param filename: log file name
        :param level: Log level to set
        :return
        """
        handler = logging.handlers.RotatingFileHandler(filename)
        handler.setLevel(level)
        handler.maxBytes = 256000000
        handler.backupCount = 10
        formatter = logging.Formatter(
            '%(asctime)s-15s [%(levelname)s] %(filename)s %(processName)s %(funcName)s %(lineno)d: %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)
        return

    def create_producer(self, host, port):
        """
        Create the Kafka producer to send the messages

        :param host: Kafka host to connect to
        :param port: Port Kafka is running on
        :return client: returns the producer object
        """
        client = KafkaProducer(
            bootstrap_servers=f"{host}:{port}",
            security_protocol="SSL",
            ssl_cafile="ca.pem",
            ssl_certfile="service.cert",
            ssl_keyfile="service.key",
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        return client

    def send_message(self, topic, message):
        """
        Send the message to Kafka

        :param topic: Kafka topic to send message to
        :param message: Message to be sent(system metrics values)
        """
        self.metrics_producer.send(topic, message)
        self.metrics_producer.flush()
        print('Message sent')
        return

    def run(self):
        while True:
            message = {"hostname": gethostname(), "system_metrics": metrics.create_metrics_json()}
            self.send_message(self.topic, message)
            time.sleep(10)

        time.sleep(10)


if __name__ == "__main__":
    metrics_producer().run()
