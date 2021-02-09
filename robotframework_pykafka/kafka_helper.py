#!/bin/python3

import json
import os
import time
from pykafka import KafkaClient
from pykafka.common import OffsetType
from utils import *

##################################################
# Kafka helper class.
class kafka_helper:

    ##################################################
    # Constructor.  The broker hostname and version are set in this order if 
    # specified:
    # 1. constructor parameters if they are non-None and non-empty
    # 2. environment variables KAFKA_HOST and KAFKA_BROKER_VERSION
    # 3. default values (localhost and 2.3)
    def __init__(self, kafkaBrokerHostname = None, kafkaBrokerVersion = None):

        # Determine the kafka host
        self._kafkaHost = ""
        if kafkaBrokerHostname:
            self._kafkaHost = kafkaBrokerHostname
        else:
            try:
                self._kafkaHost = os.environ['KAFKA_HOST']
            except KeyError as e:
                # Default it to localhost if not specified
                self._kafkaHost = "localhost:9092"
            except Exception as e:
                raise e

        # Determine the kafka version to use.  Default to 2.3.0 if not specified.
        self._kafkaBrokerVersion = ""
        if kafkaBrokerVersion:
            self._kafkaBrokerVersion = kafkaBrokerVersion
        else:
            try:
                self._kafkaBrokerVersion = os.environ['KAFKA_BROKER_VERSION']
            except KeyError as e:
                # Default it if not specified
                self._kafkaBrokerVersion = "2.3.0"
            except Exception as e:
                raise e

        # Get a kafka client
        self._client = KafkaClient(hosts = self._kafkaHost, broker_version = self._kafkaBrokerVersion)

        self._producers = dict()


    ##################################################
    # Cache the producers; key is topicName
    def _getProducer(self, topicName):
        if (topicName in self._producers):
            return self._producers[topicName]
        else:
            topic = self._client.topics[topicName]
            prod = topic.get_sync_producer()
            self._producers[topicName] = prod
            return prod

    ##################################################
    # Cache the consumers, key is (topicName, consumerGroupName)
    _consumers = dict()
    # If the consumerGroupName is not specified, it defaults to the topicName.
    # Specify the consumerGroupName if you want to have more than one consumer of
    # the same topic.
    def _getConsumer(self, topicName, consumerGroupName = None, setOffsetToEarliest = False):
        assert(topicName)

        cgn = ""
        if consumerGroupName:
            cgn = consumerGroupName
        else:
            cgn = topicName

        top = topicName

        if ((top, cgn) in self._consumers):
            return self._consumers[(top, cgn)]
        else:
            topic = self._client.topics[top]

            offsetType = OffsetType.LATEST
            if setOffsetToEarliest:
                offsetType = OffsetType.EARLIEST

            c = topic.get_simple_consumer(
                consumer_group = cgn,
                auto_offset_reset = offsetType,
                auto_commit_enable = True,
                reset_offset_on_start = True,
                consumer_timeout_ms = 1000)

            self._consumers[(top, cgn)] = c
            return c

    ##################################################
    # Produce function
    # key may be None, I guess
    def produce(self, topicName, key, value):
        assert(topicName)
        assert(value)
        k = toStr(key)
        v = toStr(value)

        top = toStr(topicName)
        producer = self._getProducer(top)
        #convert input message values to byte
        return producer.produce(bytes(v, 'utf-8'), bytes(k, 'utf-8')) #, datetime.datetime.now()) ### TODO - for certain broker versions (less than 1.0?) you have to provide a time?

    ##################################################
    ## TODO - needed?
    #def cleanup():
    #    producer.stop()

    ##################################################
    # Set offset to latest.  Deletes and recreates the cached consumer.
    def setConsumerOffsetToLatest(self, topicName, consumerGroupName = None):
        assert(topicName)
        top = toStr(topicName)
        cgn = toStr(consumerGroupName)

        log("Resetting offset to latest for topic "+top+" and consumer group "+str(cgn))
        if (top, cgn) in self._consumers:
            del self._consumers[(top, cgn)]
        self._getConsumer(top, cgn, setOffsetToEarliest = False)

    ##################################################
    # Set offset to earliest.  Deletes and recreates the cached consumer.
    def setConsumerOffsetToEarliest(self, topicName, consumerGroupName = None):
        assert(topicName)
        top = toStr(topicName)
        cgn = toStr(consumerGroupName)

        log("Resetting offset to earliest for topic "+top+" and consumer group "+str(cgn))
        if (top, cgn) in self._consumers:
            del self._consumers[(top, cgn)]
        self._getConsumer(top, cgn, setOffsetToEarliest = True)

    ##################################################
    # Consume a message from a topic as a unicode string.
    # If the consumerGroupName is not specified, it defaults to the topicName.
    # Specify the consumerGroupName if you want to have more than one consumer of
    # the same topic.
    # Returns one message (key-value tuple), or None if no message available.
    def consumeString(self, topicName, consumerGroupName = None):
        assert(topicName)
        top = toStr(topicName)
        cgn = toStr(consumerGroupName)

        consumer = self._getConsumer(top, cgn)
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
    def consumeJson(self, topicName, consumerGroupName = None):
        cm = self.consumeString(topicName, consumerGroupName)
        if cm == None:
            return None
        else:
            # Modify the returned message, decode the byte msg and convert string value to a dict:
            newValue = json.loads((cm[1].decode("utf-8")))
            tup = (cm[0].decode("utf-8"), newValue)
            return tup

