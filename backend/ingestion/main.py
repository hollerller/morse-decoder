import serial
import pika

ser = serial.Serial("/dev/tty.usbmodem11103")
ser.baudrate = 115200
print(ser.name)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="morse")


while True:
    line = ser.readline()
    channel.basic_publish(exchange="", routing_key="morse", body=line.decode().strip())
    print(line.decode().strip())
