#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from kafka import KafkaConsumer
from pgsql_database import postgresDatabaseHandler


def message_extraction(msg):
    """
    Extract the Metrics data from the kafka message
    :param msg: Kafka message
    """
    timestamp = msg.timestamp
    date_time = datetime.fromtimestamp(timestamp / 1e3)
    message = msg.value
    metrics = json.loads(message)
    hostname = metrics['hostname']
    data = metrics['system_metrics']
    metrics_values = []
    for key, value in data.items():
        metrics_values.append([date_time, hostname, key, value])
    return metrics_values


def insert_to_postgres_database(connection, data):
    """
    Insert the data from the message into the PostgreSQL table.
    :param connection: connection to the database
    :param data: List of lists of data to be inserted into PostgreSQL
    """
    cursor = connection.cursor()
    for val in data:
        cursor.execute("INSERT INTO system_metrics (datetime, hostname, metric, value) VALUES (%s, %s, %s, %s)", val)
        connection.commit()
    cursor.close()
    return


if __name__ == "__main__":
    topic = 'SystemMetrics'
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="kafka-270131d8-alxxthegeek-3ad2.aivencloud.com:11885",
        security_protocol="SSL",
        ssl_cafile="ca.pem",
        ssl_certfile="service.cert",
        ssl_keyfile="service.key",
        sasl_mechanism="PLAIN",
    )
    db = postgresDatabaseHandler()
    connection = db.connect()
    for msg in consumer:
        entries_for_database = message_extraction(msg)
        insert_to_postgres_database(connection, entries_for_database)
        print('Message saved to database')
