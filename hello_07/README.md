如何在 kafka-python 和 confluent-kafka 之间做出选择？

https://www.infoq.cn/article/2017/09/kafka-python-confluent-kafka

这篇文章是2017年的，倾向于选择 confluent-kafka，不知道 kafka-python 的问题有没有得到解决。

kafka-python 更容易上手！（python 3环境)

pip install kafka-python

https://cloud.tencent.com/developer/article/1446647

$ bin/zookeeper-server-start.sh config/zookeeper.properties
$ bin/kafka-server-start.sh config/server.properties

$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic my_favorite_topic2

WARNING: Due to limitations in metric names, topics with a period ('.') or underscore ('_') could collide. To avoid issues it is best to use either, but not both.

调整 topic 名称：my-favorite-topic2

删除 topic
$ bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic my_favorite_topic2

$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic my-favorite-topic2

$ bin/kafka-topics.sh --describe --zookeeper localhost:2181

生成消息：python producer.py

$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic my-favorite-topic2

消费消息：
    consumer.py
    consumer_02.py
    consumer_03.py
