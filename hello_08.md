为使用 kafka-rest，因独立安装需要进行一系列构建，故直接采用confluent已经构建好的包。

https://docs.confluent.io/current/installation/installing_cp/zip-tar.html#prod-kafka-cli-install

Folder	Description
/bin/	Driver scripts for starting and stopping services
/etc/	Configuration files
/lib/	Systemd services
/logs/	Log files
/share/	Jars and licenses
/src/	Source files that require a platform-dependent build

ZooKeeper
=========

/etc/kafka/zookeeper.properties

bin/zookeeper-server-start etc/kafka/zookeeper.properties

Kafka
=====

/etc/kafka/server.properties

bin/kafka-server-start etc/kafka/server.properties

bin/kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

bin/kafka-topics --list --zookeeper localhost:2181

bin/kafka-console-producer --broker-list localhost:9092 --topic test

bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic test --from-beginning