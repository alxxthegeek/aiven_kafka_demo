
import concurrent.futures
import logging
import threading
import time
import metrics_consumer

from metrics_producer import Producer
#from metrics_prod import metrics_producer
#from metrics_con import Consumer
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
    # # prod = metrics_producer()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     #while True:
    #     executor.submit(con.run())
    #     executor.submit(prod.run())


    main()

