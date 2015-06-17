import pika

from job import Job

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.basicConfig()

def publish(job, channel, exchange):
    channel.basic_publish(exchange=exchange, routing_key=job.kind,
            body=job.to_json())

if __name__ == '__main__':
    exchange = 'jobs'
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = conn.channel()
    channel.exchange_declare(exchange=exchange, type='direct')

    for i in range(10):
        job = Job('wait_around', 1)
        publish(job, channel, exchange)
    conn.close()
