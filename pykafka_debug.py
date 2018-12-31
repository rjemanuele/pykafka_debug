import signal
import os
import json
import sys
import time
from pykafka import KafkaClient
import argparse
import logging

def term_handler(signum, frame):
    global running
    running = False

class PyKafka_Debug():
    def __init__(self):
        pass

    def run(self):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)
        self.options = parser.parse_args()
        self.handle()

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            default=False,
            action='store_true',
            dest='debug',
            help='debug',
        )
        parser.add_argument(
            '--test',
            default=False,
            action='store_true',
            dest='test',
            help='test mode without kafka',
        )

    def handle(self):
        if self.options.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig()

        if not self.options.test:
            try:
                kafka_hosts = os.environ['KAFKA_HOSTS']
                kafka = KafkaClient(hosts=kafka_hosts)
                producer = kafka.topics['test_topic'].get_producer(delivery_reports=False, linger_ms=0, sync=True)
                def emit(data):
                    j = json.dumps(data)
                    logging.debug("Sending: %s"%(j))
                    producer.produce(j.encode())
            except KeyError:
                logging.error('Must have KAFKA_HOSTS set in the environment')
                sys.exit(1);
        else:
            emit = lambda data: print("Sending: %s"%(json.dumps(data)))


        global running
        running = True
        
        signal.signal(signal.SIGTERM, term_handler)

        emit({'name': 'test data'})
        
        while running:
            time.sleep(2)


if __name__ == "__main__":
    app = PyKafka_Debug()
    app.run()


