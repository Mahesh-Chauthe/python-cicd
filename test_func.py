import pytest
from fastapi.testclient import TestClient
from app import app  # Assuming your FastAPI app is in a file named 'app.py'
from utils.producer import RabbitMQProducer
from utils.consumer import RabbitMQConsumer

# Create a test client for the FastAPI app
client = TestClient(app)

# Define test data
message_data = {
    "message_from": "user1",
    "message_to": "user2",
    "message": "Hello, World!",
}

# Define a mock RabbitMQ producer and consumer for testing
class MockRabbitMQProducer(RabbitMQProducer):
    def __init__(self):
        pass

    def connect(self):
        pass

    def send_message(self, message):
        pass

class MockRabbitMQConsumer(RabbitMQConsumer):
    def __init__(self):
        pass

    def connect(self):
        pass

    def start_consuming(self):
        return message_data  # Mocked message for testing

# Replace the original producers and consumers with the mock ones
app.dependency_overrides[RabbitMQProducer] = MockRabbitMQProducer
app.dependency_overrides[RabbitMQConsumer] = MockRabbitMQConsumer

def test_send_message():
    response = client.post("/send-message", json=message_data)
    assert response.status_code == 200
    assert response.json() == "Message Sent Successfully"

def test_get_message():
    response = client.get("/get-message")
    assert response.status_code == 200
    assert response.json() == message_data

# Run tests with pytest
if __name__ == '__main__':
    pytest.main()
