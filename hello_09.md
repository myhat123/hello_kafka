参考资料:

https://blog.csdn.net/u012369535/article/details/93844653?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task

Mr-Lee-long 博客  
https://www.cnblogs.com/sunshine-long/p/9857107.html  
https://www.cnblogs.com/sunshine-long/p/9843492.html  
https://www.cnblogs.com/sunshine-long/category/1217916.html

注意：消费者有新旧版本之分

消费组
=====

> bin/zookeeper-server-start etc/kafka/zookeeper.properties

> bin/kafka-server-start etc/kafka/server.properties

> bin/kafka-topics --list --zookeeper localhost:2181

> bin/kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic test

```
bin/kafka-topics --zookeeper localhost:2181 --describe --topic test
    Topic: test	PartitionCount: 3	ReplicationFactor: 1	Configs: 
        Topic: test	Partition: 0	Leader: 0	Replicas: 0	Isr: 0	Offline: 
        Topic: test	Partition: 1	Leader: 0	Replicas: 0	Isr: 0	Offline: 
        Topic: test	Partition: 2	Leader: 0	Replicas: 0	Isr: 0	Offline:
```

> bin/kafka-console-producer --broker-list localhost:9092 --topic test

> bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic test --consumer-property group.id=group_my_test

消费者可接收到消息，但是顺序和生产者的发送顺序不一样，也就是说当一个主题有多个分区时，消费者接受消息的顺序是乱序的，因为每个partition的网络性能不一样，读写性能也不一样。

> ./bin/kafka-consumer-groups --bootstrap-server=localhost:9092 --all-groups --describe

> bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic test --offset 8 --partition 0


两个终端窗口运行同一个消费组  
consumers 1:  
```
bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic test --consumer-property group.id=group_my_test

7
8
23
```

consumers 2:  

```
bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic test --consumer-property group.id=group_my_test

5
6
9
1
```

可以看出，对于在同一个消费组内的两个消费者consumer1和consumer2，各自获取同一topic内的消息，这验证了一个topic内的一个分区只能被同一消费组内的一个消费者所消费，不能被一个组内的多个消费者所消费

新版本消费者去掉了对zookeeper的依赖，当启动一个消费者时不再向zookeeper注册，而是
由消费组协调器统一管理，已消费的消息偏移量提交后会保存到名为“__consumer_offsets”
内部主题中

__consumer_offsets 有50个分区

```
bin/kafka-topics --zookeeper localhost:2181 --describe --topic __consumer_offsets
Topic: __consumer_offsets	PartitionCount: 50	ReplicationFactor: 1	Configs: compression.type=producer,cleanup.policy=compact,segment.bytes=104857600
	Topic: __consumer_offsets	Partition: 0	Leader: 0	Replicas: 0	Isr: 0	Offline: 
	Topic: __consumer_offsets	Partition: 1	Leader: 0	Replicas: 0	Isr: 0	Offline: 
    ......
```

> ./bin/kafka-console-consumer --bootstrap-server localhost:9092 --consumer-property group.id=group_my_test --consumer-property client.id=hzg --topic test

> ./bin/kafka-consumer-groups --bootstrap-server localhost:9092 --list

> ./bin/kafka-consumer-groups --bootstrap-server=localhost:9092 --all-groups --describe

> ./bin/kafka-consumer-groups --bootstrap-server=localhost:9092 --describe --group=group_my_test

查看consumer组内消费的offset

zkCli.sh
========
```
[zk: localhost:2181(CONNECTED) 0] ls /
[admin, brokers, cluster, config, consumers, controller, controller_epoch, isr_change_notification, latest_producer_id_block, log_dir_event_notification, zookeeper]
[zk: localhost:2181(CONNECTED) 1] ls /brokers
[ids, seqid, topics]
[zk: localhost:2181(CONNECTED) 2] ls /brokers/topics
[__confluent.support.metrics, _confluent-license, test]
[zk: localhost:2181(CONNECTED) 3] ls /brokers/topics/test
[partitions]
[zk: localhost:2181(CONNECTED) 4] ls /brokers/topics/test/partitions
[0, 1, 2]
[zk: localhost:2181(CONNECTED) 5] ls /brokers/topics/test/partitions/0
[state]
[zk: localhost:2181(CONNECTED) 6] ls /brokers/topics/test/partitions/0/state
[]
[zk: localhost:2181(CONNECTED) 7] get /brokers/topics/test/partitions/0/state
{"controller_epoch":1,"leader":0,"version":1,"leader_epoch":0,"isr":[0]}
```