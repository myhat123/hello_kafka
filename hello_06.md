Step 8: 使用Kafka Stream来处理数据
================================

http://kafka.apache.org/24/documentation/streams/quickstart
https://www.orchome.com/6

两个文档，内容相同，但有些差异

WordCount示例代码

https://github.com/apache/kafka/blob/2.4/streams/examples/src/main/java/org/apache/kafka/streams/examples/wordcount/WordCountDemo.java

$ bin/zookeeper-server-start.sh config/zookeeper.properties

$ bin/kafka-server-start.sh config/server.properties

创建 输入topic -> streams-plaintext-input

$ bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic streams-plaintext-input

创建 输出topic -> streams-wordcount-output

$ bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic streams-wordcount-output \
    --config cleanup.policy=compact

$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe

启动 WordCount 应用，作为中间环节处理 输入 和 输出

$ bin/kafka-run-class.sh org.apache.kafka.streams.examples.wordcount.WordCountDemo

从 input topic streams-plaintext-input, 对每条读入的消息执行 WordCount 算法
并持续写入 output topic streams-wordcount-output.

下面开始生成消息，发给输入topic
$ bin/kafka-console-producer.sh --broker-list localhost:9092 --topic streams-plaintext-input

下面消费消息，从输出topic拿消息
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic streams-wordcount-output \
    --from-beginning \
    --formatter kafka.tools.DefaultMessageFormatter \
    --property print.key=true \
    --property print.value=true \
    --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer \
    --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer

kafka-console-producer.sh ->
>all streams lead to kafka

kafka-console-consumer.sh ->
all	1
streams	1
lead	1
to	1
kafka	1

然后继续producer
>hello kafka streams

consumer的结果
all	1
streams	1
lead	1
to	1
kafka	1
hello	1
kafka	2
streams	2

更新的结果：hello -> 1, kafka -> 2, streams -> 2
