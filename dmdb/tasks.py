import pickle
import pika
from celery import shared_task
from dmdb.models import Dmdb


RMQ_QUEUE = 'demormq'
RMQ_HOST = 'localhost'
RMQ_BATCH_SIZE = 100


@shared_task
def load_data_to_mysql():
    """
    Get messages from RabbitMQ and save to DB
    :return:
    """
    print("[load_data_to_mysql] Connect to RabbitMQ")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RMQ_HOST))
    channel = connection.channel()
    channel_status = channel.queue_declare(queue=RMQ_QUEUE,
                                           durable=True,
                                           exclusive=False,
                                           auto_delete=False)

    total_msg_count = channel_status.method.message_count
    print("[load_data_to_mysql] Total messages in queue is '%s'" % (total_msg_count))

    consume_msg_count = min(total_msg_count, RMQ_BATCH_SIZE)
    print("[load_data_to_mysql] Messages consume counter is '%s'" % (consume_msg_count))

    if consume_msg_count == 0:
        print("[load_data_to_mysql] Close RabbitMQ connection")
        connection.close()
        return 0

    print("[load_data_to_mysql] Start messages processing")
    for iter in range(consume_msg_count):
        msg = channel.basic_get(queue=RMQ_QUEUE,
                                no_ack=False)
        msg_delivery_tag = msg[0].delivery_tag
        msg_payload = pickle.loads(msg[2])
        print("[load_data_to_mysql] Received message with tx_id '%s'" % (msg_payload['uuid']))
        db_record = Dmdb(tx_obj=msg_payload['uuid'],
                         json_obj=msg_payload['data'])
        db_record.save()
        channel.basic_ack(delivery_tag=msg_delivery_tag,
                          multiple=False)

    print("[load_data_to_mysql] Close RabbitMQ connection")
    connection.close()
