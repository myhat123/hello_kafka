Step 6: 设置多个broker集群
========================

首先为每个broker创建一个配置文件:

cp config/server.properties config/server-1.properties 
cp config/server.properties config/server-2.properties

现在编辑这些新建的文件，设置以下属性：

config/server-1.properties: 
    broker.id=1 
    listeners=PLAINTEXT://:9093 
    log.dir=/tmp/kafka-logs-1

config/server-2.properties: 
    broker.id=2 
    listeners=PLAINTEXT://:9094 
    log.dir=/tmp/kafka-logs-2

broker.id是集群中每个节点的唯一且永久的名称，我们修改端口和日志目录是因为我们现在在同一台机器上运行，
我们要防止broker在同一端口上注册和覆盖对方的数据。

我们已经运行了zookeeper和刚才的一个kafka节点，所有我们只需要在启动2个新的kafka节点。

$ bin/kafka-server-start.sh config/server-1.properties  启动端口9093
$ bin/kafka-server-start.sh config/server-2.properties  启动端口9094

/tmp目录下，关机重启/tmp下内容会清除
    kafka-logs
    kafka-logs-1
    kafka-logs-2

现在，我们创建一个新topic，把备份设置为：3

$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic

列出topics:

$ bin/kafka-topics.sh --list --zookeeper localhost:2181
my-replicated-topic
test

[zk: localhost:2181(CONNECTED) 6] ls /brokers/topics
[my-replicated-topic, test]

[zk: localhost:2181(CONNECTED) 7] get /brokers/topics/my-replicated-topic
{"version":2,"partitions":{"0":[2,1,0]},"adding_replicas":{},"removing_replicas":{}}

现在我们已经有了一个集群了，我们怎么知道每个集群在做什么呢？运行命令“describe topics”

$ bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
Topic: my-replicated-topic	PartitionCount: 1	ReplicationFactor: 3	Configs: 
Topic: my-replicated-topic	Partition: 0	Leader: 2	Replicas: 2,1,0	Isr: 2,1,0

输出解释：第一行是所有分区的摘要，其次，每一行提供一个分区信息，因为我们只有一个分区，所以只有一行。

$ bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test
Topic: test	PartitionCount: 1	ReplicationFactor: 1	Configs: 
Topic: test	Partition: 0	Leader: 2	Replicas: 2	Isr: 2

1. "leader"：该节点负责该分区的所有的读和写，每个节点的leader都是随机选择的。
2. "replicas"：备份的节点列表，无论该节点是否是leader或者目前是否还活着，只是显示。
3. "isr"：“同步备份”的节点列表，也就是活着的节点并且正在同步leader。

让我们来发布一些信息在新的topic上：

$ bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-replicated-topic
my test message 1
my test message 2
^C

现在，消费这些消息。

$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic my-replicated-topic

测试集群的容错
------------

先查Leader是哪个

$ bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
Topic: my-replicated-topic	PartitionCount: 1	ReplicationFactor: 3	Configs: 
	Topic: my-replicated-topic	Partition: 0	Leader: 0	Replicas: 0,1,2	Isr: 0,1,2

Leader: 0

kill掉leader，Broker0作为当前的leader，也就是kill掉Broker0。

对应不同的server.properties
0 -> server.properties
1 -> server-1.properties
2 -> server-2.properties

$ ps -ef | grep server.properties

$ kill -9 6451

此时再看 Leader

$ bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
Topic: my-replicated-topic	PartitionCount: 1	ReplicationFactor: 3	Configs: 
	Topic: my-replicated-topic	Partition: 0	Leader: 1	Replicas: 0,1,2	Isr: 1,2

Leader 从0变成了1

再查消息：
Leader 1 -> 端口9093
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --from-beginning --topic my-replicated-topic

消息仍然可以获取，没有丢失。