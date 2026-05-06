from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pika
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CharConsumer:
    def __init__(self):
        self.symbols = []

    def callback(self, ch, method, properties, body):
        self.symbols.append(body.decode())
        print(self.symbols)

    def get_symbols(self):
        return self.symbols


consumer = CharConsumer()


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.basic_consume(
        queue="decoded", auto_ack=True, on_message_callback=consumer.callback
    )
    channel.start_consuming()


thread = threading.Thread(target=consume, daemon=True)
thread.start()


@app.get("/messages")
async def root():
    return {"symbols": consumer.get_symbols()}
