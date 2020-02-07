#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer('TutorialTopic')
for msg in consumer:
    print(msg)
