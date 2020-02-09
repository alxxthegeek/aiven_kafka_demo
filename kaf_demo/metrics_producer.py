#!/usr/bin/env python3

import sys
import logging
import logging.config
import configparser
import json
import logging
import metrics
import time
import threading

from kafka import KafkaProducer
from metrics import metrics
from socket import gethostname


def create_producer(host, port):
    producer = KafkaProducer(
        bootstrap_servers=f"{host}:{port}",
        sasl_mechanism="PLAIN",
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    return producer

def get_config():
    config_file = "../kaf_demo.cfg"
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except configparser.Error as err:
        print(err)
        logging.error("Error %s "), err
        sys.exit(1)
    prod_port = config.get('metrics_producer', 'port')
    prod_host = config.get('metrics_producer', 'host')
    prod_topic = config.get('metrics_producer', 'topic')
    return prod_host, prod_port, prod_topic


class Producer(threading.Thread):
    def __init__(self, config=get_config()):
        daemon = True
        print('starting')
        self.host, self.port, self.topic = config
        self.producer = create_producer(self.host, self.port)

    def run(self):
        while True:
            self.producer.send(self.topic, {"hostname": gethostname(), "system_metrics": metrics.create_metrics_json()})
            time.sleep(10)


if __name__ == "__main__":
    # Producer()
    Producer().run()


