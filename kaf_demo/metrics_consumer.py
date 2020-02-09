#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from kafka import KafkaConsumer
from pgsql_database import postgres_database_handler


def message_extraction(msg):
    timestamp = msg.timestamp
    date_time = datetime.fromtimestamp(timestamp / 1e3)
    message = msg.value.decode("utf-8")
    metrics = json.loads(message)
    hostname = metrics['hostname']
    data = metrics['system_metrics']
    metrics_values = []
    for key, value in data.items():
        metrics_values.append([date_time, hostname, key, value])
    return metrics_values


def insert_to_postgres_database(connection, data):
    '''

    '''
    cursor = connection.cursor()
    for val in data:
        cursor.execute("INSERT INTO system_metrics (datetime, hostname, metric, value) VALUES (%s, %s, %s, %s)", val)
        connection.commit()
    cursor.close()
    return


consumer = KafkaConsumer('TutorialTopic')
db = postgres_database_handler()
connection = postgres_database_handler().connect()
for msg in consumer:
    print(msg)
    entries_for_database = message_extraction(msg)
    print(entries_for_database)
    print('\n')
    insert_to_postgres_database(connection, entries_for_database)
