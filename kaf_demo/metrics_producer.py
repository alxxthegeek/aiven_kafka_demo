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
        security_protocol="SSL",
        ssl_cafile="ca.pem",
        ssl_certfile="service.cert",
        ssl_keyfile="service.key",
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
        print('Starting Producer')
        self.host, self.port, self.topic = config
        self.producer = create_producer(self.host, self.port)

    def run(self):
        while True:
            self.producer.send(self.topic, {"hostname": gethostname(), "system_metrics": metrics.create_metrics_json()})
            print('Message sent')
            time.sleep(10)


if __name__ == "__main__":
    # Producer()
    Producer().run()


