from fastapi import FastAPI
import uvicorn

from schemas import MessageSchema
from utils import producer
from utils import consumer

app = FastAPI()

@app.post("/send-message")
async def send_message(message: MessageSchema):
    try:
        user_message = {
            "message_from": message.message_from,
            "message_to": message.message_to,
            "message": message.message,
        }
        producer.rabbitmq_producer.connect()
        producer.rabbitmq_producer.send_message(user_message)
    except Exception as e:
        return e
    return "Message Sent Successfully"

@app.get("/get-message")
async def get_message():
    try:
        # Connect to RabbitMQ and start consuming messages
        consumer.rabbitmq_consumer.connect()
        # Assuming the callback returns the message, store it in a variable
        message = consumer.rabbitmq_consumer.start_consuming()
        # Close the RabbitMQ connection after retrieving the message
        return message
    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
        uvicorn.run(
        "app:app",
        host    = "0.0.0.0",
        port    = 8037,
        reload  = True
    )
