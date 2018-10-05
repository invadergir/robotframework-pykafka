import json
import os
from pykafka import KafkaClient
from pykafka.common import OffsetType
from robot.api import logger
from robot.api.deco import keyword

# Determine the kafka host
_kafkaHost = ""
try:
    _kafkaHost = os.environ['KAFKA_HOST']
except KeyError as e:
    # Default it to localhost if not specified
    _kafkaHost = "localhost:9092"
except Exception as e:
    raise e

# Determine the kafka version to use.  Default to 1.0.0 if not specified.
_kafkaBrokerVersion = ""
try:
    _kafkaBrokerVersion = os.environ['KAFKA_BROKER_VERSION']
except KeyError as e:
    # Default it if not specified
    _kafkaBrokerVersion = "1.0.0"
except Exception as e:
    raise e

# Get a kafka client
_client = KafkaClient(hosts = _kafkaHost, broker_version = _kafkaBrokerVersion)

##################################################
# log something 
def log(msg):
    print('[robot_pykafka] ' + msg)
    logger.info('[robot_pykafka] ' + msg)

##################################################
# Safely convert to string.  
# If the input is None, return None, else convert via str().
# This is needed because robot uses ustrings.
def toStr(inputString):
    if None == inputString:
        return None
    elif isinstance(inputString, str):
        return inputString
    elif isinstance(inputString, unicode):
        return inputString.encode("utf-8")
    else:
        # not a string
        return None

    return inputString.encode("utf-8")

##################################################
# Convert an input string to unicode
# If the input is None, return None, else convert via str().
def toUnicode(inputString):
    if None == inputString:
        return None
    elif isinstance(inputString, str):
        return unicode(inputString, "utf-8")
    elif isinstance(inputString, unicode):
        return inputString
    else:
        # not a string
        return None

##################################################
# Cache the producers; key is topicName
_producers = dict()
def _getProducer(topicName):
    if (topicName in _producers):
        return _producers[topicName]
    else:
        topic = _client.topics[topicName]
        prod = topic.get_sync_producer()
        _producers[topicName] = prod
        return prod

##################################################
# Cache the consumers, key is (topicName, consumerGroupName)
_consumers = dict()
# If the consumerGroupName is not specified, it defaults to the topicName.
# Specify the consumerGroupName if you want to have more than one consumer of
# the same topic.
def _getConsumer(topicName, consumerGroupName = None, setOffsetToEarliest = False):
    assert(topicName)

    cgn = ""
    if consumerGroupName:
        cgn = consumerGroupName
    else:
        cgn = topicName

    top = topicName

    if ((top, cgn) in _consumers):
        return _consumers[(top, cgn)]
    else:
        topic = _client.topics[top]

        offsetType = OffsetType.LATEST
        if setOffsetToEarliest:
            offsetType = OffsetType.EARLIEST

        c = topic.get_simple_consumer(
            consumer_group = cgn,
            auto_offset_reset = offsetType,
            auto_commit_enable = True,
            reset_offset_on_start = True,
            consumer_timeout_ms = 1000)

        _consumers[(top, cgn)] = c
        return c

##################################################
# Produce function
# key may be None, I guess
@keyword('Kafka Produce')
def produce(topicName, key, value):
    assert(topicName)
    assert(value)
    k = toStr(key)
    v = toStr(value)

    top = toStr(topicName)
    producer = _getProducer(top)
    return producer.produce(v, k) #, datetime.datetime.now()) ### TODO - for certain broker versions (less than 1.0?) you have to provide a time?

##################################################
## TODO - needed?
#def cleanup():
#    producer.stop()

##################################################
# Set offset to latest.  Deletes and recreates the cached consumer.
@keyword('Kafka Set Consumer Offset To Latest')
def setConsumerOffsetToLatest(topicName, consumerGroupName = None):
    assert(topicName)
    top = toStr(topicName)
    cgn = toStr(consumerGroupName)

    log("Resetting offset to latest for topic "+top+" and consumer group "+str(cgn))
    if (top, cgn) in _consumers:
        del _consumers[(top, cgn)]
    _getConsumer(top, cgn, setOffsetToEarliest = False)

##################################################
# Set offset to earliest.  Deletes and recreates the cached consumer.
@keyword('Kafka Set Consumer Offset To Earliest')
def setConsumerOffsetToEarliest(topicName, consumerGroupName = None):
    assert(topicName)
    top = toStr(topicName)
    cgn = toStr(consumerGroupName)

    log("Resetting offset to earliest for topic "+top+" and consumer group "+str(cgn))
    if (top, cgn) in _consumers:
        del _consumers[(top, cgn)]
    _getConsumer(top, cgn, setOffsetToEarliest = True)

##################################################
# Consume a message from a topic as a unicode string.
# If the consumerGroupName is not specified, it defaults to the topicName.
# Specify the consumerGroupName if you want to have more than one consumer of
# the same topic.
# Returns one message (key-value tuple), or None if no message available.
@keyword('Kafka Consume String')
def consumeString(topicName, consumerGroupName = None):
    assert(topicName)
    top = toStr(topicName)
    cgn = toStr(consumerGroupName)

    consumer = _getConsumer(top, cgn)
    msg = consumer.consume()
    if None == msg:
        return None
    else:
        return (msg.partition_key, msg.value) # , msg.offset)

##################################################
# Consume a message from a topic, converting it to JSON
# For our purposes, "JSON" is defined as a dict that has been
# deserialized from JSON.  (Converted from json.loads("{}"))
# Returns a key-value tuple where key is a unicode string and 
@keyword('Kafka Consume JSON')
def consumeJson(topicName, consumerGroupName = None):
    cm = consumeString(topicName, consumerGroupName)
    if cm == None:
        return None
    else: 
        # Modify the returned message, converting string value to a dict:
        newValue = json.loads(cm[1])
        tup = (cm[0], newValue)
        return tup

