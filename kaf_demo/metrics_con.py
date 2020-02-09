#!/usr/bin/env python3

import sys
import logging
import logging.config
import configparser
import json
import logging
import time
import threading
from kafka import KafkaConsumer



def create_consumer(host, port, topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=f"{host}:{port}",
        sasl_mechanism="PLAIN",
        value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    consumer.subscribe([topic])
    return consumer


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


class Consumer(threading.Thread):
    def __init__(self, config=get_config()):
        daemon = True
        print('starting')
        self.host, self.port, self.topic = config
        self.consumer = create_consumer(self.host, self.port, self.topic)

    def run(self):
        for message in self.consumer:
            message = message.value
            # collection.insert_one(message)
            # print('{} added to {}'.format(message, collection))
            print(f'Message is :{message}')


if __name__ == "__main__":
    Consumer()
    Consumer().run()


