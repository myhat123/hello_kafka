from kafka import KafkaConsumer
import time

def start_consumer():
    consumer = KafkaConsumer('my-favorite-topic2', 
        auto_offset_reset='earliest',
        bootstrap_servers='localhost:9092')
        
    for msg in consumer:
        print(msg)
        print("topic = %s" % msg.topic) # topic default is string
        print("partition = %d" % msg.partition)
        print("offset = %d" % msg.offset)
        print("value = %s" % msg.value.decode()) # bytes to string
        print("timestamp = %d" % msg.timestamp)
        print("time = ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( msg.timestamp/1000 )) )

if __name__ == '__main__':
    start_consumer()