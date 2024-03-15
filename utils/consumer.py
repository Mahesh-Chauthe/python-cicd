from fastapi import FastAPI
import pika
import json

app = FastAPI()

class RabbitMQConsumer:
    def __init__(self, host='localhost', queue_name='testing2'):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.message = None  # Added to store the retrieved message

    def connect(self):
        try:
            # Establish a connection to the RabbitMQ server
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            self.channel = self.connection.channel()
            # Declare the same queue as in the producer
            self.channel.queue_declare(queue=self.queue_name, durable=True)
        except Exception as e:
            print(f"Error connecting to RabbitMQ: {str(e)}")

    def callback(self, ch, method, properties, body):
        try:
            # Deserialize the JSON message
            message = json.loads(body)
            # Process the message (you can store it in self.message)
            self.message = message
            return message
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    def start_consuming(self):
        try:
            while True:
                # Get a message from the queue without blocking
                method_frame, header_frame, body = self.channel.basic_get(self.queue_name)

                # If there are no more messages, exit the loop
                if method_frame is None:
                    break

                # Process the message
                return self.callback(None, None, None, body)  # Call the callback to process the message

            print('All messages consumed. Exiting.')
        except Exception as e:
            print(f'Error while consuming messages: {str(e)}')
        finally:
            self.close_connection()


    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("RabbitMQ connection closed.")


rabbitmq_consumer = RabbitMQConsumer()

