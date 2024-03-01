import os
import pika

from producer_interface import mqProducerInterface

class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        # Save parameters to class variables
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.channel = None
        self.connection = None
        # Call setupRMQConnection
        self.setupRMQConnection()
        pass

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        
        # Establish Channel
        self.channel = self.connection.channel()
        
        # Create the exchange if not already present
        exchange = self.channel.exchange_declare(exchange="Tech Lab Exchange")
        

    def publishOrder(self, message: str) -> None:
        # Basic Publish to Exchange
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key, 
            body=message)
        # Close Channel
        self.channel.close()
        # Close Connection
        self.connection.close()