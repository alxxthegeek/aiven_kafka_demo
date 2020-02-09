
import concurrent.futures
import metrics_con
import logging
import threading
import time
import json
from kafka import KafkaConsumer, KafkaProducer

from metrics_producer import Producer
from metrics_con import Consumer


def main():
    Consumer()
    Producer()
    threads = [
        #Consumer().run(),
        Producer().run()
    ]
    for t in threads:
        t.start()
        t.join()
    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:' +
               '%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    logging.getLogger().setLevel(logging.DEBUG)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     #     while True:
    #     #         executor.submit(Consumer().run())
    #     #         executor.submit(Producer().run())
    main()

