from kafka import KafkaProducer
from time import sleep

def start_producer():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    for i in range(3):
        msg = 'msg is ' + str(i)
        producer.send('my-favorite-topic2', msg.encode('utf-8'))
        sleep(3)

    producer.close()

if __name__ == '__main__':
    start_producer()