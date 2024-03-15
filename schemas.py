from pydantic import BaseModel
from utils.producer import RabbitMQProducer

class MessageSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    message_from: str
    message_to: str
    message: str
