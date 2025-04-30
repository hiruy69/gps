import pika
import os
from dotenv import load_dotenv
import json
import uuid
# Load environment variables from .env file
load_dotenv()

class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = os.getenv('RABBITMQ_QUEUE', 'my_queue')
        self.routing_key = os.getenv('RABBITMQ_ROUTING_KEY', 'gps_data')
        self.exchange = os.getenv('RABBITMQ_EXCHANGE', 'gps_exchange')
        print(f"RabbitMQ Client initialized with queue: {self.queue_name}, routing key: {self.routing_key}, exchange: {self.exchange}")
        self._connect()

    def _connect(self):
        """Establish and store the RabbitMQ connection and channel."""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.getenv("RABBITMQ_HOST", "localhost"),
                    port=int(os.getenv("RABBITMQ_PORT", 5672)),
                    credentials=pika.PlainCredentials(
                        os.getenv("RABBITMQ_USER", "guest"),
                        os.getenv("RABBITMQ_PASSWORD", "guest")
                    )
                )
            )
        self.channel = self.connection.channel()

    def send(self, data: dict,queue_name: str = None):
        """Send a JSON-encoded dictionary to the specified queue."""
        if not self.channel or self.channel.is_closed:
            self._connect()
        queue_name = queue_name or self.queue_name
        self.channel.queue_declare(queue=queue_name, durable=True)

        message_id = str(uuid.uuid4())
        body = json.dumps(data)

        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json',
                message_id=message_id,
            )
        )

        print(f"[x] Sent to {queue_name} | ID: {message_id}")

    def close(self):
        """Manually close the connection if needed."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
