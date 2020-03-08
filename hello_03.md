kafka安装和启动

https://kafka.apache.org/downloads.html

Step 1: 下载解压源代码
====================

tar zxvf kafka_2.12-2.4.0.tar.gz
cd kafka_2.12-2.4.0

Step 2: 启动服务
===============

启动Zookeeper
-------------

运行kafka需要使用Zookeeper，所以你需要先启动Zookeeper，如果你没有Zookeeper，你可以使用
kafka自带打包和配置好的Zookeeper。

config/zookeeper.properties

    # the directory where the snapshot is stored.
    dataDir=/tmp/zookeeper
    # the port at which the clients will connect
    clientPort=2181
    # disable the per-ip limit on the number of connections since this is a non-production config
    maxClientCnxns=0
    # Disable the adminserver by default to avoid port conflicts.
    # Set the port to something non-conflicting if choosing to enable this
    admin.enableServer=false
    # admin.serverPort=8080

bin/zookeeper-server-start.sh

    ......
    exec $base_dir/kafka-run-class.sh $EXTRA_ARGS org.apache.zookeeper.server.quorum.QuorumPeerMain "$@"

$ bin/zookeeper-server-start.sh config/zookeeper.properties
    默认2181端口

启动kafka服务
------------

config/server.properties

    # see kafka.server.KafkaConfig for additional details and defaults

    ############################# Server Basics #############################

    # The id of the broker. This must be set to a unique integer for each broker.
    broker.id=0

    ############################# Socket Server Settings #############################

    # The address the socket server listens on. It will get the value returned from 
    # java.net.InetAddress.getCanonicalHostName() if not configured.
    #   FORMAT:
    #     listeners = listener_name://host_name:port
    #   EXAMPLE:
    #     listeners = PLAINTEXT://your.host.name:9092
    #listeners=PLAINTEXT://:9092

    # Hostname and port the broker will advertise to producers and consumers. If not set, 
    # it uses the value for "listeners" if configured.  Otherwise, it will use the value
    # returned from java.net.InetAddress.getCanonicalHostName().
    #advertised.listeners=PLAINTEXT://your.host.name:9092

    # Maps listener names to security protocols, the default is for them to be the same. See the config documentation for more details
    #listener.security.protocol.map=PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL

    # The number of threads that the server uses for receiving requests from the network and sending responses to the network
    num.network.threads=3

    # The number of threads that the server uses for processing requests, which may include disk I/O
    num.io.threads=8

    # The send buffer (SO_SNDBUF) used by the socket server
    socket.send.buffer.bytes=102400

    # The receive buffer (SO_RCVBUF) used by the socket server
    socket.receive.buffer.bytes=102400

    # The maximum size of a request that the socket server will accept (protection against OOM)
    socket.request.max.bytes=104857600

    ############################# Log Basics #############################

    # A comma separated list of directories under which to store log files
    log.dirs=/tmp/kafka-logs

    # The default number of log partitions per topic. More partitions allow greater
    # parallelism for consumption, but this will also result in more files across
    # the brokers.
    num.partitions=1

    # The number of threads per data directory to be used for log recovery at startup and flushing at shutdown.
    # This value is recommended to be increased for installations with data dirs located in RAID array.
    num.recovery.threads.per.data.dir=1
    ......

bin/kafka-server-start.sh

    ......
    exec $base_dir/kafka-run-class.sh $EXTRA_ARGS kafka.Kafka "$@"

$ bin/kafka-server-start.sh config/server.properties &
    默认9092端口

Step 3: 创建一个主题(topic)
=========================

bin/kafka-topics.sh
-------------------
    ......
    exec $(dirname $0)/kafka-run-class.sh kafka.admin.TopicCommand "$@"

创建一个名为“test”的Topic，只有一个分区和一个备份：

$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

创建好之后，可以通过运行以下命令，查看已创建的topic信息：

$ bin/kafka-topics.sh --list --zookeeper localhost:2181

test

zookeeper cli命令行
==================

下载解压 zookeeper 3.5.7

http://zookeeper.apache.org/releases.html

参考教程
https://www.w3cschool.cn/zookeeper/zookeeper_installation.html

$ bin/zkCli.sh

ls /brokers
ls /brokers/topics
get /brokers/topics/test

[zk: localhost:2181(CONNECTED) 10] ls /brokers
[ids, seqid, topics]
[zk: localhost:2181(CONNECTED) 11] ls /brokers/topics
[test]
[zk: localhost:2181(CONNECTED) 12] get /brokers/topics/test
{"version":2,"partitions":{"0":[0]},"adding_replicas":{},"removing_replicas":{}}

Step 4: 发送消息
===============

Kafka提供了一个命令行的工具，可以从输入文件或者命令行中读取消息并发送给Kafka集群。每一行是一条消息。
运行producer（生产者）,然后在控制台输入几条消息到服务器。

bin/kafka-console-producer.sh
-----------------------------
    ......
    exec $(dirname $0)/kafka-run-class.sh kafka.tools.ConsoleProducer "$@"

$ bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
>This is a message
>This is another message

Step 5: 消费消息
================

消费消息的命令行工具，将存储的信息输出出来。这种消费，也可以看作是查询，因为有--from-begining从头开始

bin/kafka-console-consumer.sh
-----------------------------
    ......
    exec $(dirname $0)/kafka-run-class.sh kafka.tools.ConsoleConsumer "$@"

$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning

不同的终端上运行上述命令，那么当你在运行生产者时，消费者就能消费到生产者发送的消息。
即：回到 Step 4 生产新的消息，消费者可以马上收到新的消息

Step 4 退出，Step 5也同样退出，再进入 Step 5 仍然可以看到全部从头开始的消息
再继续生产消息，消费者也继续获取消息

关闭kafka服务
============

$ bin/kafka-server-stop.sh

关闭zookeeper服务
================

$ bin/zookeeper-server-stop.sh
