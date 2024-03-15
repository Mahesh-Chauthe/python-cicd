import pika
import json


class RabbitMQProducer:
    def __init__(self, host='localhost', queue_name='testing2'):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            # Establish a connection to the RabbitMQ server
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            self.channel = self.connection.channel()
            # Declare a queue (create it if it doesn't exist)
            self.channel.queue_declare(queue=self.queue_name, durable=True)
        except Exception as e:
            print(f"Error connecting to RabbitMQ: {str(e)}")

    def send_message(self, message_dict):
        try:
            # Serialize the message dictionary to JSON
            message_json = json.dumps(message_dict)
            # Publish the message to the queue
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message_json)
            print(f" [x] Sent '{message_json}'")
        except Exception as e:
            print(f"Error sending message to RabbitMQ: {str(e)}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("RabbitMQ connection closed.")



rabbitmq_producer = RabbitMQProducer()

