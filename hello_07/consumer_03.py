from kafka import KafkaConsumer
from kafka import TopicPartition

consumer = KafkaConsumer('my-favorite-topic2', 
        bootstrap_servers='localhost:9092')


print(consumer.partitions_for_topic("my-favorite-topic2"))  #获取test主题的分区信息
print(consumer.topics())  #获取主题列表
print(consumer.subscription())  #获取当前消费者订阅的主题
print(consumer.assignment())  #获取当前消费者topic、分区信息
print(consumer.beginning_offsets(consumer.assignment())) #获取当前消费者可消费的偏移量
print(consumer.position(TopicPartition(topic='my-favorite-topic2', partition=0))) #获取当前主题的最新偏移量
consumer.seek(TopicPartition(topic='my-favorite-topic2', partition=0), 3)  #重置偏移量，从第4个偏移量消费

for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (
        message.topic, message.partition,
        message.offset, message.key,
        message.value))