#!/bin/python3

from kafka_helper import *
from robot.api import logger
from robot.api.deco import keyword

##################################################
# Defines keywords to help in testing kafka stream processing applications.
class robotframework_pykafka:

    ##################################################
    # Create the kafka_helper.
    def __init__(self):
        self.kh = kafka_helper()
        
    ##################################################
    # Produce function
    # key may be None, I guess
    @keyword('Kafka Produce')
    def produce(self, topicName, key, value):
        return self.kh.produce(topicName, key, value)

    ##################################################
    # Call to cleanup after the kafka_helper.
    #def cleanup():
    #    self.kh.cleanup()

    ##################################################
    # Set offset to latest.  Deletes and recreates the cached consumer.
    @keyword('Kafka Set Consumer Offset To Latest')
    def setConsumerOffsetToLatest(self, topicName, consumerGroupName = None):
        self.kh.setConsumerOffsetToLatest(topicName, consumerGroupName)

    ##################################################
    # Set offset to earliest.  Deletes and recreates the cached consumer.
    @keyword('Kafka Set Consumer Offset To Earliest')
    def setConsumerOffsetToEarliest(self, topicName, consumerGroupName = None):
        self.kh.setConsumerOffsetToEarliest(topicName, consumerGroupName)

    ##################################################
    # Consume a message from a topic as a unicode string.
    # If the consumerGroupName is not specified, it defaults to the topicName.
    # Specify the consumerGroupName if you want to have more than one consumer of
    # the same topic.
    # Returns one message (key-value tuple), or None if no message available.
    @keyword('Kafka Consume String')
    def consumeString(self, topicName, consumerGroupName = None):
        return self.kh.consumeString(topicName, consumerGroupName)

    ##################################################
    # Consume a message from a topic, converting it to JSON
    # For our purposes, "JSON" is defined as a dict that has been
    # deserialized from JSON.  (Converted from json.loads("{}"))
    # Returns a key-value tuple where key is a unicode string and
    @keyword('Kafka Consume JSON')
    def consumeJson(self, topicName, consumerGroupName = None):
        return self.kh.consumeJson(topicName, consumerGroupName)

