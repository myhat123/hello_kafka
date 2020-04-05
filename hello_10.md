参考资料:

https://docs.confluent.io/current/kafka-rest/quickstart.html  
https://docs.confluent.io/current/kafka-rest/monitoring.html#endpoints

kafka-rest
==========

> bin/zookeeper-server-start etc/kafka/zookeeper.properties

> bin/kafka-server-start etc/kafka/server.properties

> bin/kafka-rest-start etc/kafka-rest/kafka-rest.properties

> bin/schema-registry-start etc/schema-registry/schema-registry.properties

> ./bin/kafka-consumer-groups --bootstrap-server=localhost:9092 --all-groups --list

> ./bin/kafka-consumer-groups --bootstrap-server=localhost:9092 --all-groups --describe

```bash
# Produce a message using JSON with the value '{ "foo": "bar" }' to the topic jsontest
# 生成一个消息 json数据
curl -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" \
      -H "Accept: application/vnd.kafka.v2+json" \
      --data '{"records":[{"value":{"foo":"bar"}}]}' "http://localhost:8082/topics/jsontest"
# 运行结果
# Expected output from preceding command
  {
   "offsets":[{"partition":0,"offset":0,"error_code":null,"error":null}],"key_schema_id":null,"value_schema_id":null
  }
```

消费者看到:

> { "foo": "bar" }

```bash
http "http://localhost:8082/topics/jsontest"

# Create a consumer for JSON data, starting at the beginning of the topic's
# log. The consumer group is called "my_json_consumer" and the instance is "my_consumer_instance".

# Create a consumer for JSON data, starting at the beginning of the topic's
# log and subscribe to a topic. Then consume some data using the base URL in the first response.
# Finally, close the consumer with a DELETE to make it leave the group and clean up
# its resources.
```
```bash
# 创建消费组
curl -X POST -H "Content-Type: application/vnd.kafka.v2+json" \
      --data '{"name": "my_consumer_instance", "format": "json", "auto.offset.reset": "earliest"}' \
      http://localhost:8082/consumers/my_json_consumer

# 运行结果
# Expected output from preceding command
 {
  "instance_id":"my_consumer_instance",
  "base_uri":"http://localhost:8082/consumers/my_json_consumer/instances/my_consumer_instance"
 }
```

```bash
# 订阅
curl -X POST -H "Content-Type: application/vnd.kafka.v2+json" --data '{"topics":["jsontest"]}' \
 http://localhost:8082/consumers/my_json_consumer/instances/my_consumer_instance/subscription
```

```bash
# 获取消息
curl -X GET -H "Accept: application/vnd.kafka.json.v2+json" \
    http://localhost:8082/consumers/my_json_consumer/instances/my_consumer_instance/records

# 运行结果
[{"topic":"jsontest","key":null,"value":{"foo":"bar"},"partition":0,"offset":0}]
```

> curl "http://localhost:8082/topics/jsontest"

> curl -X DELETE -H "Content-Type: application/vnd.kafka.v2+json" \
      http://localhost:8082/consumers/my_json_consumer/instances/my_consumer_instance

采用httpie访问
=============

用httpie替换curl

> sudo apt-get install httpie

> http POST http://localhost:8082/topics/jsontest Content-Type:application/vnd.kafka.json.v2+json Accept:application/vnd.kafka.v2+json records:='[{"value":{"foo":"bar"}}]'

> http "http://localhost:8082/topics/jsontest" Accept:application/vnd.kafka.v2+json

> http POST http://localhost:8082/consumers/my_json_consumer Content-Type:application/vnd.kafka.v2+json name=my_consumer_instance format=json auto.offset.reset=earliest auto.commit.enable:=false

> http POST http://localhost:8082/consumers/my_json_consumer/instances/my_consumer_instance/subscription Content-Type:application/vnd.kafka.v2+json topics:='["jsontest"]'
 
> http http://localhost:8082/consumers/my_json_consumer/instances/my_consumer_instance/records Accept:application/vnd.kafka.json.v2+json

> http DELETE http://localhost:8082/consumers/my_json_consumer/instances/my_consumer_instance Content-Type:application/vnd.kafka.v2+json