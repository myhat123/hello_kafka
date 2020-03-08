Step 7: 使用 Kafka Connect 来 导入/导出 数据
=========================================

Kafka Connect是导入和导出数据的一个工具。它是一个可扩展的工具，运行连接器，实现与自定义的逻辑的外部系统交互。
在这个快速入门里，我们将看到如何运行Kafka Connect用简单的连接器从文件导入数据到Kafka主题，再从Kafka主题导出
数据到文件。

echo -e "foo\nbar" > test.txt

test.txt 文件在 kafka 安装目录下

config/connect-standalone.properties

    # These are defaults. This file just demonstrates how to override some settings.
    bootstrap.servers=localhost:9092

    # The converters specify the format of data in Kafka and how to translate it int
    o Connect data. Every Connect user will
    # need to configure these based on the format they want their data in when loade
    d from or stored into Kafka
    key.converter=org.apache.kafka.connect.json.JsonConverter
    value.converter=org.apache.kafka.connect.json.JsonConverter
    # Converter-specific settings can be passed in by prefixing the Converter's setting with the converter we want to apply
    # it to
    key.converter.schemas.enable=true
    value.converter.schemas.enable=true

    offset.storage.file.filename=/tmp/connect.offsets


config/connect-file-source.properties

    name=local-file-source
    connector.class=FileStreamSource
    tasks.max=1
    file=test.txt
    topic=connect-test


config/connect-file-sink.properties

    name=local-file-sink
    connector.class=FileStreamSink
    tasks.max=1
    file=test.sink.txt
    topics=connect-test


我们将启动两个standalone（独立）运行的连接器，这意味着它们各自运行在一个单独的本地专用 进程上。 
我们提供三个配置文件。

首先是Kafka Connect的配置文件，
config/connect-standalone.properties
包含常用的配置，如Kafka brokers连接方式和数据的序列化格式。

其余的配置文件均指定一个要创建的连接器。
config/connect-file-source.properties
config/connect-file-sink.properties

各指定了topics -> connect-test, file -> text.txt, text.sink.txt
这些文件包括连接器的唯一名称，类的实例，以及其他连接器所需的配置。
    
bin/connect-standalone.sh
    ......
    exec $(dirname $0)/kafka-run-class.sh $EXTRA_ARGS org.apache.kafka.connect.cli.C
    onnectStandalone "$@"

$ bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties

在启动过程中，你会看到一些日志消息，包括一些连接器正在实例化的指示。 一旦Kafka Connect进程启动，
源连接器就开始从 test.txt 读取行并且 将它们生产到主题 connect-test 中，同时接收器连接器也开始
从主题 connect-test 中读取消息， 并将它们写入文件 test.sink.txt 中。

请注意，数据存储在Kafka topic connect-test

[zk: localhost:2181(CONNECTED) 5] get /brokers/topics/connect-test
{"version":2,"partitions":{"0":[2]},"adding_replicas":{},"removing_replicas":{}}

$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic connect-test --from-beginning

{"schema":{"type":"string","optional":false},"payload":"foo"}
{"schema":{"type":"string","optional":false},"payload":"bar"}

输出是json格式，在connect-standalone.properties中有设置

连接器一直在处理数据，所以我们可以将数据添加到文件中，并看到它在pipeline 中移动：

> echo Another line >> test.txt

您应该可以看到这一行出现在控制台用户输出和接收器文件中。