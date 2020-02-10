import concurrent.futures
import logging
import time
import threading

from metrics_con import Consumer
from metrics_producer import Producer
from util import util


def main():
    threads = [
        Consumer(),
        Producer()
    ]
    for t in threads:
        t.run()
        t.join()
    time.sleep(10)


if __name__ == "__main__":
    util()
    logging.getLogger().setLevel(logging.DEBUG)
    # con = Consumer()
    # prod = Producer()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     while True:
    #     executor.submit(con.run())
    #     executor.submit(prod.run())

    main()
