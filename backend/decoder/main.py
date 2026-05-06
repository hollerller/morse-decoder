import pika
import utils

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="decoded")


class MorseDecoder:
    def __init__(self):
        self.symbols = []

    def callback(self, ch, method, properties, body):
        if body.decode().strip() != "/":
            self.symbols.append(body.decode().strip())
        else:
            symbol = "".join(self.symbols)
            print(utils.morse_to_letter.get(symbol, "?"))
            channel.basic_publish(
                exchange="",
                routing_key="decoded",
                body=utils.morse_to_letter.get(symbol, "?"),
            )
            self.symbols = []


decoder = MorseDecoder()

channel.basic_consume(
    queue="morse", auto_ack=True, on_message_callback=decoder.callback
)

channel.start_consuming()
