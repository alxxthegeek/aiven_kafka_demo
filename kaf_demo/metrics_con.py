#!/usr/bin/env python3

import sys
import logging
import logging.config
import configparser
import json
import logging
import time
import threading
import metrics_consumer
from kafka import KafkaConsumer
from pgsql_database import postgres_database_handler



def create_consumer(host, port, topic):
    """
    Create Kafka message consumer

    :param host: Kafka host to connect to
    :param port: Port Kafka is running on
    :return consumer : returns the consumer object
    """
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=f"{host}:{port}",
        client_id="system-metrics1",
        security_protocol="SSL",
        ssl_cafile="ca.pem",
        ssl_certfile="service.cert",
        ssl_keyfile="service.key",
        value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    consumer.subscribe([topic])
    return consumer


def get_config():
    """
    Get the configuration file and read the values specified
    :return: returns a tuple of the host, port and topic.
    """
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
    """
    Consumer class to read message from Kafka Topic
    """
    def __init__(self, config=get_config()):
        daemon = True
        print('Starting Consumer')
        self.host, self.port, self.topic = config
        self.consumer = create_consumer(self.host, self.port, self.topic)
        self.db = postgres_database_handler()
        self.connection = postgres_database_handler().connect()

    def run(self):
        for message in self.consumer:
            entries_for_database = metrics_consumer.message_extraction(message)
            metrics_consumer.insert_to_postgres_database(self.connection, entries_for_database)
            print("\nMessage saved\n")


if __name__ == "__main__":
    con = Consumer()
    con.run()


