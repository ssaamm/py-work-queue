import pika, time
from multiprocessing import Pool

from job import Job

job_kinds_this_can_handle = {'square_it', 'wait_around'}

def handle_job(job):
    if job.kind == 'square_it':
        squared = job.data ** 2
        print 'squared:', squared
    elif job.kind == 'wait_around':
        time.sleep(job.data)
        print 'waited', job.data
    else:
        print 'unknown job kind:', job.kind

def handle_message(channel, method, properties, body):
    job = Job.from_json(body)
    pool.apply_async(handle_job, [job])

pool = Pool(processes=2)

if __name__ == '__main__':
    exchange = 'jobs'
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = conn.channel()
    channel.exchange_declare(exchange=exchange, type='direct')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    for job_kind in job_kinds_this_can_handle:
        channel.queue_bind(exchange=exchange, queue=queue_name,
                routing_key=job_kind)

    channel.basic_consume(handle_message,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()
