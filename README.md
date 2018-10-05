# robotframework_pykafka

This is a robot framework wrapper around pykafka, the best python kafka library out there as of this writing, and the only one that supports kafka 1.0 and 1.1.

## Features

This library provides some robotframework keywords that make working with Kafka topics easier.  You can produce and consume from topics, and the framework will manage the producers and consumers for you, behind the scenes, based on the topics and consumer groups you specify.  See below for more details.

### Python Version Support

Support is guaranteed for Python 2.7.X only at this time.  It has not been tested on anything else.  All dependent libs should work under 3 but we have not tested yet.

### Kafka Version Support

Support is guaranteed for 1.0.X only at this time.  It has not been tested on anything else.

### Message Formats

#### Topic Keys

Only string keys are supported.  Currently JSON conversions (from string to dict) will have to be done by clients.

#### Topic values

Only string or JSON strings are supported.

## Usage

### Environment Vars

The following environment variables are assumed to have been set up in the session where this code is executed.  Defaults will be provided if not specified.

* KAFKA_HOST:  "localhost:9092" is the default.
* KAFKA_BROKER_VERSION:  "1.0.0" is the default.

### Keywords 

#### Producing

1. Kafka Produce   |  topicName   |  key   |  value
    * Produce a message on a kafka topic using the key and value specified.  Both key and value must be strings.
    * Keys may be None, if you want

#### Consuming

Before reading from a Kafka topic, you have to initialize a consumer by telling it how to read from the topic, from the newest/latest message or from the oldest/earliest.

For both the "Kafka Set Consumer Offset" keywords, the consumerGroupName is optional; it defaults to be the same as the topicName.  If specified, you will use the consumer that references this specific consumerGroupName, which may be important.  For example, if you want to test two consumers of the same topic, set the 2nd consumer to a different consumerGroupName so the offsets are not shared.

1. Kafka Set Consumer Offset To Latest  |  topicName  |  [ consumerGroupName ]
    * This creates a consumer and sets the topic offset to the latest/newest message.
    * The consumer is cached and referenced internally by (topicName, consumerGroupName)

1. Kafka Set Consumer Offset To Earliest  |  topicName  | [ consumerGroupName ]
    * This creates a consumer and sets the topic offset to the earliest/oldest message.
    * The consumer is cached and referenced internally by (topicName, consumerGroupName)

1. Kafka Consume String  |  topicName  | [ consumerGroupName ]
    * Consume a message from the specified consumer topic (identified by (topicName, consumerGroupName)).  The returned object will be a tuple of two Strings, where the first element is the Key, and the second element is the Value.
    * You have not previously set the consumer offset for this topic/consumer group, then a new consumer will be created using the latest offset as the initial offset.

1. Kafka Consume JSON  |  topicName  | [ consumerGroupName ]
    * Consume a message from the specified consumer topic (identified by (topicName, consumerGroupName)).  The returned object will be a tuple of two objects, where the first element is the string Key, and the second element is the JSON string converted into a dict.  This is the keyword to use when you want to compare JSON.  Raw JSON strings cannot be compared because the fields' ordering in the string is not guaranteed, so it is better to use dicts.
    * You have not previously set the consumer offset for this topic/consumer group, then a new consumer will be created using the latest offset as the initial offset.

## Examples

See the tests/ directory for some example tests of a kafka streams application.

## TODO

1. Support for producing JSON (ie. use dict as argument that is converted internally to JSON string, "Kafka Produce JSON")
1. Support for producing and consuming AVRO (pull requests wanted), ie. "Kafka Consume AVRO" and "Kafka Produce AVRO"
1. Test under later kafka versions
1. Test under Python 3.

## License

This software is copyright 2018 Zebra Technologies, and is licensed under the Apache 2 software license.
